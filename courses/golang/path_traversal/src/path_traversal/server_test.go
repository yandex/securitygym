package main

import (
	"net/http"
	"net/http/httptest"
	"strings"
	"testing"
)

func TestXSSHandler(t *testing.T) {
	s := Server{}

	t.Run("functional test", func(t *testing.T) {
		request, _ := http.NewRequest(http.MethodGet, "/getfile?filename=passwd", nil)
		response := httptest.NewRecorder()

		s.GetFileHandler(response, request)

		if strings.Index(response.Body.String(), "OK") == -1 {
			t.Errorf("Functional test failed, returns %s", response.Body.String())
		}
	})
	t.Run("security test", func(t *testing.T) {
		request, _ := http.NewRequest(http.MethodGet, "/getfile?filename=../../../../../../../etc/passwd", nil)
		response := httptest.NewRecorder()

		s.GetFileHandler(response, request)

		if strings.Index(response.Body.String(), "root") != -1 {
			t.Errorf("Security test failed, returns %s", response.Body.String())
		}

	})

}
