package main

import (
	"fmt"
	"log"
	"net/http"
)

func helloHandler(w http.ResponseWriter, r *http.Request) {
	// これを追加しないと、フロント側でエラーを吐いてしまうので注意
	w.Header().Set("Access-Control-Allow-Origin", "*");
	hello := []byte("Hello World")
	_, err := w.Write(hello)
	if err != nil {
		log.Fatal(nil)
	}
}

func main() {
	http.HandleFunc("/", helloHandler)
	fmt.Println("http://localhost:8000")
	log.Fatal(http.ListenAndServe("localhost:8000", nil))
}
