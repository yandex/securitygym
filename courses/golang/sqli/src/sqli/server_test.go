package main

import (
	"database/sql"
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"testing"

	_ "github.com/mattn/go-sqlite3"
)

func insertTestDataIntoDatabase() {
	database, _ := sql.Open("sqlite3", "./payments.db")
	statement, _ := database.Prepare("INSERT INTO payments (id, amount, user_id, description) VALUES (?, ?, ?, ?)")
	statement.Exec(1, 100, 1, "first payment")
	statement.Exec(2, 250, 1, "My second payment")
	statement.Exec(3, 1337, 2, "Secret payment")
	statement.Exec(4, 32, 1, "One more payment")
	database.Close()
}

func TestSQLiHandler(t *testing.T) {
	InitDatabase()
	insertTestDataIntoDatabase()
	database := GetDatabase()
	s := Server{DB: database}

	t.Run("functional test", func(t *testing.T) {
		request, _ := http.NewRequest(http.MethodGet, "/filter?from_amount=51", nil)
		response := httptest.NewRecorder()

		s.FilterPayments(response, request)

		var payments []Payment
		_ = json.Unmarshal(response.Body.Bytes(), &payments)

		if len(payments) != 2 || payments[0].ID != 1 || payments[1].ID != 2 {
			t.Errorf("Functional test failed, got %s", response.Body.String())
		}
	})
	t.Run("security test", func(t *testing.T) {
		payloads := [...]string{"5 or 1=1 --", "5' or 1=1 --", "5\" or 1=1 --", "5` or 1=1 --",
			"5') or 1=1 --", "5\") or 1=1 --", "5`) or 1=1 --",
			"5')) or 1=1 --", "5\")) or 1=1 --", "5`)) or 1=1 --",
			"5'))) or 1=1 --", "5\"))) or 1=1 --", "5`))) or 1=1 --"}

		for _, payload := range payloads {
			request, _ := http.NewRequest(http.MethodGet, "/filter?from_amount="+payload, nil)
			response := httptest.NewRecorder()

			s.FilterPayments(response, request)

			var payments []Payment
			_ = json.Unmarshal(response.Body.Bytes(), &payments)

			found := false
			for _, payment := range payments {
				if payment.ID == 3 {
					found = true
				}
			}

			if found {
				t.Errorf("Security test failed, sql injection present with payload %s\n Service return %s", payload, response.Body.String())
			}
		}
	})
}
