package main

import (
	"bufio"
	"encoding/csv"
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
	"time"

	"golang.org/x/exp/slices"
)

type Options struct {
	TargetAddress string
	WordListPath  string
	WorkerCount   int
	StatusCodes   []int
	Output        bool
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

func loadWordList(wordlistPath string) ([]string, error) {
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

func outputResults(results [][]string) (int, error) {
	outputFile, err := os.Create(fmt.Sprintf("results_%d.csv", time.Now().Unix()))
	if err != nil {
		return 0, err
	}
	defer outputFile.Close()

	writer := csv.NewWriter(outputFile)
	defer writer.Flush()

	header := []string{"URL", "Status"}
	writer.Write(header)
	writer.WriteAll(results)

	return 0, nil
}

func main() {
	options := Options{}

	flag.StringVar(&options.TargetAddress, "target", "", "Target address to scan")
	flag.StringVar(&options.WordListPath, "wordlist", "", "The path of the wordlist file to use")
	flag.IntVar(&options.WorkerCount, "workers", runtime.NumCPU(), "Number of threads to use (default; CPU thread count)")
	flag.BoolVar(&options.Output, "output", false, "Output results to a file (default; false)")

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

	if options.WordListPath == "" {
		fmt.Println("* Please specify a wordlist path using the --wordlist flag")
		return
	}

	wordlist, err := loadWordList(options.WordListPath)
	if err != nil {
		fmt.Printf("* Unable to open wordlist file: %s\n", options.WordListPath)
		return
	}

	var wg sync.WaitGroup
	in := make(chan string, options.WorkerCount)

	fmt.Printf(
		"\n* %s\n* %s\n* %s\n\n",
		fmt.Sprintf("Target..... %s", options.TargetAddress),
		fmt.Sprintf("Wordlist... %s", filepath.Base(options.WordListPath)),
		fmt.Sprintf("Threads.... %d", options.WorkerCount),
	)

	matches := 0
	checked := 0

	results := [][]string{}

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

				if options.Output {
					r := []string{t, strconv.Itoa(statusCode)}
					results = append(results, r)
				}

				checked++
				if checked != len(wordlist) {
					fmt.Fprintf(os.Stdout, "* %d/%d Checked, %d Matches\r", checked, len(wordlist), matches)
				} else {
					fmt.Printf("\n* %d/%d Checked, %d Matches", checked, len(wordlist), matches)
				}
			}
		}()
	}

	for _, word := range wordlist {
		in <- word
	}
	close(in)
	wg.Wait()

	if options.Output {
		outputResults(results)
	}
}
