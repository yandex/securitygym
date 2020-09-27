package main

import (
	"database/sql"
	"net/http"

	_ "github.com/mattn/go-sqlite3"
)

func InitDatabase() {
	database, _ := sql.Open("sqlite3", "./payments.db")
	statement, _ := database.Prepare("CREATE TABLE IF NOT EXISTS payments (id INTEGER PRIMARY KEY, amount DECIMAL(10,2) NOT NULL, user_id INTEGER, description TEXT)")
	statement.Exec()
	database.Close()
}

func GetDatabase() *sql.DB {
	database, _ := sql.Open("sqlite3", "./payments.db")
	return database
}

func GetCurrentUserID() int {
	return 1
}

func main() {
	db := GetDatabase()
	s := Server{DB: db}
	mux := http.NewServeMux()
	mux.HandleFunc("/payments", s.ShowAllPayments)
	mux.HandleFunc("/show_payment", s.ShowPayment)
	server := http.Server{Handler: mux, Addr: ":80"}
	server.ListenAndServe()
}
