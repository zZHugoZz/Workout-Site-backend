from fastapi import HTTPException, status


FORBIDDEN_EXCEPTION = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Not authorized to perform this action",
)


def NOT_FOUND_EXCEPTION(name: str, id: int) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"{name.capitalize()} with id: {id} doesn't exist",
    )
