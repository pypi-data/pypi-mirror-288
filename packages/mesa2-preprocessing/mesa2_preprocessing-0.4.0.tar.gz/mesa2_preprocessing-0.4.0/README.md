# MESA2.0 Preprocessing Tool

This package provides a set of tools designed for pre-processing MESA2.0 measurement data. It includes functionality to read, merge, and process measurement data efficiently.

## Features
- Read data from `.dat` and associated binary files.
- Merge data from different sources like TDMS and DAT files.
- Export processed data to various formats such as CSV and Parquet.
- Handle metadata and unit conversions.

## Installation
Install `mesa2_preprocessing` using pip:

```bash
pip install mesa2_preprocessing
```

## Usage
Here is a simple example of how to use the package:

```python
from mesa2_preprocessing import dat_to_df, create_merged_tdms

# Convert a DAT file to a DataFrame
df = dat_to_df('path_to_your_dat_file.dat')

# Create a merged TDMS file from DAT and TDMS sources
create_merged_tdms('path_to_your_tdms_file.tdms', 'path_to_your_dat_file.dat', 'output_directory')
```
## Dependencies

- Python >= 3.8
- pandas
- pyarrow
- fastparquet
- numpy
- nptdms

## License
This project is licensed under the MIT License - see the LICENSE file for details.