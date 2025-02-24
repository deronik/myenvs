# MyENVs
Project to store my environment configurations and switch between them easily.
This project do not woried about how you setup your environment, it just save the current environment and switch between them.

## How to use
1. Install package:
```bash
pip install myenvs
# or develop mode
pip install -e .
```
1. Save current environment:
```bash
myenvs save <env_name>
```
2. Activate environment:
```bash
# This will activate the environment and set the working directory to the saved one
# we should use eval to set the environment variables in the current shell
eval $(myenvs activate <env_name>)
```
3. List saved environments:
```bash
myenvs list
```
4. Remove saved environment:
```bash
myenvs remove <env_name>
```
