# Busty
Web-directory scanner written in python


### Setup
```sh
> python -m pip install -r requirements.txt
```

### Example
```sh
> python busty.py --target https://raffsimms.com --list list.txt
[200] https://raffsimms.com/contact
[404] https://raffsimms.com/admin

```
- `--target`

  the target domain to scan (required)
- `--list` 

  the word list to fetch url requests from (required)
- `--status` 

  optionally specify a certain status code to look for
