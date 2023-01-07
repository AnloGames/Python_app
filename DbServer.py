import jose.exceptions
from fastapi import FastAPI
from fastapi import Body, Header, Depends
from fastapi.exceptions import HTTPException
from fastapi.responses import HTMLResponse
import uvicorn
from jose import jwt
import config
from Utils import DbAction, run_code, execute_action
from TaskChecker import Task


app = FastAPI()


def get_user(authorization: str = Header(...)):
    try:
        user_id = jwt.decode(authorization, config.Secret, algorithms=['HS256'])['id']
    except jose.exceptions.JWTError:
        raise HTTPException(
            status_code=400,
            detail="Неверный токен"
        )
    user = execute_action('''
        select * from users where id = ?
    ''', (user_id,), DbAction.fetchone)
    return user


def send_html(file_name: str):
    with open(f"Html/{file_name}.html") as f:
        return HTMLResponse(f.read())


@app.on_event("startup")
def create_db():
    execute_action('''create table if not exists users (
        id integer primary key,
        username text not null,
        password text not null
    );
    ''', (), DbAction.none)
    execute_action('''create table if not exists tasks (
        id integer primary key,
        name text not null,
        description text,
        output text not null
    );
    ''', (), DbAction.none)


@app.get("/")
def hello():
    return send_html("index")


@app.post("/api/ping")
def ping(user: list = Depends(get_user)):
    return {
        'response': 'Pong',
        'username': user[1]
    }


@app.get("/login")
def login():
    return send_html("login")


@app.post("/api/login")
def login(username: str = Body(...), password: str = Body(...)):
    user = execute_action('''
        select * from users where username = ? and password = ?
    ''', (username, password), DbAction.fetchone)
    if user is None:
        return {'error': "Пользователь не найден"}
    token = jwt.encode({'id': user[0]}, config.Secret, algorithm="HS256")
    return {'token': token}


@app.get("/signUp")
def sign_up():
    return send_html("signUp")


@app.post("/api/signUp")
def sign_up(username: str = Body(...), password: str = Body(...)):
    if execute_action('''
        select * from users where username = ?
    ''', (username,), DbAction.fetchone) is not None:
        raise HTTPException(
            status_code=400,
            detail="Пользователь уже существует"
        )

    execute_action('''
        insert into users (username, password) values (?, ?)
    ''', (username, password), DbAction.commit)
    return {"message": "Добро пожаловать"}


@app.post("/api/execute")
def execute(user: list = Depends(get_user), code: str = Body(..., embed=True)):
    stdout = run_code(code)
    return {
        'result': stdout
    }


@app.get("/api/tasks")
def get_tasks(user: list = Depends(get_user)):
    return Task.all()


@app.post("/api/send_task")
def send_task(user: list = Depends(get_user), code: str = Body(..., embed=True), task_id: int = Body(..., embed=True)) -> bool:
    task = Task.get(task_id)
    return task.check_solution(code)


uvicorn.run(app)
