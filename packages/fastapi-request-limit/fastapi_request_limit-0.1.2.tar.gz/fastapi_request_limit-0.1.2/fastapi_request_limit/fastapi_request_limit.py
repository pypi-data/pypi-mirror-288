from fastapi import HTTPException, Request
from datetime import datetime, timedelta
from functools import wraps
from typing import Dict, Callable, Any, List

def request_limit(seconds: int, data: List[str]):
    """
    Decorator to limit the rate of requests to a FastAPI endpoint based on specified parameters.

    Args:
        seconds (int): Minimum number of seconds required between requests with the same parameter values.
        data (List[str]): List of parameter names to use for rate limiting.

    Returns:
        Callable: A decorator function for FastAPI route handlers.
    """
    last_request_time: Dict[str, datetime] = {}

    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            request: Request = kwargs.get("request")
            
            # Extract all specified parameters to form a unique key
            key_parts = []
            for param in data:
                value = kwargs.get(param) or request.path_params.get(param) or request.query_params.get(param)
                if value is None:
                    raise HTTPException(status_code=400, detail=f"Missing required parameter: {param}")
                key_parts.append(str(value))
            
            # Create a unique key by joining the values of the parameters
            key = "_".join(key_parts)

            current_time = datetime.now()

            # Check the last request time for the given key
            last_time = last_request_time.get(key)
            if last_time and (current_time - last_time) < timedelta(seconds=seconds):
                raise HTTPException(status_code=429, detail=f"Requests can only be made every {seconds} seconds")

            # Update the last request time for this unique key
            last_request_time[key] = current_time

            # Call the original function
            return await func(*args, **kwargs)

        return wrapper

    return decorator