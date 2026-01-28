package config

import (
	"log"

	"github.com/joho/godotenv"
)

type Config struct {
	TrackedAccounts []string
}

func LoadConfig() Config {
	err := godotenv.Load()
	if err != nil {
		log.Fatal("Error loading .env file")
	}
	return Config{
		TrackedAccounts: []string{
			"Chase Sapphire Preferred",
			"One Deposit Checking",
			"One Deposit Savings",
			"Mortgage",
		},
	}
}
