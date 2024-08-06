# pastesh

A package to create and upload encrypted pastes to paste.sh.

## Installation

```bash
pip install pastesh
```

## Usage
```python
from pastesh import upload_to_pastesh

title = "Sample Title"
message = "This is the body of the paste."
api_endpoint = "https://paste.sh"

try:
    url = upload_to_pastesh(title, message, api_endpoint)
    print(f"Paste created successfully: {url}")
except Exception as e:
    print(f"Failed to create paste: {str(e)}")
```