from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi_request_limit.fastapi_request_limit import request_limit

app = FastAPI()

@app.post("/", response_class=JSONResponse)
@request_limit(seconds=5, data=["foo", "bar"])
async def root(foo: str, bar: int, request: Request):
    """
    Endpoint to demonstrate rate limiting based on 'foo' and 'bar' parameters.

    Args:
        foo (str): A string parameter.
        bar (int): An integer parameter.
        request (Request): The HTTP request object.

    Returns:
        JSONResponse: JSON response indicating the request acceptance.
    """
    return JSONResponse(content={"message": f"Request accepted for {foo} and {bar}"})
