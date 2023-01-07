import Utils
from Utils import execute_action, DbAction


class Task:
    id: int
    name: str
    description: str
    output: str

    def __init__(self, task_id, name, description, output):
        self.id = task_id
        self.name = name
        self.description = description
        self.output = output

    def save(self):
        execute_action('''
        update tasks set name = ?, description = ?, output = ? where id = ? 
        ''', (self.name, self.description, self.output, self.id), DbAction.commit)

    @staticmethod
    def get(task_id: int) -> 'Task':
        db_task = execute_action(
            '''select * from tasks where id = ?''', (task_id,), DbAction.fetchone
        )
        if db_task is None:
            return None
        task = Task(db_task[0], db_task[1], db_task[2], db_task[3])
        return task

    @staticmethod
    def all():
        db_tasks = execute_action('''
        select * from tasks
        ''', (), DbAction.fetchall)
        tasks = []
        for task in db_tasks:
            tasks.append(Task(task[0], task[1], task[2], task[3]))
        return tasks

    @staticmethod
    def create(name: str, description: str, output: str):
        task_id = execute_action('''
        insert into tasks (name, description, output) values (?, ?, ?)
        ''', (name, description, output), DbAction.commit)
        task = Task.get(task_id)
        return task


    def check_solution(self, code: str) -> bool:
        output = Utils.run_code(code)
        if output[-1] == "\n":
            output = output[:-2]
        return output == self.output
