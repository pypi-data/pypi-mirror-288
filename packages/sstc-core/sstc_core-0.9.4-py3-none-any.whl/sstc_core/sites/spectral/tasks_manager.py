import importlib
import tempfile
import os
import pickle
import psutil
from typing import Callable, Dict, Any, Optional, List

class Task:
    def __init__(self, function: Optional[Callable] = None, params: Dict[str, Any] = None, import_path: Optional[str] = None):
        """
        Initializes a task with a function and its parameters or an import path.

        :param function: The function to be executed (if already loaded).
        :param params: The parameters for the function.
        :param import_path: The import path to dynamically load the function (e.g., 'package.module.function').
        """
        if function is None and import_path is None:
            raise ValueError("Either function or import_path must be provided.")
        
        self.function = function
        self.params = params if params is not None else {}
        self.import_path = import_path

    def _import_function(self):
        """
        Dynamically imports the function using the provided import path.
        """
        if self.import_path:
            module_name, function_name = self.import_path.rsplit('.', 1)
            module = importlib.import_module(module_name)
            self.function = getattr(module, function_name)

    def run(self, input_data: Dict[str, Any] = None) -> Any:
        """
        Runs the task with the provided input data.

        :param input_data: A dictionary containing results of previous tasks, if any.
        :return: The result of the function execution.
        """
        if self.function is None:
            self._import_function()
        
        if input_data:
            self.params.update(input_data)
        return self.function(**self.params)

class TaskManager:
    def __init__(self, tasks: Dict[int, Task], stop_on_error: bool = True, default_on_error: Any = None, use_memory: bool = True):
        """
        Initializes the TaskManager with a dictionary of tasks and error handling options.

        :param tasks: A dictionary where the key is the task order and the value is a Task object.
        :param stop_on_error: Whether to stop execution if a task fails (default is True).
        :param default_on_error: Default value to use if a task fails (used only if stop_on_error is False).
        :param use_memory: Whether to use memory for storing results. If False or memory is insufficient, store on disk.
        
        Example:
        
            ```python
            # Example usage

            # Define some example functions in separate files/modules and use import paths
            def task1(param1, input_data=None):
                return param1 * 2

            def task2(param2, input_data=None):
                if input_data is None:
                    raise ValueError("input_data is required")
                return input_data + param2

            def task3(param3, input_data=None):
                return input_data ** param3

            def task4(input_data=None):
                return input_data * 2

            def task5(input_data=None):
                return sum(input_data.values())

            tasks = {
                1: Task(function=task1, params={'param1': 10}),
                2: Task(function=task2, params={'param2': 5}),
                3: Task(function=task3, params={'param3': 2}),
                4: Task(function=task4, params={}),
                5: Task(function=task5, params={})
            }

            # Define dependencies for tasks (task 5 depends on the results of tasks 1 and 3)
            dependencies = {
                2: [1],
                3: [2],
                4: [3],
                5: [1, 3],
            }

            # Create a TaskManager and run the tasks
            manager = TaskManager(tasks, stop_on_error=False, default_on_error=0)
            final_result = manager.run_all(dependencies)
            print(f"Final Result: {final_result}")
            
            
            
            ```
        """
        self.tasks = tasks
        self.stop_on_error = stop_on_error
        self.default_on_error = default_on_error
        self.use_memory = use_memory
        self.results = {}  # Store results of each task in memory
        self.temp_files = {}  # Store file paths for temporary files

    def _memory_available(self) -> bool:
        """
        Checks if there is enough available memory to store results in memory.

        :return: True if enough memory is available, False otherwise.
        """
        available_memory = psutil.virtual_memory().available
        # Here, we assume each result should ideally not exceed 100MB. Adjust as necessary.
        return available_memory > 100 * 1024 * 1024

    def _save_result(self, task_order: int, result: Any):
        """
        Saves the result in memory or on disk based on available memory.

        :param task_order: The task number.
        :param result: The result to be saved.
        """
        if self.use_memory and self._memory_available():
            self.results[task_order] = result
        else:
            temp_file = tempfile.NamedTemporaryFile(delete=False)
            with open(temp_file.name, 'wb') as f:
                pickle.dump(result, f)
            self.temp_files[task_order] = temp_file.name

    def _load_result(self, task_order: int) -> Any:
        """
        Loads the result from memory or disk.

        :param task_order: The task number.
        :return: The loaded result.
        """
        if task_order in self.results:
            return self.results[task_order]
        elif task_order in self.temp_files:
            with open(self.temp_files[task_order], 'rb') as f:
                return pickle.load(f)
        return None

    def run_all(self, dependencies: Dict[int, List[int]] = None) -> Any:
        """
        Runs all tasks in sequence, passing the output of one as the input to the next.

        :param dependencies: A dictionary where the key is the task number and the value is a list of task numbers whose results are required as input.
        :return: The final output after all tasks have been executed, or the last successful output if a task fails.
        """
        dependencies = dependencies if dependencies is not None else {}
        result = None

        for task_order in sorted(self.tasks.keys()):
            task = self.tasks[task_order]
            input_data = {}

            # Gather inputs from dependencies
            if task_order in dependencies:
                for dep_task in dependencies[task_order]:
                    input_data[f'result_from_task_{dep_task}'] = self._load_result(dep_task)

            try:
                result = task.run(input_data)
                self._save_result(task_order, result)
            except Exception as e:
                print(f"Error in task {task_order}: {e}")
                if self.stop_on_error:
                    print("Stopping execution due to error.")
                    return None
                else:
                    print("Continuing execution with default value.")
                    result = self.default_on_error
                    self._save_result(task_order, result)

        # Clean up temporary files
        for temp_file in self.temp_files.values():
            os.remove(temp_file)

        return result

