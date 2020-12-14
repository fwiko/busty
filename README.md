# Busty
Web-directory scanner written in python


### Setup
```sh
> python -m pip install -r requirements.txt
```

### Directory Scanner Example
```sh
> python busty.py -t https://raffsimms.com -l default.txt
[BUSTY] Using default.txt

[200] https://raffsimms.com/contact

Checked 11/11 | Found 1
Finished in 0.29s
```
- `-t/--target`

  the target domain to scan (required)
  
- `-l/--list` 

  the word list to fetch url requests from (required)
  
<!-- - `--status` 

  optionally specify a certain status code to look for --!>
