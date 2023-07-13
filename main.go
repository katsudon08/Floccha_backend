package main

import (
	"encoding/json"
	"fmt"
	"io"
	"log"
	"net/http"
	"strconv"
	"reflect"
)

type Ping struct {
	Status int    `json:"status"`
	Result string `json:"result"`
}

func helloHandler(w http.ResponseWriter, r *http.Request) {
	// これを追加しないと、フロント側でエラーを吐いてしまうので注意
	w.Header().Set("Access-Control-Allow-Origin", "*")
	w.Header().Set("Access-Control-Allow-Headers", "Content-Type")
	w.Header().Set("Accept", "application/json")

	ping := Ping{
		Status: http.StatusOK,
		Result: "ok",
	}
	res, _ := json.Marshal(ping)

	header := r.Header
	fmt.Println("header", header)

	if r.Method == "POST" || r.Method == "OPTIONS" {
		w.WriteHeader(http.StatusOK)
	} else {
		w.WriteHeader(http.StatusBadRequest)
		return
	}

	if r.Header.Get("Content-Type") != "application/json" {
		w.WriteHeader(http.StatusBadRequest)
	}

	length, err := strconv.Atoi(r.Header.Get("Content-Length"))
	if err != nil {
		w.WriteHeader(http.StatusInternalServerError)
		return
	}

	body := make([]byte, length)
	length, err = r.Body.Read(body)
	if err != nil && err != io.EOF {
		w.WriteHeader(http.StatusInternalServerError)
		return
	}

	var jsonBody map[string][]string
	err = json.Unmarshal(body[:length], &jsonBody)
	if err != nil {
		w.WriteHeader(http.StatusInternalServerError)
		return
	}

	fmt.Println("request", jsonBody["src"])
	srcJsonBody := jsonBody["src"]
	fmt.Println(reflect.TypeOf(srcJsonBody))
	fmt.Println(srcJsonBody[0])

	w.WriteHeader(http.StatusOK)
	w.Write(res)
}

func main() {
	http.HandleFunc("/", helloHandler)
	fmt.Println("http://localhost:8000")
	log.Fatal(http.ListenAndServe("localhost:8000", nil))
}
