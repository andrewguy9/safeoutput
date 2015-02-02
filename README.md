# safeoutput

Safeoutput.open returns a file handle like object which can use used to write data to disk.
It is meant to be used with python's with syntax. If an exception is thrown, safeoutput automatically deletes the file so that your partially rendered output is not left around. If your handle leaves scope, without an exception being thrown, the file is atomically flipped into the desired location.

safeoutput uses temporary files to store writes, so your file contents do not have to fit in memory.

# Usage:

```
import sys
import safeoutput

def calc(line):
  return line+1
  
input_fname = sys.argv[0]
output_fname = sys.argv[1]

with open(input_fname, 'r') as input:
  with safeoutput.safe_output(output_fname, 'r') as output:
    for line in input.xreadlines():
      output.write(calc(int(line)))
```
