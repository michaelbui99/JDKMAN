Java Development Kit Manager for Windows and Linux.<br>
The goal with JDKMAN is to have a reliable way to switch between JDKs similar to nvm for Node.js

# Installation

## Requirements

- Python 3.10
- pip
- Make (Optional)
 

## 1. Clone repository
```bash
$ git clone https://github.com/michaelbui99/JDKMAN.git && cd ./JDKMAN
```
## 2. Install JDKMAN 
JDKMAN can be installed in 2 ways:

Using pip
```bash
$ pip install  .
```

Using Make
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

### Configuration
All distributions will be installed at <em><JDKMAN_INSTALLATION_PATH>/distributions<em>

JDKMAN can be configured by using the configure command
```bash
$ jdkman configure
```