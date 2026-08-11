from fastapi import HTTPException, status

from app.models import TaskStatus


VALID_TRANSITIONS: frozenset[tuple[TaskStatus, TaskStatus]] = frozenset(
    {
        (TaskStatus.TODO, TaskStatus.IN_PROGRESS),
        (TaskStatus.IN_PROGRESS, TaskStatus.DONE),
        (TaskStatus.DONE, TaskStatus.IN_PROGRESS),
    }
)


def validate_status_transition(
    current: TaskStatus,
    new: TaskStatus,
) -> None:
    """Validate that a status transition is allowed.

    Args:
        current (TaskStatus): Current task status.
        new (TaskStatus): Requested next status.

    Returns:
        None.

    Raises:
        HTTPException: 422 when the transition is not in VALID_TRANSITIONS.
    """
    if (current, new) not in VALID_TRANSITIONS:
        allowed = sorted(
            {
                f"{from_status.value}->{to_status.value}"
                for from_status, to_status in VALID_TRANSITIONS
            }
        )
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=(
                f"Invalid status transition from {current.value} to "
                f"{new.value}. Allowed transitions: {allowed}"
            ),
        )