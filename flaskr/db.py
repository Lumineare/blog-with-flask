import sqlite3
from datetime import datetime

import click
from flask import current_app, g

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()
# The get_db function returns a database connection, which is used to execute the commands read from the file. close_db checks if a connection was created by checking if g.db was set. If the connection exists, it is closed. Further, the close_db function is registered with the app instance for cleanup when the app context is popped.

def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

# The init_db function initializes the database. The open_resource() method of the current_app object opens a file relative to the flaskr package, which is useful since you won’t necessarily know where that location is when deploying the application later.
# The schema.sql file is a file that contains the SQL commands to create the tables of the database. The file is read and executed in the database connection.
# You can use the sqlite3 command line tool to create a new database using this schema file. Run sqlite3 /path/to/flaskr.sqlite < schema.sql in a terminal to create the database.
# You can also use the sqlite3 command line tool to interact with the database. Run sqlite3 /path/to/flaskr.sqlite and then run SQL commands to insert, update, delete, and select data. For example, to select all rows from the user table, you can run SELECT * FROM user;.
# The sqlite3 command line tool is useful for debugging and testing. You can run commands to verify that the schema is correct and that the database is set up properly. You can also run commands to insert data and then select it to verify that the application is working as expected.
 
@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')
# The init_db_command function defines a command line command called init-db that calls the init_db function and outputs a success message to the command line. The command can be called with flask init-db.

sqlite3.register_adapter(
    "timestamp", lambda v: datetime.fromisoformat(v.decocode ())
)

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)