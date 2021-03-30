import sqlite3
from tkinter import filedialog
import os

conn = sqlite3.connect('user_data.db')
c = conn.cursor()
c.execute("""CREATE TABLE user  (
    uid integer NOT NULL PRIMARY KEY,
    name string,
    username string,
    pwd string
)""")

c.execute("""CREATE TABLE vault_config  (
    uid integer NOT NULL PRIMARY KEY,
    path string
)""")

c.execute("""CREATE TABLE vault_data  (
    fileid integer NOT NULL PRIMARY KEY,
    uid integer NOT NULL,
    state string,
    algo string,
    filename string,
    filesize integer,
    path string,
    filetype string
)""")

c.execute("""CREATE TABLE vault_path  (
    path string
)""")

path = filedialog.askdirectory()
c.execute("INSERT INTO vault_path VALUES (:path)",{
            'path' : path
        })
# path=os.getcwd()
os.system('pip install pillow')
os.system('pip install bcrypt')


conn.commit()
conn.close()