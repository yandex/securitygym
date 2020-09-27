package main

import (
	"database/sql"
	"encoding/json"
	"net/http"
	"strconv"
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

func (s *Server) FilterPayments(w http.ResponseWriter, req *http.Request) {
	currentUserID := strconv.Itoa(GetCurrentUserID())
	amount := req.URL.Query().Get("from_amount")

	payments := make([]Payment, 0)
	rows, err := s.DB.Query("SELECT id, amount, user_id, description FROM payments " +
		"WHERE user_id = " + currentUserID + " AND amount > " + amount)
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
