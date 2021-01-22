package vigenere

import (
	"math"
	"strings"
)

func EncryptVigenere(plaintext string, keyword string) string {

	const Max_ABC = int('Z')
	const Min_ABC = int('A')
	const Max_abc = int('z')
	const Min_abc = int('a')

	var key string

	if len(plaintext) > len(keyword) {
		key = strings.ToLower(strings.Repeat(keyword, (1 + len(plaintext)/len(keyword))))
	} else {
		key = strings.ToLower(keyword)
	}

	var shifts []int

	for i := 0; i < len(key); i++ {
		shifts = append(shifts, (int(key[i]) - int('a')))
	}

	var ciphertext string

	for i := 0; i < len(plaintext); i++ {
		var plain_letter int = int(plaintext[i])
		var shift int = int(shifts[i])

		if plain_letter >= Min_ABC && plain_letter <= Max_ABC-shifts[i] {
			ciphertext += string(rune(plain_letter + shift))
		} else if plain_letter >= Min_abc && plain_letter <= Max_abc-shift {
			ciphertext += string(rune(plain_letter + shift))
		} else if plain_letter >= Max_ABC-shift && plain_letter <= Min_abc {
			ciphertext += string(rune(Min_ABC - 1 + shift - Max_ABC + plain_letter))
		} else if plain_letter >= Min_abc-shift && plain_letter <= Max_abc {
			ciphertext += string(rune(Min_abc - 1 + shift - Max_abc + plain_letter))
		} else {
			ciphertext += string(rune(plain_letter))
		}
	}
	return ciphertext
}

func DecryptVigenere(ciphertext string, keyword string) string {

	const Max_ABC = int('Z')
	const Min_ABC = int('A')
	const Max_abc = int('z')
	const Min_abc = int('a')

	var key string

	if len(ciphertext) > len(keyword) {
		key = strings.ToLower(strings.Repeat(keyword, (1 + len(ciphertext)/len(keyword))))
	} else {
		key = strings.ToLower(keyword)
	}

	var shifts []int

	for i := 0; i < len(key); i++ {
		shifts = append(shifts, (int(key[i]) - int('a')))
	}

	var plaintext string

	for i := 0; i < len(ciphertext); i++ {
		var ciph_letter int = int(ciphertext[i])
		var shift int = int(shifts[i])

		if ciph_letter >= Min_ABC+shift && ciph_letter <= Max_ABC {
			plaintext += string(rune(ciph_letter - shift))
		} else if ciph_letter >= Min_abc+shift && ciph_letter <= Max_abc {
			plaintext += string(rune(ciph_letter - shift))
		} else if ciph_letter >= Min_ABC && ciph_letter <= Min_ABC+shift {
			plaintext += string(rune(Max_ABC - int(math.Abs(float64(ciph_letter-shift-Min_ABC))) + 1))
		} else if ciph_letter >= Min_abc && ciph_letter <= Min_abc+shift {
			plaintext += string(rune(Max_abc - int(math.Abs(float64(ciph_letter-shift-Min_abc))) + 1))
		} else {
			plaintext += string(rune(ciph_letter))
		}
	}
	return plaintext
}
