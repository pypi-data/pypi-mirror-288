import math
import shutil
from abc import ABC
from pathlib import Path
# https://docs.python.org/3/library/tempfile.html
from tempfile import NamedTemporaryFile

from todotree.Errors.NoSuchTaskError import NoSuchTaskError
from todotree.Task.ConsoleTask import ConsoleTask
from todotree.Task.Task import Task


class AbstractManager(ABC):
    not_found_error = FileNotFoundError
    """Error to raise when the database file is not found."""

    @property
    def max_task_number(self) -> int:
        """Property which defines the highest number in the task list."""
        try:
            return max([x.i for x in self.task_list])
        except ValueError:
            # Then the list is empty
            return 0

    @property
    def number_of_digits(self) -> int:
        """Property which defines the number of digits of the task in the task list with the highest number."""
        return int(math.ceil(math.log(self.max_task_number + 1, 10)))

    def __init__(self):
        self.file: Path = Path("/")
        """Path to the 'database' file. Must be set in the subclass."""

        self.task_list: list[Task] = []
        """Task list"""

    def remove_task_from_file(self, task_number: int) -> Task:
        # Remove task.
        return self.remove_tasks_from_file([task_number])[0]

    def remove_tasks_from_file(self, task_numbers: list[int]) -> list[Task]:
        """Removes the list of task numbers from the task list and writes the pruned list to the file."""
        removed_tasks = [tasks for tasks in self.task_list if tasks.i in task_numbers]
        if len(removed_tasks) != len(task_numbers):
            # One or more are missing, diff the sets, convert to string.
            set_diff = set(task_numbers) - set([tasks.i for tasks in removed_tasks])
            missed_tasks = ', '.join([str(i) for i in set_diff])
            # Raise an error.
            raise NoSuchTaskError(f"Task{'s' if len(set_diff) != 1 else ''} {missed_tasks} does not exist in {self.file}.")
        # Remove tasks. We add empty tasks to preserve the location of the remaining tasks.
        new_list = []
        for task in self.task_list:
            if task.i not in task_numbers:
                new_list.append(task)
            else:
                new_list.append(Task(task.i, ""))
        self.task_list = new_list
        self.write_to_file()
        return removed_tasks

    def write_to_file(self):
        """Writes the entire list to the file."""
        # Sort task list.
        self.task_list.sort(key=lambda x: x.i)
        expanded_task_list = [Task(i, "") for i in range(1, self.max_task_number + 1)]
        for task in self.task_list:
            expanded_task_list[task.i - 1] = task
        # Remove empty tasks at the end of the list.
        for task in reversed(expanded_task_list):
            if task.task_string == "":
                expanded_task_list.pop()
            else:
                break
        #  Delete=false is needed for windows, I hope that somebodies temp folder won't be clobbered with this...
        try:
            with NamedTemporaryFile("w+t", newline="", delete=False) as temp_file:
                for task in expanded_task_list:
                    temp_file.write(task.to_file())
                temp_file.flush()
                shutil.copy(temp_file.name, self.file)
        except FileNotFoundError as e:
            raise self.not_found_error from e

    def get_task_by_task_number(self, task_number: int) -> Task | None:
        for task in self.task_list:
            if task.i == task_number:
                return task
        return None

    def add_tasks_to_file(self, tasks: list[Task]) -> list[Task]:
        """Adds multiple tasks to the file. Returns the added tasks."""
        if len(self.task_list) != 0:
            numbers = set(x.i for x in self.task_list)
            blanks = list(set(range(1, self.max_task_number)) - numbers)
            blanks.sort()
            if len(blanks) >= len(tasks):
                for task in tasks:
                    task.i = blanks.pop(0)
            else:
                # Fill in the blanks.
                i = 0 # Warning, is modified in the following loop.
                for i, blank in enumerate(blanks):
                    tasks[i].i = blank
                # Add the remaining to the end of the list.
                for j, task in enumerate(tasks[i:], start=1):
                    task.i = j + self.max_task_number

        # Final housekeeping.
        self.task_list.extend(tasks)
        self.write_to_file()
        return tasks

    def import_tasks(self):
        """Imports the tasks from the database file."""
        try:
            with self.file.open('r') as f:
                content = f.readlines()
                for i, task in enumerate(content):
                    # Skip empty lines.
                    if task.strip() == "":
                        continue
                    self.task_list.append(Task(i + 1, task.strip()))
        except FileNotFoundError as e:
            raise self.not_found_error() from e

    def __str__(self):
        """List the tasks."""
        s = ""
        for tsk in [ConsoleTask(task.i, task.task_string, self.number_of_digits) for task in self.task_list]:
            s += str(tsk) + "\n"
        return s

    def __repr__(self):
        return f"AbstractManager({self.max_task_number} Tasks)"
