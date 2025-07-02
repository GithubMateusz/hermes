from esmerald import Request, status
from esmerald.exceptions import HTTPException
from sqlalchemy.exc import IntegrityError


class Conflict(HTTPException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Item already exists."


async def handle_integrity_error(request: Request, exc: IntegrityError) -> Conflict:
    raise Conflict()
