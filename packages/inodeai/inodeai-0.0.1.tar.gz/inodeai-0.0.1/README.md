
This package includes helper scripts for interfacing your machine learning code with the Inode-ai.com  containerization code.



## How to implement

```
from Inode import inodeai

# transform input data against your  model (or whatever you want)
# If an error occured please thwor an error message

def transform_data (dataPath,outPath):
    
    # Read data  from dataPath
    # Transform Data via model
    # Write data out to outPath
    # Return None if everything is ok.
    # return an error msg if any error ocuured .


please intialize your model or other thing before using wait_for_request

inodeai.wait_for_requests(process_data)

```



run via command line arguments

python test.py serve input.csv output.csv

usage: test.py [-h] {run} ...

options:
  -h, --help  show this help message and exit

subcommands:
  {run}       commands to choose from
    run       run this model once from the command line




