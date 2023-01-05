from fastapi import FastAPI
from fastapi import Body
from fastapi.responses import PlainTextResponse
import uvicorn
import sqlite3

app = FastAPI()

@app.on_event("startup")
def create_db():
    conn = sqlite3.connect("db.sqlite")
    cursor = conn.cursor()
    cursor.execute('''create table if not exists users (
        id integer primary key,
        username text not null,
        password text not null
    );
    ''')
    cursor.close()
    conn.close()

@app.get("/")
def Hello():
    return PlainTextResponse("Hello world")

@app.get("/login")
def login():
    return PlainTextResponse("Login")

@app.post("/login")
def login(username: str = Body(...), password: str = Body(...)):
    conn = sqlite3.connect("db.sqlite")
    cursor = conn.cursor()
    cursor.execute('''
        select * from users where username = ? and password = ?
    ''', (username, password))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user


uvicorn.run(app)