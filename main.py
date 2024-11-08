import Database
import dotenv
import os
import pathlib

dotenv.load_dotenv()
DATABASE_FILENAME = os.getenv("DATABASE_FILENAME")

if not pathlib.Path(DATABASE_FILENAME).exists():
    raise FileNotFoundError("Database does not exist")
database = Database.Database(DATABASE_FILENAME)
print(database.__str__())
database.bye()
