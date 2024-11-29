# pylint: disable=C0114
# Imports
import base64
import os
import secrets
import sqlite3
import sys
import dotenv
import pyescrypt
import mvvm
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
if not mvvm.Identification.is_identification_valid(sys.argv[2]):
    print("You need to specify a valid identification.")
    sys.exit(4)
# Load environment variables and connect to database
dotenv.load_dotenv()
connection = sqlite3.connect(os.getenv("DATABASE_FILENAME"))
cursor = connection.cursor()
# Begin hashing and salting the password
hasher = pyescrypt.Yescrypt(mode=pyescrypt.Mode.RAW)
password = bytes(sys.argv[3], "utf-8")
salt = secrets.token_bytes(32)
hashed_password = hasher.digest(password, salt)
# Execute database query and commit changes to database
cursor.execute("INSERT INTO users VALUES (?, ?, ?, ?);", (sys.argv[1], mvvm.Identification(sys.argv[2]).
                                                          get_raw_identification(), base64.b64encode(hashed_password).
                                                          decode(), base64.b64encode(salt).decode()))
connection.commit()
