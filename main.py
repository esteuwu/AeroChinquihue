import dotenv
import mvvm.model
import os
import pathlib

dotenv.load_dotenv()
DATABASE_FILENAME = os.getenv("DATABASE_FILENAME")

if not pathlib.Path(DATABASE_FILENAME).exists():
    raise FileNotFoundError("Database does not exist")
database = mvvm.model.Model(DATABASE_FILENAME)
print(database.__str__())
