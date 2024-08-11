from fastapi import HTTPException


class BaseException(HTTPException):
    status_code = 500
    detail = "Что-то пошло не так"

    def __init__(
        self,
        status_code: int = None,
        detail=None,
    ) -> None:
        super().__init__(
            status_code=self.status_code or status_code, detail=self.detail or detail
        )
