package models

import "gorm.io/gorm"

type Envelope struct {
	gorm.Model
	Name    string
	Balance float64
	Target  float64
}
