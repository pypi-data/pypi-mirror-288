import numpy as np
import pandas as pd
import struct
import os
from nptdms import TdmsFile, TdmsWriter, ChannelObject, RootObject, GroupObject


def read_dat_file(dat_file_path):
    """
    Reads a .dat file to extract metadata and configure channel information.

    Parameters:
        dat_file_path (str): The path to the .dat file.

    Returns:
        tuple: A tuple containing a dictionary with channel configurations and the path to the data file.
    """
    channels = {}
    current_channel = None
    data_file_path = None

    try:
        with open(dat_file_path, 'r') as file:
            for line in file:
                line = line.strip()
                if line.startswith('#BEGINCHANNELHEADER'):
                    current_channel = {}
                elif line.startswith('#ENDCHANNELHEADER'):
                    if current_channel:
                        channels[current_channel['name']] = current_channel
                        if data_file_path is None:
                            data_file_path = current_channel.get('data_file')
                        current_channel = None
                elif current_channel is not None:
                    if ',' in line:
                        key, value = line.split(',', 1)
                        key, value = key.strip(), value.strip()
                        if key == '200':
                            current_channel['name'] = value
                        elif key == '202':
                            current_channel['unit'] = value
                        elif key == '214':
                            current_channel['dtype'] = value
                        elif key == '220':
                            current_channel['num_values'] = int(value)
                        elif key == '221':
                            current_channel['offset'] = int(value)
                        elif key == '222':
                            current_channel['block_offset'] = int(value)
                        elif key == '211':
                            current_channel['data_file'] = os.path.join(os.path.dirname(dat_file_path), value)
    except Exception as e:
        print(f"Failed to read or parse {dat_file_path}: {e}")
        return {}, None

    return channels, data_file_path


def read_data_file(data_file_path, channels):
    """
    Reads the data from a specified binary file and constructs a DataFrame based on the channel metadata.

    Parameters:
        data_file_path (str): Path to the binary data file.
        channels (dict): Dictionary containing channel definitions and metadata.

    Returns:
        pd.DataFrame: DataFrame populated with the structured data from the binary file.
    """
    data_types = {
        'REAL32': ('f', 4),
        'INT16': ('h', 2),
        'REAL64': ('d', 8)
    }

    try:
        total_channels = len(channels)
        data = np.empty((0, total_channels))

        with open(data_file_path, 'rb') as file:
            dtype_format = ''.join([data_types[info['dtype']][0] for info in channels.values()])
            record_size = sum([data_types[info['dtype']][1] for info in channels.values()])
            while True:
                record = file.read(record_size)
                if not record:
                    break
                unpacked_data = struct.unpack(dtype_format, record)
                data = np.vstack([data, unpacked_data])

        df = pd.DataFrame(data, columns=[ch['name'] for ch in channels.values()])

    except FileNotFoundError:
        print(f"Data file {data_file_path} not found.")
        return pd.DataFrame()
    except struct.error as e:
        print(f"Error unpacking data from {data_file_path}: {e}")
        return pd.DataFrame()

    return df


def dat_to_df(dat_file_path):
    """
    Converts data from a .dat and associated binary file to a DataFrame.

    Parameters:
        dat_file_path (str): The path to the .dat file.

    Returns:
        pd.DataFrame: DataFrame containing the structured data or an empty DataFrame on failure.
    """
    try:
        dataframe = pd.DataFrame()
        channels, data_file_path = read_dat_file(dat_file_path)
        if data_file_path:
            dataframe = read_data_file(data_file_path, channels)
        return dataframe
    except Exception as e:
        print(f"An error occurred while converting data to DataFrame: {e}")
        return pd.DataFrame()  # Return an empty DataFrame on error


def dat_to_parquet(dat_file_path, parquet_file_name):
    """
    Converts data from a .dat file to a Parquet file.

    Parameters:
        dat_file_path (str): The path to the .dat file.
        parquet_file_name (str): The path where the Parquet file will be saved.
    """
    try:
        dataframe = dat_to_df(dat_file_path)
        if not dataframe.empty:
            dataframe.to_parquet(parquet_file_name)
            print(f"Data saved to {parquet_file_name}")
        else:
            print("No data available to save to Parquet.")
    except Exception as e:
        print(f"Failed to save data to Parquet: {e}")


