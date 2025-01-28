# MtG_game_log
Inspired by EDHRECast's game tracking.

## setup instructions

1. Make sure you have the following environment variables set:
```
MtG_log_MYSQL_USER  # your MySQL username
MtG_log_MYSQL_PWD   # your MySQL password
MtG_log_MYSQL_HOST  # your MySQL host
MtG_log_MYSQL_DB    # must be "MtG_log"
```
2. Run the following command: `mysql < ${path_to_MtG_game_log_repo}/data/MtG_log_db.sql`. This sets up the database.
3. Populate the database (I want to make a script that edits the .sql to do this automatically using the data from my database)

### api/
Contains API stuff.

### data/
Contains stuff to do with the database.

### models/
Converts SQL tables to python classes.

### templates/
Contains html stuff.

### static/
Contains css stuff.
