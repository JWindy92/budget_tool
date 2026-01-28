package models

import (
	"gorm.io/gorm"
)

type Account struct {
	SimpleFINAccount
}

// type Account struct {
// 	gorm.Model
// 	AccountName  string `gorm:"unique"`
// 	Balance      float64
// 	Transactions []Transaction `gorm:"foreignKey:"AccountID"`
// }

type SimpleFINAccount struct {
	gorm.Model
	// Org struct {
	// 	Domain string `json:"domain"`
	// 	URL    string `json:"sfin-url"`
	// } `json:"org"`
	ID               string        `gorm:"unique" json:"id"`
	Name             string        `json:"name"`
	Currency         string        `json:"currency"`
	Balance          string        `json:"balance"`
	AvailableBalance string        `json:"available-balance,omitempty"`
	BalanceDate      int64         `json:"balance-date"`
	Transactions     []Transaction `gorm:"foreignKey:AccountID" json:"transactions"`
}

func (SimpleFINAccount) TableName() string {
	return "accounts"
}
