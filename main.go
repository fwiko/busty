package main

import (
	"bufio"
	"flag"
	"fmt"
	"net"
	"net/http"
	"net/url"
	"os"
	"path/filepath"
	"runtime"
	"strconv"
	"strings"
	"sync"

	"golang.org/x/exp/slices"
)

type Options struct {
	TargetAddress string
	WordlistPath  string
	WorkerCount   int
	StatusCodes   []int
}

func isValidUrl(targetAddress string) bool {
	uri, err := url.ParseRequestURI(targetAddress)
	if err != nil {
		return false
	}

	switch uri.Scheme {
	case "http", "https":
	default:
		return false
	}

	_, err = net.LookupHost(uri.Host)
	return err == nil
}

func loadWordlist(wordlistPath string) ([]string, error) {
	wordlistFile, err := os.Open(wordlistPath)
	if err != nil {
		return make([]string, 0), err
	}
	defer wordlistFile.Close()

	var wordlist []string
	scanner := bufio.NewScanner(wordlistFile)
	for scanner.Scan() {
		wordlist = append(wordlist, scanner.Text())
	}

	return wordlist, nil
}

func requestUrl(targetAddress string) (int, error) {
	resp, err := http.Get(targetAddress)
	if err != nil {
		return 0, err
	}
	return resp.StatusCode, nil
}

func leftJustify(text string, length int) string {
	return fmt.Sprintf("%s%s", text, strings.Repeat(" ", length-len(text)))
}

func main() {
	options := Options{}

	flag.StringVar(&options.TargetAddress, "target", "", "Target address to scan")
	flag.StringVar(&options.WordlistPath, "wordlist", "", "The path of the wordlist file to use")
	flag.IntVar(&options.WorkerCount, "workers", runtime.NumCPU(), "Number of threads to use (default; CPU thread count)")

	tempStatusCodes := flag.String("status-codes", "200,301,302,303,307", "Comma-separated list of status codes to look for")
	options.StatusCodes = make([]int, len(strings.Split(*tempStatusCodes, ",")))

	for i, code := range strings.Split(*tempStatusCodes, ",") {
		options.StatusCodes[i], _ = strconv.Atoi(strings.Trim(code, " "))
	}

	flag.Parse()

	if !isValidUrl(options.TargetAddress) {
		fmt.Println("* Please specify a valid target address")
		return
	}

	if (options.TargetAddress)[len(options.TargetAddress)-1] == '/' {
		options.TargetAddress = (options.TargetAddress)[:len(options.TargetAddress)-1]
	}

	if options.WordlistPath == "" {
		fmt.Println("* Please specify a wordlist path using the --wordlist flag")
		return
	}
	wordlist, err := loadWordlist(options.WordlistPath)
	if err != nil {
		fmt.Printf("* Unable to open wordlist file: %s\n", options.WordlistPath)
		return
	}

	var wg sync.WaitGroup
	in := make(chan string, options.WorkerCount)

	targetAddressText := leftJustify("Target", 9) + ": " + options.TargetAddress
	wordlistText := leftJustify("Wordlist", 9) + ": " + filepath.Base(options.WordlistPath)
	workersText := leftJustify("Threads", 9) + ": " + strconv.Itoa(options.WorkerCount)

	fmt.Printf("\n* %s\n* %s\n* %s\n\n", targetAddressText, wordlistText, workersText)

	matches := 0

	for i := 0; i < options.WorkerCount; i++ {
		wg.Add(1)
		go func() {
			defer wg.Done()
			for word := range in {
				t := options.TargetAddress + "/" + word
				statusCode, err := requestUrl(t)
				if err != nil {
					continue
				}
				if slices.Contains(options.StatusCodes, statusCode) {
					fmt.Printf("[%d] %s\n", statusCode, t)
					matches++
				}
			}
		}()
	}

	for _, word := range wordlist {
		in <- word
	}
	close(in)
	wg.Wait()

	fmt.Printf("\n* Scanned %d paths | Found %d matches\n", len(wordlist), matches)
}
