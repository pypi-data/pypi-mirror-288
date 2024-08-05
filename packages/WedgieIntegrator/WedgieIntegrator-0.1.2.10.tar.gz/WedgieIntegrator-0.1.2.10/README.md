# WedgieIntegrator
WedgieIntegrator is an async friendly package for Python which acts as API client toolkit for creating and managing API clients with ease.

## Features

- Fully asynchronous
- Simple configuration
- Multiple authentication strategies
- Retry mechanisms
- Pagination
- Helpful logging

## Installation

```bash
pip install WedgieIntegrator
```


# ToDo
- Add pagination option where the response can provide all remaining links at once
- Break out the steps for inspecting httpx responses. This way an overridden method could apply custom exceptions without 
  having to override the entire send_request method.
- Add automatic wait & retry for connection errors
- Add automatic wait & retry for rate limit errors
- More tests
- Documentation
- sample scripts, or perhaps a library of specific API configurations
- Review all non-async methods and consider making them async

- kinda done: Add rate limiting (safe for Python 3.7)
