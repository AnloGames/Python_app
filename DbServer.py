from fastapi import FastAPI
from fastapi import Body
from fastapi.responses import PlainTextResponse
import uvicorn
from enum import Enum, auto
import sqlite3

app = FastAPI()


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


@app.on_event("startup")
def create_db():
    execute_action('''create table if not exists users (
        id integer primary key,
        username text not null,
        password text not null
    );
    ''', (), DbAction.none)


@app.get("/")
def hello():
    return PlainTextResponse("Hello world")


@app.get("/login")
def login():
    return PlainTextResponse("Login")


@app.post("/login")
def login(username: str = Body(...), password: str = Body(...)):
    user = execute_action('''
        select * from users where username = ? and password = ?
    ''', (username, password), DbAction.fetchone)
    return user


@app.post("/signUp")
def sign_up(username: str = Body(...), password: str = Body(...)):
    if execute_action('''
        select * from users where username = ?
    ''', (username,), DbAction.fetchone) is not None:
        return PlainTextResponse("Этот пользователь уже зарегистрирован")

    execute_action('''
        insert into users (username, password) values (?, ?)
    ''', (username, password), DbAction.commit)
    return PlainTextResponse("Добро пожаловать")


uvicorn.run(app)
