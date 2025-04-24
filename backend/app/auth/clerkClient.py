import os
import httpx
from fastapi import Depends
from clerk_backend_api import Clerk
from clerk_backend_api.jwks_helpers import authenticate_request, AuthenticateRequestOptions

from fastapi.security import APIKeyHeader
from app.core.config import settings


oauth2_schema = APIKeyHeader(name="Authorization")

sdk = Clerk(bearer_auth=settings.CLERK_SECRET_KEY)

# def is_signed_in(request: httpx.Request):
    # request_state = sdk.sign_in_tokens(
    #     request,
    #     AuthenticateRequestOptions(
    #         authorized_parties=['https://example.com']
    #     )
    # )
    # return request_state.is_signed_in

# async def verify_token(token: str = Depends(oauth2_schema)):
#     res = clerk.clients.verify(request={
#         "token": token,
#     })

#     assert res is not None, "Token is invalid"

#     return res["user"]



# async def get_current_user(user: Dict[str, Any] = Depends(verify_token)):
#   return user