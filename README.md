# Project Title

A *simple* command-line with GUI option for *r*emote *access* via SSH/VNC.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Installing

Get the relevant module via pip, and install Paramiko and PyQT5 as well.

```

pip install simpler-access
pip install paramiko
pip install pyqt5

```

### Using the simple remote access Client

Use the *-l* (list) flag will list details of all machines recorded.

```

python3 -m simpler_access -l

```

Use the *-a [xml]* (add [xml]) flag to add a new machine, provide the path to your xml as a parameter if you wish to import a machine instead.

```

python3 -m simpler_access -a
#
#Adding a machine
#----------------------
#Machine Name:
#

python3 -m simpler_access -a /some/path/to/file.xml

``` 

Use the *-d [id]* (delete [id]) flag with the id parameter of the machine to delete it from the list.

```

python3 -m simpler_access -d 2
#
#Deleting the following connection:
#----------------------------------------
#ID#2 - machine_name@123.456.789.012
#Are you sure you wish to delete? (y/n): 

``` 

Use the *-c [id]* (connect [id]) flag to connect to a machine in the list, you can provide the id as a parameter to connect to it immediately.

```

python3 -m simpler_access -c
#
#Id       Machine        Host
#================================
#1        ec2-inst       123.2...
#

python3 -m simpler_access -c 1

```

Use the *-g* (GUI) flag to run the program in the GUI mode.

```

python3 -m simpler_access -g

```


## Built With

* [Paramiko](http://www.paramiko.org/)- Python implementation of SSHv2
* [PyQT5](https://www.riverbankcomputing.com/static/Docs/PyQt5/) - Qt application framework used for GUI development

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