def dat_to_csv(dat_file_path, csv_file_name):
    """
    Converts data from a .dat file to a CSV file.

    Parameters:
        dat_file_path (str): The path to the .dat file.
        csv_file_name (str): The path where the CSV file will be saved.
    """
    try:
        dataframe = dat_to_df(dat_file_path)
        if not dataframe.empty:
            dataframe.to_csv(csv_file_name, sep=';', index=False)
            print(f"Data saved to {csv_file_name}")
        else:
            print("No data available to save to CSV.")
    except Exception as e:
        print(f"Failed to save data to CSV: {e}")


def get_min_decimal_places(series):
    """Returns the minimum number of decimal places that can be used without causing duplicates."""
    unique_series = series.drop_duplicates()

    for decimals in range(11):
        rounded = unique_series.round(decimals)
        if not rounded.duplicated().any():
            return decimals
    return 10


def merge_dat_with_tdms(tdms_path, dat_paths, base_channel='UnixTime', fill_missing='nan'):
    """
    Merges data from TDMS and multiple DAT files into a single DataFrame.

    Parameters:
        tdms_path (str): The file path to the TDMS file.
        dat_paths (list): List of file paths to the DAT files.
        base_channel (str): The channel for merging data from DAT to TDMS.
        fill_missing (str): Specifies how to handle missing values: 'drop' or 'nan'.

    Returns:
        tuple: Contains merged DataFrame, Channel units, the root name, and waveform information.
    """
    try:
        tdms_file = TdmsFile.read(tdms_path)
        tdms_df = tdms_file.as_dataframe()

        # Adjust column names by removing quotes and paths
        tdms_df.columns = [col.split('/')[-1].replace("'", "").strip() for col in tdms_df.columns]
        tdms_channel_units = {
            channel.path.split('/')[-1].replace("'", "").strip(): channel.properties.get('unit_string', 'unknown')
            for group in tdms_file.groups() for channel in group.channels()}

        # Additional channel properties
        tdms_channel_properties = {
            channel.path.split('/')[-1].replace("'", "").strip(): channel.properties
            for group in tdms_file.groups() for channel in group.channels()}

        # Group properties
        tdms_group_properties = {group.name: group.properties for group in tdms_file.groups()}

        # Root properties
        tdms_root_properties = tdms_file.properties

        # Combine data from multiple DAT files
        combined_dat_df = pd.DataFrame()
        dat_channel_units = {}
        for dat_path in dat_paths:
            channels, _ = read_dat_file(dat_path)
            dat_df = dat_to_df(dat_path)
            combined_dat_df = pd.concat([combined_dat_df, dat_df], ignore_index=True)

            for channel in channels.values():
                dat_channel_units[channel['name']] = channel.get('unit', 'unknown')

        root_name = 'Measurement'
        for group in tdms_file.groups():
            root_name = group.name

        # Determine the maximum decimal places to avoid duplicates in dat_df
        max_decimals = get_min_decimal_places(combined_dat_df[base_channel])
        print(f"Rounding {base_channel} channel to {max_decimals} decimal places to avoid nans and duplicates.")

        # Round the base_channel to the determined decimal places
        tdms_df[base_channel] = tdms_df[base_channel].round(max_decimals)
        combined_dat_df[base_channel] = combined_dat_df[base_channel].round(max_decimals)

        dat_df = combined_dat_df[[col for col in combined_dat_df.columns if col not in tdms_df.columns or col == base_channel]]

        # Store waveform information
        waveforms = {}
        for group in tdms_file.groups():
            for channel in group.channels():
                if channel.properties.get('wf_increment', None) is not None:
                    waveforms['wf_start_time'] = channel.properties['wf_start_time']
                    waveforms['wf_increment'] = channel.properties['wf_increment']
                    break  # We only need to find one waveform channel

        merged_df = pd.merge(tdms_df, dat_df, on=base_channel, how='left')

        if fill_missing == 'drop':
            merged_df.dropna(inplace=True)
            new_first_value = merged_df[base_channel].iloc[0]
            if 'wf_start_time' in waveforms and 'wf_increment' in waveforms:
                # Find the number of rows dropped at the beginning
                dropped_rows_at_start = tdms_df[tdms_df[base_channel] < new_first_value].shape[0]
                # Adjust wf_start_time based on the new starting index after dropping rows
                delta_time = dropped_rows_at_start * waveforms['wf_increment']
                new_start_time = pd.to_datetime(waveforms['wf_start_time']) + pd.to_timedelta(delta_time, unit='s')
                waveforms['wf_start_time'] = new_start_time

        elif fill_missing == 'nan':
            merged_df.fillna(value=np.nan, inplace=True)

        return (merged_df, tdms_channel_units, dat_channel_units, root_name, waveforms, tdms_channel_properties,
                tdms_group_properties, tdms_root_properties)
    except Exception as e:
        print(f"Error merging TDMS and DAT files: {e}")
        return pd.DataFrame(), {}, {}, 'Measurement', {}, {}, {}, {}


