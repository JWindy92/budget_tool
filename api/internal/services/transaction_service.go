package services

import (
	"errors"
	"log/slog"

	"github.com/JWindy92/budget_tool/internal/models"
	"gorm.io/gorm"
)

var ErrTransactionExists = errors.New("transaction with this name already exists")

type TransactionService struct {
	DB *gorm.DB
}

func NewTransactionService(conn *gorm.DB) *TransactionService {
	return &TransactionService{DB: conn}
}

func (s *TransactionService) NewTransaction(trx *models.Transaction) error {
	slog.Info("Creating new Transaction")
	return s.DB.Create(trx).Error
}
