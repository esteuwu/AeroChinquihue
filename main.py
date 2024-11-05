from Database import Database
import pathlib

if not pathlib.Path("database.db").exists():
    raise FileNotFoundError("Database does not exist")
database = Database("database.db")
print(database.query())
database.bye()
