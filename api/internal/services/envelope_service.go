package services

import (
	"errors"
	"log/slog"

	"github.com/JWindy92/budget_tool/internal/models"
	"gorm.io/gorm"
)

var ErrEnvelopeExists = errors.New("envelope with this name already exists")

type EnvelopeService struct {
	DB *gorm.DB
}

func NewEnvelopeService(conn *gorm.DB) *EnvelopeService {
	return &EnvelopeService{DB: conn}
}

func (s *EnvelopeService) NewEnvelope(env *models.Envelope) error {
	slog.Info("Creating new envelope")
	return s.DB.Create(env).Error
}
