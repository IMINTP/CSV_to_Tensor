# CSV_to_Tensor
Deeplabcut에서 label 한 csv file을 co-tracker의 tensor로 바꿔주는 python file 입니다.

t
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
