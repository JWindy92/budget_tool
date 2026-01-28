package services

import (
	"encoding/json"
	"fmt"
	"io"
	"log"
	"net/http"
	"os"
	"slices"

	"github.com/JWindy92/budget_tool/internal/config"
	"github.com/JWindy92/budget_tool/internal/models"
	"github.com/JWindy92/budget_tool/internal/utils"
)

const testDataPath = "./test/data/simpleFinResp.json"

// type SimpleFINAccount struct {
// 	Org struct {
// 		Domain string `json:"domain"`
// 		URL    string `json:"sfin-url"`
// 	} `json:"org"`
// 	ID               string               `json:"id"`
// 	Name             string               `json:"name"`
// 	Currency         string               `json:"currency"`
// 	Balance          string               `json:"balance"`
// 	AvailableBalance string               `json:"available-balance,omitempty"`
// 	BalanceDate      int64                `json:"balance-date"`
// 	Transactions     []models.Transaction `json:"transactions,omitempty"`
// }

type SimpleFinAccountResponse struct {
	Errors   []string                  `json:"errors"`
	Accounts []models.SimpleFINAccount `json:"accounts"`
}

type AccountSet struct {
	Accounts []models.SimpleFINAccount `json:"accounts"`
}

func FetchAccounts(sfar *SimpleFinAccountResponse) {
	accessUrl := os.Getenv("ACCESS_URL")
	accountsResp, err := http.Get(accessUrl + "/accounts?start-date=978360153")
	if err != nil {
		fmt.Println("Failed to fetch accounts:", err)
		return
	}
	defer accountsResp.Body.Close()

	body, _ := io.ReadAll(accountsResp.Body)

	// var simpleFinResp SimpleFinAccountResponse
	if err := json.Unmarshal(body, sfar); err != nil {
		fmt.Println("Failed to parse response:", err)
		return
	}

	if len(sfar.Errors) > 0 {
		fmt.Println("Errors from API:", sfar.Errors)
	}
	utils.SaveJSON(testDataPath, sfar)
}

func LoadAccountData(svc AccountService, startDate string, endDate string) {
	cfg := config.LoadConfig()

	var simpleFinResp SimpleFinAccountResponse
	exists, err := utils.CheckFileExists(testDataPath)
	if err != nil {
		log.Println(err)
	}
	if exists {
		utils.ReadJSON(testDataPath, &simpleFinResp)
	} else {
		FetchAccounts(&simpleFinResp)
	}
	// utils.PrettyPrint(simpleFinResp)
	var trackedAccounts AccountSet
	for _, acct := range simpleFinResp.Accounts {
		if slices.Contains(cfg.TrackedAccounts, acct.Name) {
			trackedAccounts.Accounts = append(trackedAccounts.Accounts, acct)
		}
	}
	for _, acct := range trackedAccounts.Accounts {
		svc.NewAccount(&models.Account{acct})
		fmt.Printf("Account %s (%s): Balance: %s %s\n",
			acct.Name, acct.ID, acct.Balance, acct.Currency)
		for _, txn := range acct.Transactions {
			fmt.Printf("  - %s: %s on %d\n", txn.Description, txn.Amount, txn.Posted)
		}
	}
}
