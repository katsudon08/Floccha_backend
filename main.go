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

//! もう少しモック関数に修正
func main() {
	analysis := func(w http.ResponseWriter, r *http.Request) {
		ping := Ping{http.StatusOK, "Ok"}
		res, err := json.Marshal(ping)

		if err != nil {
			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}

		if r.Method == "POST" {
			fmt.Println(r)
		}
		w.Header().Set("Content-Type", "application/json")
		w.Write(res)
	}

	http.HandleFunc("/", analysis)

	fmt.Println("starting server: http://localhost:8000")
	//* ListenAndServeは起動に失敗するとerrorオブジェクトを返すため、その内容を出力する必要があるのでlog.Fatal1で囲んでいる
	log.Fatal(http.ListenAndServe(":8000", nil))
}
