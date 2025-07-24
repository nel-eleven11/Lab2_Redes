package main

import (
	"fmt"
	"os"
	"strings"
)

const CRC32_POLYNOMIAL = "100000100110000010001110110110111"

func isValidBinary(s string) bool {
	for _, char := range s {
		if char != '0' && char != '1' {
			return false
		}
	}
	return true
}

func xorBinary(a, b string) string {
	result := make([]byte, len(a))
	for i := 0; i < len(a); i++ {
		if a[i] == b[i] {
			result[i] = '0'
		} else {
			result[i] = '1'
		}
	}
	return string(result)
}

func performCRCDivision(dividend, divisor string) string {
	temp := dividend
	divisorLen := len(divisor)
	
	for i := 0; i <= len(temp)-divisorLen; i++ {
		if temp[i] == '1' {
			for j := 0; j < divisorLen; j++ {
				if temp[i+j] == divisor[j] {
					temp = temp[:i+j] + "0" + temp[i+j+1:]
				} else {
					temp = temp[:i+j] + "1" + temp[i+j+1:]
				}
			}
		}
	}
	
	if len(temp) >= 32 {
		return temp[len(temp)-32:]
	} else {
		return strings.Repeat("0", 32-len(temp)) + temp
	}
}

func calculateCRC32(data string) string {
	paddedData := data + strings.Repeat("0", 32)
	remainder := performCRCDivision(paddedData, CRC32_POLYNOMIAL)
	return remainder
}

func createCRCMessage(data string) string {
	crc := calculateCRC32(data)
	return data + crc
}

func main() {
	var binaryData string
	
	if len(os.Args) < 2 {
		fmt.Println("Uso: go run emisor_crc.go \"cadena_binaria\"")
		fmt.Println("O simplemente ejecuta el programa para ingresar la cadena binaria interactivamente")
		
		fmt.Print("Ingresa la cadena binaria a codificar con CRC-32: ")
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
	fmt.Printf("Longitud de datos: %d bits\n", len(binaryData))
	
	crc := calculateCRC32(binaryData)
	fmt.Printf("CRC-32 calculado: %s\n", crc)
	
	message := createCRCMessage(binaryData)
	fmt.Printf("Mensaje con CRC-32: %s\n", message)
	fmt.Printf("Longitud total: %d bits (datos: %d + CRC: 32)\n", len(message), len(binaryData))
}
