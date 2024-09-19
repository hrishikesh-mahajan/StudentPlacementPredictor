import sqlite3

import click
from flask import current_app
from flask import g


def get_db_admin():
    """Connect to the application's configured database. The connection
    is unique for each request and will be reused if this is called
    again.
    """
    if "db_admin" not in g:
        g.db_admin = sqlite3.connect(
            current_app.config["DATABASE_ADMIN"], detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db_admin.row_factory = sqlite3.Row

    return g.db_admin


def close_db_admin(e=None):
    """If this request connected to the database, close the
    connection.
    """
    db_admin = g.pop("db_admin", None)

    if db_admin is not None:
        db_admin.close()


def init_db_admin():
    """Clear existing data and create new tables."""
    db_admin = get_db_admin()

    with current_app.open_resource("schema.sql") as f:
        db_admin.executescript(f.read().decode("utf8"))


@click.command("init-db-admin")
def init_db_command_admin():
    """Clear existing data and create new tables."""
    init_db_admin()
    click.echo("Initialized the database.")


def init_app_admin(app):
    """Register database functions with the Flask app. This is called by
    the application factory.
    """
    app.teardown_appcontext(close_db_admin)
    app.cli.add_command(init_db_command_admin)
