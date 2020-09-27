package main

import (
	"database/sql"
	"encoding/json"
	"net/http"
)

type Server struct {
	DB *sql.DB
}

type Payment struct {
	ID          int    `json:"id" db:"id"`
	Amount      int    `json:"amount" db:"amount"`
	UserID      int    `json:"user_id" db:"user_id"`
	Description string `json:"description" db:"description"`
}

func (s *Server) ShowAllPayments(w http.ResponseWriter, req *http.Request) {
	currentUserID := GetCurrentUserID()
	payments := make([]Payment, 0)
	rows, err := s.DB.Query("SELECT id, amount, user_id, description FROM payments "+
		"WHERE user_id = ?", currentUserID)
	if err == nil {
		for rows.Next() {
			var payment Payment
			rows.Scan(&payment.ID, &payment.Amount, &payment.UserID, &payment.Description)
			payments = append(payments, payment)
		}
	}
	j, _ := json.Marshal(payments)
	w.Write(j)
}

func (s *Server) ShowPayment(w http.ResponseWriter, req *http.Request) {
	paymentID := req.URL.Query().Get("payment_id")
	var payment Payment
	err := s.DB.QueryRow("SELECT id, amount, user_id, description FROM payments "+
		"WHERE id = ?", paymentID).Scan(&payment.ID, &payment.Amount, &payment.UserID, &payment.Description)
	if err != nil {
		return
	}
	j, _ := json.Marshal(payment)
	w.Write(j)
}
