# pylint: disable=C0114
# Imports
import base64
import os
import secrets
import sqlite3
import sys
import dotenv
import pyescrypt
from aerochinquihue import Identification
# Condition checks
if len(sys.argv) < 2:
    print("You need to specify a name.")
    sys.exit(1)
if len(sys.argv) < 3:
    print("You need to specify an identification.")
    sys.exit(2)
if len(sys.argv) < 4:
    print("You need to specify a password.")
    sys.exit(3)
try:
    identification = Identification(sys.argv[2])
except ValueError:
    print("You need to specify a valid identification.")
    sys.exit(4)
# Load environment variables and connect to database
dotenv.load_dotenv()
connection = sqlite3.connect(os.getenv("DATABASE_FILENAME"))
cursor = connection.cursor()
# Hash the password
hasher = pyescrypt.Yescrypt(mode=pyescrypt.Mode.RAW)
salt = secrets.token_bytes(32)
hashed_password = hasher.digest(bytes(sys.argv[3], "utf-8"), salt)
# Update database and commit changes
cursor.execute("INSERT INTO users VALUES (?, ?, ?, ?);", (identification.get_raw_identification(), sys.argv[1], base64.
                                                          b64encode(hashed_password).decode(), base64.b64encode(salt).
                                                          decode()))
connection.commit()
