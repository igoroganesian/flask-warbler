# Warbler - README

## Overview

Warbler is a social microblogging platform; users have access to standard functionality such as following each other, liking "warbles" (ie tweets), and viewing warbles from followed users on their homepage. 

## Dependencies

Requires:
- venv
- Python3
- PostgreSQL

## Setup

1. Create a Python virtual environment:
```
$ python3 -m venv venv
$ source venv/bin/activate
```

2. Install the required dependencies:
```
(venv) $ pip install -r requirements.txt
```

3. Set up the database:
```
(venv) $ psql
=# CREATE DATABASE warbler;
=# (ctrl-d/cmd-d to exit)
(venv) $ python seed.py
```

4. Create an `.env` file to hold the configuration:
```
.env»
SECRET_KEY=secret
DATABASE_URL=postgresql:///warbler
```

5. Start the server:
```
(venv) $ flask run
```
**Note** If you encounter an "address already in use" error, try running on port 5001 instead via:
`flask run -p 5001`

Feel free to contact the project owner with any questions or feedback.
