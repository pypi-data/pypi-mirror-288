from http import HTTPStatus


class Response:
    id: str
    status: HTTPStatus
    detail: dict

    def __init__(
        self,
        *,
        id: str = None,
        status: HTTPStatus = HTTPStatus.OK,
        detail: dict = None
    ):
        self.id = id
        self.status = status
        self.detail = detail
