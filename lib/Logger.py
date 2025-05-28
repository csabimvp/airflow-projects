"""
Logger class to log successful and unsuccesful API calls and DAG runs.

Measure how long a task took start -> finish
Measure API call outcomes

data model:
- date
- taskID
- task Name
- processing_time
- request status_code
- data_size
"""

import os
import pathlib
import random
import string
import sys
from dataclasses import dataclass
from datetime import datetime

# from ...lib.Processors import DataProcessor, ItemProcessor

lib = os.path.join(pathlib.Path(__file__).parent.parent.parent.resolve(), "lib")
sys.path.append(lib)
from Processors import ItemProcessor


@dataclass
class LogItem(ItemProcessor):
    data_items: int
    description: str
    finished: str
    project_name: str
    start: str
    status_code: int
    task_id: str
    task_name: str

    def generate_id():
        characterList = string.ascii_letters + string.digits
        myId = "".join([random.choice(characterList) for i in range(30)])
        return myId

    def format_date(self):
        return self.start.strftime("%Y-%m-%d %H:%M:%S")
        # return self.start.strptime("%Y-%m-%d %H:%M:%S")

    def __init__(self, project_name, task_name):
        self.data_items = 0
        self.description = None
        self.finished = None
        self.project_name = project_name
        self.start = datetime.now()
        self.status_code = None
        self.task_id = LogItem.generate_id()
        self.task_name = task_name

    def __str__(self):
        return f"{self.project_name} - {self.task_name} (id: {self.task_id}) on {self.start}: {self.error_message} "

    def log_actions(self, data_items=0, description="Success", status_code=200) -> None:
        self.data_items = data_items
        self.description = description
        self.status_code = status_code
        self.finished = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.start = self.format_date()
        print("Log saved.")


if __name__ == "__main__":
    L = LogItem(project_name="Test", task_name="Test01")
