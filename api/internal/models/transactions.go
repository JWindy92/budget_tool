package models

import (
	"log"

	"gorm.io/gorm"
)

type Transaction struct {
	gorm.Model
	ID          string `gorm:"unique" json:"id"`
	Posted      int64  `json:"posted"`
	Amount      string `json:"amount"`
	Description string `json:"description"`
	// Vendor      string
	// Amount      float64
	AccountID string
}

func (t *Transaction) ApplyToEnvelope(envelope_id int) {
	log.Println("Adding to envelope with id %d", envelope_id)
}
