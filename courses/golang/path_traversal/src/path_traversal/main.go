package main

import (
	"net/http"
)

func main() {
	s := Server{}
	mux := http.NewServeMux()
	mux.HandleFunc("/getfile", s.GetFileHandler)
	server := http.Server{Handler: mux, Addr: ":80"}
	server.ListenAndServe()
}
