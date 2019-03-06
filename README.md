# safeoutput

Safeoutput.open returns a file handle like object which can use used to write data to disk.
It is meant to be used with python's with syntax.

If an exception is thrown, safeoutput automatically deletes the file. This ensures partially rendered output is not left sitting around.

If your handle leaves scope, without an exception being thrown, the file is atomically flipped into the desired location.

Safeoutput uses temporary files to store writes, so your file contents do not have to fit in memory.

## Usage

### Python

```python
import sys
import safeoutput

def calc(line):
  return line+1

input_fname = sys.argv[1]
output_fname = sys.argv[2]

with open(input_fname, 'r') as input:
  with safeoutput.open(output_fname) as output:
    for line in input.xreadlines():
      output.write(str(calc(int(line))))
```

### Command line

```bash
$ safeoutput
usage: safeoutput [-h] [--binary] FILE
```

The example below ensures bar is not written until the pipe is closed.

```bash
(sleep 10; echo foo ${RANDOM} ) | \
  safeoutput --binary bar

cat bar
```
