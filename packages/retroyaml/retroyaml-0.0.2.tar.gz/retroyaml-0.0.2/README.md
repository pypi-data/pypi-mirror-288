# reyaml

## Description
Small utility class to ease yaml configuration in python3.

## Requirements
Currently only requires `pyyaml`. 

To install the requirements:
`pip3 install -r requirements.txt`

## Example
### config.yaml
```
hello: world
this:
  is:
    - a
    - test
```
### example.py
```
from retroyaml.yamlConf import yamlConf

config = yamlConf('config.yaml')

print(config.hello)
```
> world
```
print(len(config.this.is))
```
> 2