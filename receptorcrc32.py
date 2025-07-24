#!/usr/bin/env python3
import sys

CRC32_POLYNOMIAL = "100000100110000010001110110110111"

def perform_crc_division(dividend, divisor):
    temp = list(dividend)
    divisor_len = len(divisor)
    
    for i in range(len(temp) - divisor_len + 1):
        if temp[i] == '1':
            for j in range(divisor_len):
                if temp[i + j] == divisor[j]:
                    temp[i + j] = '0'
                else:
                    temp[i + j] = '1'
    
    remainder = ''.join(temp[-32:])
    
    if len(remainder) < 32:
        remainder = '0' * (32 - len(remainder)) + remainder
    
    return remainder

def calculate_crc32(data):
    padded_data = data + '0' * 32
    remainder = perform_crc_division(padded_data, CRC32_POLYNOMIAL)
    return remainder

def verify_crc(message):
    if len(message) < 32:
        return False, "", "", ""
    
    data_bits = message[:-32]
    received_crc = message[-32:]
    
    calculated_crc = calculate_crc32(data_bits)
    
    is_valid = (received_crc == calculated_crc)
    
    return is_valid, data_bits, received_crc, calculated_crc

def verify_crc_alternative(message):
    remainder = perform_crc_division(message, CRC32_POLYNOMIAL)
    is_valid = all(bit == '0' for bit in remainder)
    return is_valid, remainder

def main():
    if len(sys.argv) < 2:
        print("Uso: python receptor_crc.py <cadena_binaria_con_crc>")
        print("O ingresa la cadena binaria cuando se solicite:")
        
        received_message = input("Ingresa la cadena binaria con CRC-32: ").strip()
        
        if not received_message:
            print("No se ingresó ninguna cadena binaria")
            return
    else:
        received_message = sys.argv[1]
    
    print(f"Mensaje recibido: {received_message}")
    print(f"Longitud total: {len(received_message)} bits")
    
    if not all(c in '01' for c in received_message):
        print("Error: El mensaje debe contener solo 0s y 1s")
        return
    
    if len(received_message) < 32:
        print("Error: El mensaje debe tener al menos 32 bits (CRC-32)")
        return
    
    is_valid, data_bits, received_crc, calculated_crc = verify_crc(received_message)
    
    print(f"Datos extraídos: {data_bits}")
    print(f"Longitud de datos: {len(data_bits)} bits")
    print(f"CRC recibido: {received_crc}")
    print(f"CRC calculado: {calculated_crc}")
    
    is_valid_alt, remainder = verify_crc_alternative(received_message)
    print(f"Resto de división completa: {remainder}")
    
    if is_valid and is_valid_alt:
        print("✓ MENSAJE VÁLIDO - No se detectaron errores")
        print(f"Datos originales: {data_bits}")
    elif is_valid:
        print("✓ MENSAJE VÁLIDO (método 1) - No se detectaron errores")
        print(f"Datos originales: {data_bits}")
    elif is_valid_alt:
        print("✓ MENSAJE VÁLIDO (método 2) - No se detectaron errores")
        print(f"Datos originales: {data_bits}")
    else:
        print("✗ ERROR DETECTADO - El mensaje está corrupto")
        print("Los datos pueden contener errores de transmisión")

if __name__ == "__main__":
    main()
