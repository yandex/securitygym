package main

import (
	"fmt"
	"net/http"
)

type Server struct {
}

func (s *Server) HelloHandler(w http.ResponseWriter, req *http.Request) {
	helloTemplate := `
	<html>
	<head></head>
	<body>
		<p>Hello, <b>%s</b></p>
		<p><a href="%s">Go back</a></p>
	</body>
	</html>
	`
	name := req.URL.Query().Get("name")
	returnUrl := req.URL.Query().Get("return_url")
	fmt.Fprintf(w, helloTemplate, name, returnUrl)
}
