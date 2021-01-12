package caesar

import "math"

func EncryptCaesar(plaintext string, shift int) string {

	const Max_ABC = int('Z')
	const Min_ABC = int('A')
	const Max_abc = int('z')
	const Min_abc = int('a')

	var ciphertext string

	for _, i := range plaintext {
		if int(i) >= Min_ABC && int(i) <= Max_ABC-shift {
			ciphertext += string(rune(int(i) + shift))
		} else if int(i) >= Min_abc && int(i) <= Max_abc-shift {
			ciphertext += string(rune(int(i) + shift))
		} else if int(i) >= Max_ABC-shift && int(i) <= Min_abc {
			ciphertext += string(rune(Min_ABC + shift - Max_ABC + int(i) - 1))
		} else if int(i) >= Min_abc-shift && int(i) <= Max_abc {
			ciphertext += string(rune(Min_abc + shift - Max_abc + int(i) - 1))
		} else {
			ciphertext += string(i)
		}
	}
	return ciphertext
}

func DecryptCaesar(ciphertext string, shift int) string {

	const Max_ABC = int('Z')
	const Min_ABC = int('A')
	const Max_abc = int('z')
	const Min_abc = int('a')

	var plaintext string

	for _, i := range ciphertext {
		if int(i) >= Min_ABC+shift && int(i) <= Max_ABC {
			plaintext += string(rune(int(i) - shift))
		} else if int(i) >= Min_abc+shift && int(i) <= Max_abc {
			plaintext += string(rune(int(i) - shift))
		} else if int(i) >= Min_ABC && int(i) <= Min_ABC+shift {
			plaintext += string(rune(Max_ABC - int(math.Abs(float64(int(i)-shift-Min_ABC))) + 1))
		} else if int(i) >= Min_abc && int(i) <= Min_abc+shift {
			plaintext += string(rune(Max_abc - int(math.Abs(float64(int(i)-shift-Min_abc))) + 1))
		} else {
			plaintext += string(i)
		}
	}
	return plaintext
}
