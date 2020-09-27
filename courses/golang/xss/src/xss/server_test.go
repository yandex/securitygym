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
		request, _ := http.NewRequest(http.MethodGet, "/hello?name=alex&return_url=https://ya.ru", nil)
		response := httptest.NewRecorder()

		s.HelloHandler(response, request)

		if strings.Index(response.Body.String(), "<b>alex</b>") == -1 ||
			strings.Index(response.Body.String(), "<a href=\"https://ya.ru\">") == -1 {
			t.Errorf("Functional test failed, /payments returns %s", response.Body.String())
		}

	})
	t.Run("security test", func(t *testing.T) {
		request, _ := http.NewRequest(http.MethodGet, "/hello?name=<xss>&return_url=javascript:alert()", nil)
		response := httptest.NewRecorder()

		s.HelloHandler(response, request)

		if strings.Index(response.Body.String(), "<xss>") != -1 ||
			strings.Index(response.Body.String(), "<a href=\"javascript:alert()\">") != -1 {
			t.Errorf("Security test failed, /payments returns %s", response.Body.String())
		}

	})

}
