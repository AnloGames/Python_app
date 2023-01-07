import os
import random
import string
import subprocess
from enum import Enum, auto
import sqlite3

class DbAction(Enum):
    fetchone = auto()
    fetchall = auto()
    commit = auto()
    none = auto()


def execute_action(query, args, action):
    conn = sqlite3.connect("db.sqlite")
    cursor = conn.cursor()
    cursor.execute(query, args)
    result = None
    if action == DbAction.fetchone:
        result = cursor.fetchone()
    elif action == DbAction.fetchall:
        result = cursor.fetchall()
    elif action == DbAction.commit:
        conn.commit()
    cursor.close()
    conn.close()
    return result


def run_code(code: str):
    filename = "".join(random.choices(string.ascii_letters, k=10))
    filename = f"codes/{filename}"
    with open(filename, "w") as f:
        f.write(code)
    process = subprocess.Popen(['python', filename], stdout=subprocess.PIPE)
    process.wait()
    stdout = process.stdout.read()
    os.remove(filename)
    print(stdout)