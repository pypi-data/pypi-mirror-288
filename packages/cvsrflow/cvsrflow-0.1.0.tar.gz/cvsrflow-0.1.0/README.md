# cvsrflow

`cvsrflow` is a Python library for capturing website screenshots and sending them to OpenAI API.

## Installation

```bash
pip install cvsrflow
```

## Usage

```python
from cvsrflow import cvsrflow

api_key = 'YOUR_OPENAI_API_KEY'
url = 'https://example.com'

response = cvsrflow(api_key, url)
print(response)
```
