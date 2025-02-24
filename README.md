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
2. Save current environment:
```bash
myenvs save <env_name>
```
3. Activate environment:
```bash
myenvs activate <env_name>
```
4. Switch to working dir of environment:
```bash
myenvs workon <env_name>
```
5. List saved environments:
```bash
myenvs list
```
6. Remove saved environment:
```bash
myenvs remove <env_name>
```
