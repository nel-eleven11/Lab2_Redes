def codificador_convolucional(bits):
    state = 0
    out = []
    for bit in bits:
        bit = int(bit)
        # Estado extendido para los polinomios (3 bits)
        full_state = ((state << 1) | bit) & 0b111
        # G1 = 111, G2 = 101
        o1 = bit ^ ((full_state >> 1) & 1) ^ ((full_state >> 2) & 1)
        o2 = bit ^ ((full_state >> 2) & 1)
        out.append(str(o1))
        out.append(str(o2))
        # Actualiza el estado
        state = ((state << 1) | bit) & 0b11
    return ''.join(out)

def viterbi_decode(received):
    n = (len(received) // 2) - 2  # Número de bits originales (sin contar terminación)
    states = [0, 1, 2, 3]
    path_metrics = {s: float('inf') for s in range(4)}
    paths = {s: [] for s in range(4)}
    path_metrics[0] = 0

    transitions = {}
    for prev_state in range(4):
        for input_bit in [0, 1]:
            state = ((prev_state << 1) | input_bit) & 0b11
            full_state = ((prev_state << 1) | input_bit) & 0b111
            o1 = input_bit ^ ((full_state >> 1) & 1) ^ ((full_state >> 2) & 1)
            o2 = input_bit ^ ((full_state >> 2) & 1)
            transitions[(prev_state, input_bit)] = (state, [o1, o2])

    # Algoritmo de Viterbi
    for i in range(n + 2):  # Incluir los bits de terminación
        rec_bits = [int(received[2*i]), int(received[2*i+1])]
        new_metrics = {s: float('inf') for s in range(4)}
        new_paths = {s: [] for s in range(4)}
        input_bit_range = [0] if i >= n else [0, 1]  # Forzar 0 en bits de terminación
        for prev_state in range(4):
            if path_metrics[prev_state] < float('inf'):
                for input_bit in input_bit_range:
                    state, out_bits = transitions[(prev_state, input_bit)]
                    dist = sum([ob != rb for ob, rb in zip(out_bits, rec_bits)])
                    metric = path_metrics[prev_state] + dist
                    if metric < new_metrics[state]:
                        new_metrics[state] = metric
                        new_paths[state] = paths[prev_state] + [input_bit]
        path_metrics = new_metrics
        paths = new_paths

    # Encontrar el mejor camino
    best_state = min(path_metrics, key=lambda s: path_metrics[s])
    best_path = paths[best_state][:n]  # Solo los bits originales
    full_path = paths[best_state]  # Incluir bits de terminación
    errores = path_metrics[best_state]

    # Generar la secuencia recodificada
    recodificada = codificador_convolucional(full_path)
    print("RECODIFICADA:", recodificada)  # Para depuración
    error_positions = []
    for i in range(len(received)):
        if i < len(recodificada) and received[i] != recodificada[i]:
            error_positions.append(i)

    return best_path, errores, error_positions

def main():
    with open("message.txt", "r") as f:
        codificada = f.read().strip()
    decodificada, errores, error_positions = viterbi_decode(codificada)
    print("Trama decodificada:", ''.join(str(b) for b in decodificada))
    if errores == 0:
        print("No se detectaron errores.")
    else:
        print(f"Se corrigieron {errores} bit(s) durante la decodificación.")
        print("Posiciones corregidas en la trama codificada:", error_positions)

if __name__ == "__main__":
    main()