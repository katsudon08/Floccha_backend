package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
)

type Ping struct {
	Status int    `json:"status"`
	Result string `json:"result"`
}

func helloHandler(w http.ResponseWriter, r *http.Request) {
	// これを追加しないと、フロント側でエラーを吐いてしまうので注意
	w.Header().Set("Access-Control-Allow-Origin", "*")
	w.Header().Set("Access-Control-Allow-Headers", "Content-Type")

	ping := Ping{
		Status: http.StatusOK,
		Result: "ok",
	}
	res, _ := json.Marshal(ping)

	len := r.ContentLength
	body := make([]byte, len)
	r.Body.Read(body)

	fmt.Println("reauest", string(body))
	_, err := w.Write(res)
	if err != nil {
		log.Fatal(nil)
	}
}

func main() {
	http.HandleFunc("/", helloHandler)
	fmt.Println("http://localhost:8000")
	log.Fatal(http.ListenAndServe("localhost:8000", nil))
}