def save_to_tdms(df, base_channel, tdms_channel_units, dat_channel_units, tdms_path_read, root_name, output_directory,
                 waveforms, tdms_channel_properties, tdms_group_properties, tdms_root_properties):
    """
    Saves the merged DataFrame to a new TDMS file with metadata.

    Parameters:
        df (pd.DataFrame): The DataFrame to save.
        base_channel (str): The channel for merging data from DAT to TDMS.
        tdms_channel_units (dict): Dictionary of units from TDMS channels.
        dat_channel_units (dict): Dictionary of units from DAT channels.
        tdms_path_read (str): The original TDMS file path.
        root_name (str): The root name for the TDMS file.
        output_directory (str): Directory to save the new TDMS file.
        waveforms (dict): Dictionary of waveform information.
        tdms_channel_properties (dict): Dictionary of additional channel properties.
        tdms_group_properties (dict): Dictionary of group properties.
        tdms_root_properties (dict): Dictionary of root properties.
    """
    try:
        os.makedirs(output_directory, exist_ok=True)
        tdms_path_write = os.path.join(output_directory, os.path.basename(tdms_path_read))
        root_object = RootObject(properties=tdms_root_properties)

        base_channel_index = df.columns.get_loc(base_channel)
        kanal_nr = int(tdms_channel_properties.get(base_channel, {}).get('Kanal_Nr', base_channel_index))

        with TdmsWriter(tdms_path_write) as tdms_writer:
            tdms_writer.write_segment([root_object])
            for group_name, group_properties in tdms_group_properties.items():
                group_object = GroupObject(root_name, properties=group_properties)
                tdms_writer.write_segment([root_object, group_object])
                for column in df.columns:
                    properties = {}

                    # Set properties in the desired order
                    if 'wf_start_time' in waveforms and 'wf_increment' in waveforms:
                        properties['wf_start_time'] = waveforms['wf_start_time']
                        properties['wf_increment'] = waveforms['wf_increment']

                    properties['wf_start_offset'] = tdms_channel_properties.get(base_channel,
                                                                                {}).get('wf_start_offset', '')
                    properties['wf_samples'] = tdms_channel_properties.get(base_channel, {}).get('wf_samples', '')
                    properties['NI_ChannelName'] = column

                    if column in tdms_channel_units:
                        properties['NI_UnitDescription'] = tdms_channel_units.get(column, '')
                        properties['unit_string'] = tdms_channel_units.get(column, '')
                    elif column in dat_channel_units:
                        properties['NI_UnitDescription'] = dat_channel_units.get(column, '')
                        properties['unit_string'] = dat_channel_units.get(column, '')

                    column_index = df.columns.get_loc(column)
                    if column_index > base_channel_index:
                        properties['Typ'] = tdms_channel_properties.get(base_channel, {}).get('Typ', '')
                        properties['AULA_Server'] = tdms_channel_properties.get(base_channel, {}).get('AULA_Server', '')
                        kanal_nr += 1
                        properties['Kanal_Nr'] = str(kanal_nr)
                        if column in tdms_channel_units:
                            properties['Einheit'] = tdms_channel_units.get(column, '')
                        elif column in dat_channel_units:
                            properties['Einheit'] = dat_channel_units.get(column, '')
                    elif column == base_channel:
                        properties['Kanal_Nr'] = tdms_channel_properties.get(base_channel, {}).get('Kanal_Nr', '')
                        if column in tdms_channel_units:
                            properties['Einheit'] = tdms_channel_units.get(column, '')
                        elif column in dat_channel_units:
                            properties['Einheit'] = dat_channel_units.get(column, '')

                    # Add any remaining original properties
                    if column in tdms_channel_properties:
                        for key, value in tdms_channel_properties[column].items():
                            if key not in properties:
                                properties[key] = value

                    channel = ChannelObject(group_name, column, df[column].values, properties=properties)
                    tdms_writer.write_segment([root_object, group_object, channel])
            print(f"Data successfully saved to TDMS file: {tdms_path_write}")
    except Exception as e:
        print(f"Error saving data to TDMS file: {e}")


