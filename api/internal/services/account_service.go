package services

import (
	"errors"
	"log"
	"log/slog"

	"github.com/JWindy92/budget_tool/internal/models"
	"gorm.io/gorm"
	"gorm.io/gorm/clause"
)

var ErrAccountExists = errors.New("account with this name already exists")

type AccountService struct {
	Accounts []models.Account
	DB       *gorm.DB
}

func NewAccountService(conn *gorm.DB) *AccountService {
	return &AccountService{DB: conn}
}

func (s *AccountService) NewAccount(acct *models.Account) error {
	slog.Info("Creating new account")
	return s.DB.Clauses(clause.OnConflict{
		UpdateAll: true,
	}).Create(&acct).Error
}

func (s *AccountService) GetAccounts() ([]models.Account, error) {
	var accts []models.Account
	result := s.DB.Find(&accts)
	if result.Error != nil {
		return accts, result.Error
	}
	slog.Info("Fetched all accounts", "Num Accounts", len(accts))
	s.Accounts = accts
	return accts, nil
}

func (s *AccountService) GetAccountByName(name string) (models.Account, error) {
	var acct models.Account
	result := s.DB.Where("name = ?", name).First(&acct)
	if result.Error != nil {
		return acct, result.Error
	}
	return acct, nil
}

func (s *AccountService) GetAccountTransactions(acct models.Account) (models.Account, error) {
	var transactions []models.Transaction
	err := s.DB.Model(&acct).Association("Transactions").Find(&transactions)
	if err != nil {
		log.Fatal(err)
		return acct, err
	}
	slog.Info("Fetched account transactions", "account", acct.Name, "trx_count", len(transactions))
	acct.Transactions = transactions
	return acct, nil
}
