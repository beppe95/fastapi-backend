from typing import Type

from fastapi import status as statuscode
from fastapi.responses import JSONResponse

from .models.errors import BaseError, NotFoundError, BaseIdentifiedError


class BaseAPIException(Exception):
    """Base error for custom API exceptions"""
    message = "Generic error"
    code = statuscode.HTTP_500_INTERNAL_SERVER_ERROR
    model = BaseError

    def __init__(self, **kwargs):
        kwargs.setdefault("message", self.message)
        self.message = kwargs["message"]
        self.data = self.model(**kwargs)

    def __str__(self):
        return self.message

    def response(self):
        return JSONResponse(
            content=self.data.dict(),
            status_code=self.code
        )

    @classmethod
    def response_model(cls):
        return {cls.code: {"model": cls.model}}


class BaseIdentifiedException(BaseAPIException):
    """Base error for exceptions related with entities, uniquely identified"""
    message = "Entity error"
    code = statuscode.HTTP_500_INTERNAL_SERVER_ERROR
    model = BaseIdentifiedError

    def __init__(self, identifier, **kwargs):
        super().__init__(identifier=identifier, **kwargs)


class NotFoundException(BaseIdentifiedException):
    """Base error for exceptions raised because an entity does not exist"""
    message = "The entity does not exist"
    code = statuscode.HTTP_404_NOT_FOUND
    model = NotFoundError


class TrafficLogNotFoundException(NotFoundException):
    """Error raised when a traffic log does not exist"""


def get_exception_responses(
        *args: Type[BaseAPIException]
) -> dict:
    responses = dict()
    for cls in args:
        responses.update(cls.response_model())
    return responses
