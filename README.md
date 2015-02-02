# safeoutput
Python library for writing program output atomically.

Tool to facilitate console script output redirection. 
When scripts run, often they have an output file option. 
If no output option is specified, its common to write to stdout. 

Its common to use tempfiles as output, and then rename the tempfile to the output name as the last step of the 
program so that the flip of output is atomic and partial/truncated/corrupt output is not confused as successful output. 

This is especially true when dealing with make, as exiting with error will stop make, but subsequent runs will assume 
that partial output files left in the workspace are complete.

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
      output.write(calc(line))
```
