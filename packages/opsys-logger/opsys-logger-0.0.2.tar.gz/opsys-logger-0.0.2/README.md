# README #

This README would normally document whatever steps are necessary to get your application up and running.

### What is this repository for? ###

* This repository is a part of opsys automation infrastructure
* This repository contains different print formatting implementations for automation purposes 

### How do I get set up? ###

* pip install opsys-logger

### Unit Testing

* python -m unittest -v

### Usage Example
```
from opsys_logger.print_formatter import PrintFormatter

print_format = PrintFormatter()
print_format.print_error_message("This is an ERROR!!!")
```