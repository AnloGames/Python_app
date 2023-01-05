from fastapi import FastAPI
from fastapi import Body
from fastapi.responses import PlainTextResponse
import uvicorn

app = FastAPI()

class Note:
    note_id: int
    name: str
    content: str

    def __init__(self, note_id, name, content):
        self.note_id = note_id
        self.name = name
        self.content = content


class Database:
    db: list[Note]
    last_note_id: int

    def __init__(self):
        self.db = []
        self.last_note_id = 0


@app.get("/")
def index():
    return PlainTextResponse("Доступные команды: /add, /list, /note, /remove, /append, /change")

@app.post("/add")
def create_note(name: str = Body(..., embed=True), content: str = Body(..., embed=True)):
    new_note = Note(database.last_note_id, name, content)
    database.db.append(new_note)
    database.last_note_id += 1
    return PlainTextResponse("Заметка создана")

@app.get("/list")
def check_db():
    if len(database.db) > 0:
        st = "Список заметок:\n"
        st += "\n".join([f"id: {note.note_id}, name: {note.name}" for note in database.db])
        return PlainTextResponse(st)
    else:
        return PlainTextResponse("У вас нет заметок")

@app.get("/note")
def check_note(note_id: int):
    current_note: Note
    for note in database.db:
        if note.note_id == note_id:
            return PlainTextResponse(f"name: {note.name}, content: {note.content}")
    return PlainTextResponse("Заметки с этим id не существует")

@app.post("/remove")
def delete_note(note_id: int = Body(..., embed=True)):
    current_note: Note
    for note in database.db:
        if note.note_id == note_id:
            database.db.remove(note)
            return PlainTextResponse("Заметка удалена")
    return PlainTextResponse("Заметки с этим id не существует")

@app.post("/append")
def append(note_id: int = Body(..., embed=True), content: str = Body(..., embed=True)):
    current_note: Note
    for note in database.db:
        if note.note_id == note_id:
            note.content += content
            return PlainTextResponse("Заметка изменена")
    return PlainTextResponse("Заметки с этим id не существует")

@app.post("/change")
def change(note_id: int = Body(..., embed=True), name: str = Body(..., embed=True)):
    current_note: Note
    for note in database.db:
        if note.note_id == note_id:
            note.name = name
            return PlainTextResponse("Заметка изменена")
    return PlainTextResponse("Заметки с этим id не существует")

database = Database()
uvicorn.run(app)