package utils

import (
	"encoding/json"
	"errors"
	"fmt"
	"log"
	"log/slog"
	"os"
)

func SaveJSON(path string, data interface{}) {
	jsonData, err := json.MarshalIndent(data, "", "  ")
	if err != nil {
		log.Fatal(err)
	}

	// Save the JSON data to a file
	err = os.WriteFile(path, jsonData, 0644) // 0644 grants read/write for owner, read-only for others
	if err != nil {
		log.Fatal(err)
	}
	slog.Info("Saved data as JSON", "path", path)
}

func ReadJSON(path string, data interface{}) error {
	file, err := os.Open(path)
	if err != nil {
		log.Fatalf("Error opening file '%s': %v", path, err)
	}
	defer file.Close()

	decoder := json.NewDecoder(file)
	if err := decoder.Decode(data); err != nil {
		slog.Error("Error decoding JSON", "path", path, "error", err)
		return err
	}
	return nil
}

func CheckFileExists(path string) (bool, error) {
	_, err := os.Stat(path)
	if errors.Is(err, os.ErrNotExist) {
		fmt.Printf("File '%s' does not exist.\n", path)
		return false, err
	} else if err != nil {
		log.Fatalf("Error checking file existence: %v", err)
		return false, err
	}
	return true, nil
}
