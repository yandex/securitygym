package main

import (
	"net/http"
)

func main() {
	s := Server{}
	mux := http.NewServeMux()
	mux.HandleFunc("/hello", s.HelloHandler)
	server := http.Server{Handler: mux, Addr: ":80"}
	server.ListenAndServe()
}
