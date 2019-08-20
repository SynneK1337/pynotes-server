# PyNotes Server
Simple hosting solutions for your notes

## Future plans:
* Finish curses-based text interface [client](https://github.com/synnek1337/pynotes-client)
* Prepare a Dockerfile for easier hosting
* Write documentation for API

## Usage:
* Set up MySQL: edit ```create_tables.py``` and **execute**
* Install dependencies: ```pip install -r requirements.txt```
* Run: ```python src/main.py```

## Dependencies:
* [MySQL](https://mysql.com)
* [mysql-connector](https://pypi.org/project/mysql-connector/)
* [aiohttp](https://aiohttp.readthedocs.io/en/stable/)