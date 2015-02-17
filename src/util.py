import json
import os
import pprint

def write_json(path, data):
    output = open(path, 'w')
    output.write(json.dumps(data, indent=4))
    output.close

def read_json(path):
    file = open(os.path.abspath(path), 'r')
    data = json.load(file)
    file.close
    return data

def pp(data):
  pp = pprint.PrettyPrinter(indent=4)
  pp.pprint(data)