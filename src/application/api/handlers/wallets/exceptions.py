from fastapi import status

from application.api.exceptions import APIErrorSchema, BaseHTTPError


class NotFoundAddressHTTPException(BaseHTTPError):
    status_code = status.HTTP_404_NOT_FOUND
    code = "ADDRESS_NOT_FOUND"

    def __init__(self, address: str):
        self.error_schema = APIErrorSchema(
            code=self.code,
            message="Address `{address}` in Tron not found".format(address=address),
        )
        super().__init__()


class InvalidFormatAddressHTTPException(BaseHTTPError):
    status_code = status.HTTP_400_BAD_REQUEST
    code = "INVALID_FORMAT_ADDRESS"

    def __init__(self, address: str):
        self.error_schema = APIErrorSchema(
            code=self.code,
            message="Invalid format of address `{address}`".format(address=address),
        )
        super().__init__()
