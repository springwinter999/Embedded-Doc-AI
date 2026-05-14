from fastapi import Depends, HTTPException, Request


async def get_current_user(request: Request):
    """
    Placeholder: currently allows all requests.
    To add authentication later:
      1. Read token from request.headers["Authorization"]
      2. Validate the token
      3. Return user info or raise HTTPException(401)
    Only this function needs to change — all routers stay the same.
    """
    return {"user_id": "anonymous"}