def create_merged_tdms(tdms_path, dat_paths, output_directory, base_channel='UnixTime', fill_missing='drop'):
    """
    Creates a merged TDMS file from TDMS and DAT sources.

    Parameters:
        tdms_path (str): The file path to the TDMS file.
        dat_paths (list): List of file paths to the DAT files.
        output_directory (str): The directory to save the merged TDMS file.
        base_channel (str): The channel for merging data from DAT to TDMS.
        fill_missing (str): Specifies how to handle missing values in the merge.
    """
    (result_df, tdms_channel_units, dat_channel_units, root_name, waveforms, tdms_channel_properties,
     tdms_group_properties, tdms_root_properties) = merge_dat_with_tdms(
        tdms_path, dat_paths, base_channel=base_channel, fill_missing=fill_missing)
    save_to_tdms(result_df, base_channel, tdms_channel_units, dat_channel_units, tdms_path, root_name, output_directory,
                 waveforms, tdms_channel_properties, tdms_group_properties, tdms_root_properties)


def tdms_to_parquet(tdms_path, parquet_file_name):
    try:
        tdms_file = TdmsFile.read(tdms_path)
        dataframe = tdms_file.as_dataframe()
        if not dataframe.empty:
            dataframe.to_parquet(parquet_file_name)
            print(f"Data saved to {parquet_file_name}")
        else:
            print("No data available to save to Parquet.")
    except Exception as e:
        print(f"Failed to save data to Parquet: {e}")


def tdms_metadata_to_csv(tdms_path):
    """
    Extracts and saves metadata from a TDMS file to a CSV file.

    Parameters:
        tdms_path (str): The path to the TDMS file.

    The function reads the specified TDMS file, extracts metadata from all channels across all groups,
    and saves this information into a CSV file named after the original TDMS file with a '_metadata' suffix.
    """
    try:
        # Read the TDMS file
        tdms_file = TdmsFile.read(tdms_path)

        # Extract metadata from each channel
        metadata = []
        for group in tdms_file.groups():
            for channel in group.channels():
                channel_metadata = {
                    "Group": group.name,
                    "Channel": channel.name,
                    "Unit": channel.properties.get("unit_string", ""),
                    "wf_start_time": channel.properties.get("wf_start_time", ""),
                    "wf_increment": channel.properties.get("wf_increment", "")
                }
                # Include additional channel properties
                for key, value in channel.properties.items():
                    if key not in channel_metadata:
                        channel_metadata[key] = value
                metadata.append(channel_metadata)

        # Include group properties
        for group in tdms_file.groups():
            group_metadata = {
                "Group": group.name,
                "Channel": "",
                "Unit": "",
                "wf_start_time": "",
                "wf_increment": ""
            }
            for key, value in group.properties.items():
                group_metadata[key] = value
            metadata.append(group_metadata)

        # Include root properties
        root_metadata = {
            "Group": "Root",
            "Channel": "",
            "Unit": "",
            "wf_start_time": "",
            "wf_increment": ""
        }
        for key, value in tdms_file.properties.items():
            root_metadata[key] = value
        metadata.append(root_metadata)

        # Convert the metadata into a DataFrame
        metadata_df = pd.DataFrame(metadata)

        # Determine the output file path
        output_file_path = os.path.splitext(tdms_path)[0] + "_metadata.csv"

        # Save the DataFrame to CSV
        metadata_df.to_csv(output_file_path, sep=';', index=False)
        print(f"Metadata saved successfully to: {output_file_path}")
    except Exception as e:
        print(f"An error occurred while extracting metadata from the TDMS file: {e}")
