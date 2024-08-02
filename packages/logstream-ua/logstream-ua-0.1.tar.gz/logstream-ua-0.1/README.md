# logstream

A package that allows you to create simple records of the results of your application\'s functionality, read them, and clean the file of all obsolete records when not needed.
Developed by Bohdan Terskow (c) 2024

## Examples of How To Use

CLI: pip install logstream-ua

```python
from logstream import LogStream

logfile_dir = './logs.txt'
logstream = LogStream(logfile_dir)

logstream(description='Test', level=3)
# description - record description
# level - level of record (5 - debug, 4 - info, 3 - warning, 2 - error, 1 - fatal)

# Other Code

read_logs = logstream.read()
print(read_logs) # show text into logfile

logstream.clear() # clear all file from records
```