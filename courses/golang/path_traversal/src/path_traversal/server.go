package main

import (
	"io"
	"net/http"
	"os"
	"strconv"
)

type Server struct {
}

func (s *Server) GetFileHandler(w http.ResponseWriter, req *http.Request) {
	filename := req.URL.Query().Get("filename")
	f, err := os.Open("uploads/"+filename)
	defer f.Close()
	if err != nil {
		http.Error(w, "File not found.", 404)
		return
	}
	fileHeader := make([]byte, 512)
	f.Read(fileHeader)
	fileContentType := http.DetectContentType(fileHeader)

	fileStat, _ := f.Stat()
	fileSize := strconv.FormatInt(fileStat.Size(), 10)

	w.Header().Set("Content-Disposition", "attachment; filename="+filename)
	w.Header().Set("Content-Type", fileContentType)
	w.Header().Set("Content-Length", fileSize)

	f.Seek(0, 0)
	io.Copy(w, f)
	return
}
