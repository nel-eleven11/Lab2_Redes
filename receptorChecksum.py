def fletcher16(data):
    c1, c2 = 0, 0
    for byte in data:
        c1 = (c1 + byte) % 255
        c2 = (c2 + c1) % 255
    return c1, c2

def main():
    with open("message.txt", "r") as f:
        contenido = f.read().strip()
    trama = contenido[:-4]
    c1_recv = int(contenido[-4:-2], 16)
    c2_recv = int(contenido[-2:], 16)
    c1, c2 = fletcher16([ord(x) for x in trama])
    if (c1, c2) == (c1_recv, c2_recv):
        print("No se detectaron errores. Trama recibida:", trama)
    else:
        print("Se detectó error. Trama descartada.")

if __name__ == "__main__":
    main()
