package utils

import (
	"encoding/json"
	"fmt"
)

func PrettyPrint(s interface{}) {
	b, err := json.MarshalIndent(s, "", "  ")
	if err != nil {
		fmt.Println("PrettyPrint error:", err)
		return
	}
	fmt.Println(string(b))
}
