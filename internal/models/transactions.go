package models

import "log"

type Transaction struct {
	Vendor  string
	Amount  string
	Account string
}

func (t *Transaction) ApplyToEnvelope(envelope_id int) {
	log.Println("Adding to envelope with id %d", envelope_id)
}
