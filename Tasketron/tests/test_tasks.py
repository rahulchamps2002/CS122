from logic.task_manager import TaskManager
import os

def test_add_and_delete_task(tmp_path):
    test_file = tmp_path / "test_tasks.json"
    manager = TaskManager(str(test_file))

    manager.add_task("Sample", "Desc", "Home", "2025-01-01", "High")
    assert len(manager.tasks) == 1

    task_id = manager.tasks[0]["id"]
    manager.delete_task(task_id)
    assert len(manager.tasks) == 0
