# CSV to Tensor Converter v0.1

A simple GUI application that converts CSV files containing coordinate data to PyTorch tensors.
(Deeplabcut, co-tracker와 연계하기 위함)


## Features

- GUI interface for easy file selection
- Converts CSV files with 10 coordinate points (r00-r09) to PyTorch tensors
- Displays formatted tensor code ready for use
- Supports CUDA if available
- Scrollable output display

## Installation

1. Clone the repository:
```bash
git clone https://github.com/your-username/csv-to-tensor.git
cd csv-to-tensor
```

2. Install the required packages:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the application:
```bash
python csv_to_tensor.py
```

2. Click "Select CSV File" and choose your CSV file
3. The converted tensor code will be displayed in the GUI

## CSV Format

The expected CSV format:

The CSV file should contain four rows:
1. Header row: Contains column identifiers
2. Body parts row: Contains repeated point identifiers (r00-r09)
3. Coordinate type row: Specifies 'x' and 'y' for each point
4. Data row: Contains the actual coordinate values, starting with metadata (labeled-data, filename) followed by x,y coordinates for each point

Example structure:
```
[header row]    : column names and identifiers
[body parts]    : point identifiers (r00-r09 repeated pairs)
[coord types]   : x,y labels for each point
[data]         : labeled-data, filename, frame_number, x1, y1, x2, y2, ..., x10, y10
```

The program expects exactly 10 points (r00 through r09), each with x and y coordinates.

## Output Format

The program generates tensor code in the following format:
```python
queries = torch.tensor([
    [frame_num, x1, y1],
    [frame_num, x2, y2],
    ...
    [frame_num, x10, y10]
    ])
if torch.cuda.is_available():
    queries = queries.cuda()
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
