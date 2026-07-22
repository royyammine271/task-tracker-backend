import importlib
from datetime import date, timedelta

from fastapi.testclient import TestClient

from app.models import TaskCreate


def test_cors_allows_localhost_frontend_origin(client: TestClient) -> None:
    response = client.get(
        "/health",
        headers={"origin": "http://127.0.0.1:8001"},
    )

    assert response.status_code == 200
    assert response.headers.get("access-control-allow-origin") == "http://127.0.0.1:8001"


def test_storage_persists_tasks_across_reload(monkeypatch, tmp_path) -> None:
    data_file = tmp_path / "tasks.json"
    monkeypatch.setenv("TASKS_DATA_FILE", str(data_file))

    import app.storage as storage_module

    storage_module = importlib.reload(storage_module)
    storage_module._reset()

    storage_module.add_task(TaskCreate(title="Persisted task"))

    reloaded_storage = importlib.reload(storage_module)

    assert reloaded_storage.get_all_tasks()[0].title == "Persisted task"


def test_create_task_valid_returns_201_with_full_body(
    client: TestClient,
) -> None:
    response = client.post(
        "/tasks",
        json={
            "title": "Build API",
            "description": "Create the task endpoints",
            "status": "ToDo",
            "priority": "High",
            "assignee": "Jean-Pierre",
        },
    )

    assert response.status_code == 201

    body = response.json()
    assert body["id"]
    assert body["title"] == "Build API"
    assert body["description"] == "Create the task endpoints"
    assert body["status"] == "ToDo"
    assert body["priority"] == "High"
    assert body["assignee"] == "Jean-Pierre"
    assert body["due_date"] is None
    assert body["created_at"]
    assert body["updated_at"]


def test_create_task_valid_due_date_returns_201(
    client: TestClient,
) -> None:
    response = client.post(
        "/tasks",
        json={
            "title": "Task with due date",
            "due_date": "2026-08-15",
        },
    )

    assert response.status_code == 201
    assert response.json()["due_date"] == "2026-08-15"


def test_create_task_invalid_due_date_returns_422(
    client: TestClient,
) -> None:
    response = client.post(
        "/tasks",
        json={
            "title": "Task with invalid due date",
            "due_date": "15-08-2026",
        },
    )

    assert response.status_code == 422


def test_create_task_missing_title_returns_422(
    client: TestClient,
) -> None:
    response = client.post(
        "/tasks",
        json={
            "description": "Task without a title",
            "priority": "Medium",
        },
    )

    assert response.status_code == 422


def test_create_task_blank_title_returns_422(
    client: TestClient,
) -> None:
    response = client.post(
        "/tasks",
        json={"title": "   "},
    )

    assert response.status_code == 422


def test_create_task_invalid_priority_returns_422(
    client: TestClient,
) -> None:
    response = client.post(
        "/tasks",
        json={
            "title": "Invalid priority task",
            "priority": "Urgent",
        },
    )

    assert response.status_code == 422


def test_create_task_unknown_field_returns_422(
    client: TestClient,
) -> None:
    response = client.post(
        "/tasks",
        json={
            "title": "Task with unknown field",
            "unknown_field": "not allowed",
        },
    )

    assert response.status_code == 422


def test_list_tasks_empty_returns_200_and_empty_list(
    client: TestClient,
) -> None:
    response = client.get("/tasks")

    assert response.status_code == 200
    assert response.json() == []


def test_list_tasks_filter_by_status_no_match_returns_200_and_empty_list(
    client: TestClient,
    created_task: dict,
) -> None:
    response = client.get(
        "/tasks",
        params={"status": "Done"},
    )

    assert response.status_code == 200
    assert response.json() == []


def test_list_tasks_filter_by_priority_returns_only_matches(
    client: TestClient,
) -> None:
    high_priority_response = client.post(
        "/tasks",
        json={
            "title": "High priority task",
            "priority": "High",
        },
    )
    low_priority_response = client.post(
        "/tasks",
        json={
            "title": "Low priority task",
            "priority": "Low",
        },
    )

    assert high_priority_response.status_code == 201
    assert low_priority_response.status_code == 201

    response = client.get(
        "/tasks",
        params={"priority": "High"},
    )

    assert response.status_code == 200

    body = response.json()
    assert len(body) == 1
    assert body[0]["title"] == "High priority task"
    assert body[0]["priority"] == "High"


def test_get_task_by_id_returns_task(
    client: TestClient,
    created_task: dict,
) -> None:
    response = client.get(f"/tasks/{created_task['id']}")

    assert response.status_code == 200
    assert response.json() == created_task


def test_get_task_by_id_not_found_returns_404_with_detail(
    client: TestClient,
) -> None:
    task_id = "missing-task-id"

    response = client.get(f"/tasks/{task_id}")

    assert response.status_code == 404
    assert response.json() == {
        "detail": f"Task with id {task_id} not found"
    }


