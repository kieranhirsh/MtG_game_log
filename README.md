# MtG_game_log
Inspired by EDHRECast's game tracking.

## setup instructions

<ol>
<li>Make sure you have the following environment variables set:
```
MtG_log_MYSQL_USER  # your MySQL username
MtG_log_MYSQL_PWD   # your MySQL password
MtG_log_MYSQL_HOST  # your MySQL host
MtG_log_MYSQL_DB    # must be "MtG_log"
```
<li>Run the following command to set up the database: `mysql < ${path_to_MtG_game_log_repo}/data/MtG_log_db.sql`
<li>Populate the database (I want to make a script that edits the .sql to do this automatically using the data from my database)
</ol>

### data/
Contains stuff to do with the database.
