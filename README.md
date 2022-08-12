# Busty

A simple web-directory scanner written in Golang. This project was originally written using the Python language, i used the oppourtunity to rewrite this to become more familiar with Golang concurrency and worker pools.

## Build

```console
go build .
```

## Usage

```console
./busty --target=https://example.com --wordlist=./wordlist.txt --workers=8
```

## Arguments

- `--target` The target URL to scan
- `--wordlist` The wordlist to use
- `--workers` Number of threads to use (default: CPU thread count)
- `--status-codes` Comma-separated list of status codes to include in the scan (default: 200,301,302,303,307)