def test_patch_partial_update_keeps_other_fields(
    client: TestClient,
) -> None:
    create_response = client.post(
        "/tasks",
        json={
            "title": "Original title",
            "description": "Original description",
            "priority": "High",
            "assignee": "Alice",
        },
    )
    assert create_response.status_code == 201

    original_task = create_response.json()

    response = client.patch(
        f"/tasks/{original_task['id']}",
        json={"title": "Updated title"},
    )

    assert response.status_code == 200

    updated_task = response.json()
    assert updated_task["id"] == original_task["id"]
    assert updated_task["title"] == "Updated title"
    assert updated_task["description"] == "Original description"
    assert updated_task["status"] == "ToDo"
    assert updated_task["priority"] == "High"
    assert updated_task["assignee"] == "Alice"
    assert updated_task["created_at"] == original_task["created_at"]
    assert updated_task["updated_at"]


def test_patch_due_date_can_be_added_and_removed(
    client: TestClient,
    created_task: dict,
) -> None:
    add_due_date_response = client.patch(
        f"/tasks/{created_task['id']}",
        json={"due_date": "2026-09-01"},
    )

    assert add_due_date_response.status_code == 200
    assert add_due_date_response.json()["due_date"] == "2026-09-01"

    remove_due_date_response = client.patch(
        f"/tasks/{created_task['id']}",
        json={"due_date": None},
    )

    assert remove_due_date_response.status_code == 200
    assert remove_due_date_response.json()["due_date"] is None


def test_list_tasks_filter_overdue_returns_only_not_done_past_due(
    client: TestClient,
) -> None:
    yesterday = (date.today() - timedelta(days=1)).isoformat()
    tomorrow = (date.today() + timedelta(days=1)).isoformat()

    overdue_not_done = client.post(
        "/tasks",
        json={
            "title": "Overdue not done",
            "status": "InProgress",
            "due_date": yesterday,
        },
    )
    assert overdue_not_done.status_code == 201

    not_overdue_future = client.post(
        "/tasks",
        json={
            "title": "Future due date",
            "status": "ToDo",
            "due_date": tomorrow,
        },
    )
    assert not_overdue_future.status_code == 201

    done_past_due = client.post(
        "/tasks",
        json={
            "title": "Done but past due",
            "status": "Done",
            "due_date": yesterday,
        },
    )
    assert done_past_due.status_code == 201

    no_due_date = client.post(
        "/tasks",
        json={
            "title": "No due date",
            "status": "InProgress",
        },
    )
    assert no_due_date.status_code == 201

    response = client.get(
        "/tasks",
        params={"overdue": "true"},
    )

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    assert body[0]["title"] == "Overdue not done"


def test_list_tasks_filter_overdue_still_respects_status_and_priority(
    client: TestClient,
) -> None:
    yesterday = (date.today() - timedelta(days=1)).isoformat()

    high_overdue = client.post(
        "/tasks",
        json={
            "title": "High overdue",
            "status": "InProgress",
            "priority": "High",
            "due_date": yesterday,
        },
    )
    assert high_overdue.status_code == 201

    low_overdue = client.post(
        "/tasks",
        json={
            "title": "Low overdue",
            "status": "InProgress",
            "priority": "Low",
            "due_date": yesterday,
        },
    )
    assert low_overdue.status_code == 201

    response = client.get(
        "/tasks",
        params={"overdue": "true", "status": "InProgress", "priority": "High"},
    )

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    assert body[0]["title"] == "High overdue"


def test_patch_not_found_returns_404(
    client: TestClient,
) -> None:
    task_id = "missing-task-id"

    response = client.patch(
        f"/tasks/{task_id}",
        json={"title": "Updated title"},
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": f"Task with id {task_id} not found"
    }


def test_patch_valid_transition_todo_to_inprogress_returns_200(
    client: TestClient,
    created_task: dict,
) -> None:
    response = client.patch(
        f"/tasks/{created_task['id']}",
        json={"status": "InProgress"},
    )

    assert response.status_code == 200

    body = response.json()
    assert body["id"] == created_task["id"]
    assert body["status"] == "InProgress"


def test_patch_invalid_transition_todo_to_done_returns_422(
    client: TestClient,
    created_task: dict,
) -> None:
    response = client.patch(
        f"/tasks/{created_task['id']}",
        json={"status": "Done"},
    )

    assert response.status_code == 422
    assert response.json()["detail"].startswith(
        "Invalid status transition from ToDo to Done."
    )


def test_patch_same_status_returns_422(
    client: TestClient,
    created_task: dict,
) -> None:
    response = client.patch(
        f"/tasks/{created_task['id']}",
        json={"status": "ToDo"},
    )

    assert response.status_code == 422
    assert response.json()["detail"].startswith(
        "Invalid status transition from ToDo to ToDo."
    )


def test_delete_existing_returns_204_no_body(
    client: TestClient,
    created_task: dict,
) -> None:
    response = client.delete(f"/tasks/{created_task['id']}")

    assert response.status_code == 204
    assert response.content == b""


def test_delete_missing_returns_404(
    client: TestClient,
) -> None:
    task_id = "missing-task-id"

    response = client.delete(f"/tasks/{task_id}")

    assert response.status_code == 404
    assert response.json() == {
        "detail": f"Task with id {task_id} not found"
    }