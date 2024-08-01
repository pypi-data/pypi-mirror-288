class UnionLLMError(Exception):
    """Base exception class for UnionLLM."""
    pass

class ProviderError(UnionLLMError):
    """Exception raised when there is an issue with the model provider."""
    pass

class APICallError(UnionLLMError):
    """Exception raised when an API call fails."""
    pass

from openai import (
    AuthenticationError,
    BadRequestError,
    RateLimitError,
    APIStatusError,
    OpenAIError,
    APIError, 
    APITimeoutError, 
    APIConnectionError, 
)
import httpx

class AuthenticationError(AuthenticationError):  # type: ignore
    def __init__(self, message, llm_provider, model, response: httpx.Response):
        self.status_code = 401
        self.message = message
        self.llm_provider = llm_provider
        self.model = model
        super().__init__(
            self.message,
            response=response,
            body=None
        )  # Call the base class constructor with the parameters it needs

class BadRequestError(BadRequestError):  # type: ignore
    def __init__(self, message, model, llm_provider, response: httpx.Response):
        self.status_code = 400
        self.message = message
        self.model = model
        self.llm_provider = llm_provider
        super().__init__(
            self.message,
            response=response,
            body=None
        )  # Call the base class constructor with the parameters it needs

class Timeout(APITimeoutError):  # type: ignore
    def __init__(self, message, model, llm_provider, request: httpx.Request):
        self.status_code = 408
        self.message = message
        self.model = model
        self.llm_provider = llm_provider
        super().__init__(
            request=request
        )  # Call the base class constructor with the parameters it needs

class RateLimitError(RateLimitError):  # type: ignore
    def __init__(self, message, llm_provider, model, response: httpx.Response):
        self.status_code = 429
        self.message = message
        self.llm_provider = llm_provider
        self.modle = model
        super().__init__(
            self.message,
            response=response,
            body=None
        )  # Call the base class constructor with the parameters it needs

# sub class of rate limit error - meant to give more granularity for error handling context window exceeded errors
class ContextWindowExceededError(BadRequestError):  # type: ignore
    def __init__(self, message, model, llm_provider, response: httpx.Response):
        self.status_code = 400
        self.message = message
        self.model = model
        self.llm_provider = llm_provider
        super().__init__(
            message=self.message, 
            model=self.model, # type: ignore
            llm_provider=self.llm_provider, # type: ignore
            response=response
        )  # Call the base class constructor with the parameters it needs

class ServiceUnavailableError(APIStatusError):  # type: ignore
    def __init__(self, message, llm_provider, model):
        self.status_code = 503
        self.message = message
        self.llm_provider = llm_provider
        self.model = model
        super().__init__(
            self.message
        )  # Call the base class constructor with the parameters it needs


# raise this when the API returns an invalid response object - https://github.com/openai/openai-python/blob/1be14ee34a0f8e42d3f9aa5451aa4cb161f1781f/openai/api_requestor.py#L401
class APIError(APIError): # type: ignore 
    def __init__(self, status_code, message, llm_provider, model, request: httpx.Request):
        self.status_code = status_code 
        self.message = message
        self.llm_provider = llm_provider
        self.model = model
        super().__init__(
            self.message,
            request=request # type: ignore
        )

# raised if an invalid request (not get, delete, put, post) is made
class APIConnectionError(APIConnectionError):  # type: ignore 
    def __init__(self, message, llm_provider, model):
        self.message = message
        self.llm_provider = llm_provider
        self.model = model
        super().__init__(
            self.message
        )

class OpenAIError(OpenAIError):  # type: ignore
    def __init__(self, original_exception):
        self.status_code = original_exception.http_status
        super().__init__(
            http_body=original_exception.http_body,
            http_status=original_exception.http_status,
            json_body=original_exception.json_body,
            headers=original_exception.headers,
            code=original_exception.code,
        )
        self.llm_provider = "openai"

class BudgetExceededError(Exception):
    def __init__(self, current_cost, max_budget):
        self.current_cost = current_cost
        self.max_budget = max_budget
        message = f"Budget has been exceeded! Current cost: {current_cost}, Max budget: {max_budget}"
        super().__init__(message)

## DEPRECATED ## 
class InvalidRequestError(BadRequestError):  # type: ignore
    def __init__(self, message, model, llm_provider):
        self.status_code = 400
        self.message = message
        self.model = model
        self.llm_provider = llm_provider
        super().__init__(
            self.message, f"{self.model}"
        )  # Call the base class constructor with the parameters it needs
