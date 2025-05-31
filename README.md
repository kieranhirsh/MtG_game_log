# MtG_game_log
Inspired by EDHRECast's game tracking (episodes 298 and 345).

## setup instructions
1. Make sure you have python installed on your machine.
2. `pip install -r requirements.txt` to install the required packages.
3. Make sure you have the following environment variables set:
```
MtG_log_MYSQL_USER  # your MySQL username
MtG_log_MYSQL_PWD   # your MySQL password
MtG_log_MYSQL_HOST  # your MySQL host
MtG_log_MYSQL_DB    # must be "MtG_log"
```
4. `mysql < ${path_to_MtG_game_log_repo}/data/MtG_log_db.sql` to create the database and populate it with some data to get you started.
5. `python app.py` to start the app.
6. Head to `http://127.0.0.1:5000` in your favourite browser.
7. Have fun!

### [api/](https://github.com/kieranhirsh/MtG_game_log/tree/main/api/v1)
Contains API stuff.

### [crud/](https://github.com/kieranhirsh/MtG_game_log/tree/main/crud)
Contains all the functions related to creating, reading, updating, and deleting data.

### [data/](https://github.com/kieranhirsh/MtG_game_log/tree/main/data)
Contains stuff to do with the database.

### [data/](https://github.com/kieranhirsh/MtG_game_log/tree/main/errors)
Contains functions to make error handling less ugly.

### [graphs/](https://github.com/kieranhirsh/MtG_game_log/tree/main/graphs)
Contains functions that plot graphs.

### [models/](https://github.com/kieranhirsh/MtG_game_log/tree/main/models)
Converts SQL tables to python classes.

### [static/](https://github.com/kieranhirsh/MtG_game_log/tree/main/static)
Contains css, javascript, and other front end stuff.

### [templates/](https://github.com/kieranhirsh/MtG_game_log/tree/main/templates)
Contains html stuff.

### [templates/](https://github.com/kieranhirsh/MtG_game_log/tree/main/utils)
Contains utility functions.

### [validation/](https://github.com/kieranhirsh/MtG_game_log/tree/main/validation)
Any time a piece of data is created or edited, they must pass the validators stored here.
