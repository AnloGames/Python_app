from Utils import execute_action, DbAction

class Task:
    id: int
    name: str
    content: str
    output: str

    def __init__(self, id, name, content, output):
        self.id = id
        self.name = name
        self.content = content
        self.output = output


def get_task(task_id: int) -> Task:
    db_task = execute_action(
        '''select * from tasks where id = ?''', (task_id,), DbAction.fetchone
    )
    if db_task is None:
        return None
    task = Task(db_task[0], db_task[1], db_task[2], db_task[3])
    return task