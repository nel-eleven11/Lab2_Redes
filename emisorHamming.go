package main

import (
	"fmt"
	"os"
	"strings"
)

func isValidBinary(s string) bool {
	for _, char := range s {
		if char != '0' && char != '1' {
			return false
		}
	}
	return true
}

func hammingEncode(data string) string {
	var encoded strings.Builder
	
	for i := 0; i < len(data); i += 4 {
		var block string
		if i+4 <= len(data) {
			block = data[i : i+4]
		} else {
			block = data[i:]
			for len(block) < 4 {
				block += "0"
			}
		}
		
		d := make([]int, 4)
		for j, bit := range block {
			if bit == '1' {
				d[j] = 1
			}
		}
		
		p1 := d[0] ^ d[1] ^ d[3]
		p2 := d[0] ^ d[2] ^ d[3]
		p3 := d[1] ^ d[2] ^ d[3]
		
		codeword := fmt.Sprintf("%d%d%d%d%d%d%d", p1, p2, d[0], p3, d[1], d[2], d[3])
		encoded.WriteString(codeword)
	}
	
	return encoded.String()
}

func main() {
	var binaryData string
	
	if len(os.Args) < 2 {
		fmt.Println("Uso: go run emisor.go \"cadena_binaria\"")
		fmt.Println("O simplemente ejecuta el programa para ingresar la cadena binaria interactivamente")
		
		fmt.Print("Ingresa la cadena binaria a codificar: ")
		fmt.Scanln(&binaryData)
		
		if binaryData == "" {
			fmt.Println("No se ingresó ninguna cadena binaria")
			return
		}
	} else {
		binaryData = os.Args[1]
	}
	
	if !isValidBinary(binaryData) {
		fmt.Println("Error: La entrada debe contener solo 0s y 1s")
		return
	}
	
	fmt.Printf("Datos binarios de entrada: %s\n", binaryData)
	fmt.Printf("Longitud: %d bits\n", len(binaryData))
	
	encoded := hammingEncode(binaryData)
	fmt.Printf("Mensaje codificado (Hamming): %s\n", encoded)
	fmt.Printf("Longitud codificada: %d bits\n", len(encoded))
}
