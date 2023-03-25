Java Development Kit Manager for Windows and Linux.<br>
The goal with JDKMAN is to have a reliable way to switch between JDKs similar to nvm for Node.js

# Installation

## Requirements

- Python 3.10
- Make (Optional)
 

## 1. Clone repository
```bash
$ git clone https://github.com/michaelbui99/JDKMAN.git && cd ./JDKMAN
```
## 2. Install JDKMAN 
JDKMAN can be installed with pip
```bash
$ pip install  .
```
or with Make
```bash
$ make install
```


# Usage
List all available commands by using the --help flag
```bash
$ jdkman --help
```

See usage for a command by running
```bash
$ jdkman <COMMAND> --help #e.g. jdkman install --help
```

## Examples
### Installing Azul Zulu JDK 
```bash
$ jdkman install --distribtuion Zulu 17.40.19
```