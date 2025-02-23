# MtG_game_log/data

Contains stuff to do with the database.

## db_storage.py

Defines a class to manage database storage.

## MtG_log_db.sql

MySQL script that creates the database.<br>
The script can be run with the following command: `mysql < ${path_to_MtG_game_log_repo}/data/MtG_log_db.sql`

## MtG_log_db_full.sql

An old version of the database.
I tried to add all tables at once and realised that that's a terrible idea.
It is being kept around as a reference though.

## Useful commands

To dump the database to an sql script<br>
`mysqldump -u username -p databasename > output_file.sql`
