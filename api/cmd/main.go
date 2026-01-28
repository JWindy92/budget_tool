package main

import (
	"log/slog"

	"github.com/JWindy92/budget_tool/internal/models"
	"github.com/JWindy92/budget_tool/internal/services"
	"github.com/JWindy92/budget_tool/internal/utils"
	"github.com/JWindy92/go_app_utils/pkg/database"
	"github.com/JWindy92/go_app_utils/pkg/logging"
)

func main() {
	logging.InitLogger()
	slog.Info("Logger initialized")
	slog.Info("Hello budget tool!")
	sqlite := database.SQLiteImpl{}
	sqlite.ConnectDB("test.db")
	sqlite.RunAutoMigrate(&models.Envelope{}, &models.Transaction{}, &models.SimpleFINAccount{})

	// envSvc := services.NewEnvelopeService(sqlite.DB)
	acctSvc := services.NewAccountService(sqlite.DB)
	// trxSvc := services.NewTransactionService(sqlite.DB)
	services.LoadAccountData(*acctSvc)
	// acctSvc.GetAccounts()
	// // utils.PrettyPrint(acctSvc.Accounts)
	acct, _ := acctSvc.GetAccountByName("One Deposit Checking")
	acct, _ = acctSvc.GetAccountTransactions(acct)

	utils.PrettyPrint(acct)
}
