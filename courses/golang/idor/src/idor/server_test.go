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

func TestIDORHandler(t *testing.T) {
	InitDatabase()
	insertTestDataIntoDatabase()
	database := GetDatabase()
	s := Server{DB: database}

	t.Run("functional all payments test", func(t *testing.T) {
		request, _ := http.NewRequest(http.MethodGet, "/payments", nil)
		response := httptest.NewRecorder()

		s.ShowAllPayments(response, request)

		var payments []Payment
		_ = json.Unmarshal(response.Body.Bytes(), &payments)

		if len(payments) != 3 || payments[0].ID != 1 || payments[1].ID != 2 || payments[2].ID != 4 {
			t.Errorf("Functional test failed, /payments returns %s", response.Body.String())
		}
	})

	t.Run("functional one payment test", func(t *testing.T) {
		request, _ := http.NewRequest(http.MethodGet, "/show_payment?payment_id=2", nil)
		response := httptest.NewRecorder()

		s.ShowPayment(response, request)

		var payment Payment
		_ = json.Unmarshal(response.Body.Bytes(), &payment)

		if payment.ID != 2 {
			t.Errorf("Functional test failed, /show_payment returns %s", response.Body.String())
		}
	})

	t.Run("idor one payment test", func(t *testing.T) {
		request, _ := http.NewRequest(http.MethodGet, "/show_payment?payment_id=3", nil)
		response := httptest.NewRecorder()

		s.ShowPayment(response, request)

		var payment Payment
		_ = json.Unmarshal(response.Body.Bytes(), &payment)

		if payment.ID == 3 {
			t.Errorf("Security test failed, /show_payment returns %s", response.Body.String())
		}
	})
}
