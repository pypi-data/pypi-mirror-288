# async_llm_handler/exceptions.py

class LLMAPIError(Exception):
    """Exception raised for errors in the LLM API."""
    pass

class RateLimitTimeoutError(Exception):
    """Exception raised when a rate limit wait exceeds the specified timeout."""
    pass