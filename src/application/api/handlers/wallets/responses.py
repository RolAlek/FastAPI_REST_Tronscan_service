from application.api.exceptions import get_responses
from application.api.handlers.wallets import exceptions

get_wallet_info_responses = get_responses(
    exceptions.NotFoundAddressHTTPException("address"),
    exceptions.InvalidFormatAddressHTTPException("address"),
)
