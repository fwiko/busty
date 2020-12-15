# Busty
Web-directory scanner written in python


### Setup
```sh
> python -m pip install -r requirements.txt
```

## Directory Scanner

### Example

```sh
> python busty.py -m ds -t https://raffsimms.com -l default.txt
[BUSTY] Using default.txt

[200] https://raffsimms.com/contact

Checked 11/11 | Found 1
Finished in 0.29s
```


### Arguments
- `-t/--target`

  the target domain to scan (required)
  
- `-l/--list` 

  the word list to fetch url requests from (required)

### Config

```json
"dirscanner": {
    "timeout": 15,
    "threads": 8,
    "response-codes": [200, 301, 502, 403, 401],
    "default-word-list": "default.txt",
    "headers": {
        "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0"
    }
}
```

- timeout - The time in which a request will timeout
- threads - max_workers (threads) for the ThreadPoolExecutor
- response-codes - Response codes that will be watched for and output
- default-word-list - Default word list to use if one is not specified
- headers - Headers to be used for requests

