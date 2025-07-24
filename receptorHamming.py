import sys

def hamming_decode(encoded_data):
    decoded_bits = []
    
    for i in range(0, len(encoded_data), 7):
        if i + 7 <= len(encoded_data):
            block = encoded_data[i:i+7]
        else:
            block = encoded_data[i:]
            while len(block) < 7:
                block += '0'
        
        bits = [int(b) for b in block]
        
        p1, p2, d1, p3, d2, d3, d4 = bits
        
        s1 = p1 ^ d1 ^ d2 ^ d4  
        s2 = p2 ^ d1 ^ d3 ^ d4  
        s3 = p3 ^ d2 ^ d3 ^ d4  
        
        error_pos = s1 + 2*s2 + 4*s3
        
        if error_pos != 0:
            print(f"Error detectado en posición: {error_pos}")
            if error_pos <= 7:
                bits[error_pos - 1] ^= 1
                p1, p2, d1, p3, d2, d3, d4 = bits
        
        data_bits = [d1, d2, d3, d4]
        decoded_bits.extend(data_bits)
    
    return ''.join(map(str, decoded_bits))

def main():
    if len(sys.argv) < 2:
        print("Uso: python receptor.py <cadena_binaria_codificada>")
        print("O ingresa la cadena binaria codificada cuando se solicite:")
        
        encoded_message = input("Ingresa la cadena binaria codificada: ").strip()
        
        if not encoded_message:
            print("No se ingresó ninguna cadena binaria codificada")
            return
    else:
        encoded_message = sys.argv[1]
    
    print(f"Cadena binaria codificada recibida: {encoded_message}")
    print(f"Longitud: {len(encoded_message)} bits")
    
    if not all(c in '01' for c in encoded_message):
        print("Error: El mensaje debe contener solo 0s y 1s")
        return
    
    decoded_binary = hamming_decode(encoded_message)
    print(f"Cadena binaria decodificada: {decoded_binary}")
    print(f"Longitud decodificada: {len(decoded_binary)} bits")

if __name__ == "__main__":
    main()
