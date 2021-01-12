package rsa

import (
	"errors"
	"math"
	"math/big"
	"math/rand"
)

type Key struct {
	key int
	n   int
}

type KeyPair struct {
	Private Key
	Public  Key
}

func isPrime(n int) bool {
	if n < 2 {
		return false
	} else {
		for i := 2; i < n; i++ {
			if n%i == 0 {
				return false
			}
		}
		return true
	}
}

func gcd(a int, b int) int {
	for a != 0 && b != 0 {
		if a > b {
			a = a % b
		} else {
			b = b % a
		}
	}
	return a + b
}

func multiplicativeInverse(e int, phi int) int {

	var N int = phi
	var x, xx, y, yy = 1, 0, 0, 1
	var q int

	for e != 0 {
		q = phi / e
		phi, e = e, phi%e
		x, xx = xx, x-xx*q
		y, yy = yy, y-yy*q
	}
	return (int(math.Abs(float64(y+N))) % N)
}

func GenerateKeypair(p int, q int) (KeyPair, error) {
	if !isPrime(p) || !isPrime(q) {
		return KeyPair{}, errors.New("Both numbers must be prime.")
	} else if p == q {
		return KeyPair{}, errors.New("p and q can't be equal.")
	}

	// n = pq
	var n = p * q

	// phi = (p-1)(q-1)
	var phi = (p - 1) * (q - 1)

	e := rand.Intn(phi-1) + 1
	g := gcd(e, phi)
	for g != 1 {
		e = rand.Intn(phi-1) + 1
		g = gcd(e, phi)
	}

	d := multiplicativeInverse(e, phi)
	return KeyPair{Key{e, n}, Key{d, n}}, nil
}

func Encrypt(pk Key, plaintext string) []int {
	cipher := []int{}
	n := new(big.Int)
	for _, ch := range plaintext {
		n = new(big.Int).Exp(
			big.NewInt(int64(ch)), big.NewInt(int64(pk.key)), nil)
		n = new(big.Int).Mod(n, big.NewInt(int64(pk.n)))
		cipher = append(cipher, int(n.Int64()))
	}
	return cipher
}

func Decrypt(pk Key, cipher []int) string {
	plaintext := ""
	n := new(big.Int)
	for _, ch := range cipher {
		n = new(big.Int).Exp(
			big.NewInt(int64(ch)), big.NewInt(int64(pk.key)), nil)
		n = new(big.Int).Mod(n, big.NewInt(int64(pk.n)))
		plaintext += string(rune(int(n.Int64())))
	}
	return plaintext
}
