def codificador_convolucional(bits):
    state = 0
    out = []
    for bit in bits:
        bit = int(bit)
        o1 = bit ^ ((state >> 1) & 1) ^ ((state >> 2) & 1)
        o2 = bit ^ ((state >> 2) & 1)
        out.append(str(o1))
        out.append(str(o2))
        state = ((state << 1) | bit) & 0b111
    return ''.join(out)

def viterbi_decode(received):
    n = len(received) // 2  # Número de bits originales
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

    trellis = []
    for i in range(n):
        rec_bits = [int(received[2*i]), int(received[2*i+1])]
        new_metrics = {s: float('inf') for s in range(4)}
        new_paths = {s: [] for s in range(4)}
        for prev_state in range(4):
            if path_metrics[prev_state] < float('inf'):
                for input_bit in [0, 1]:
                    state, out_bits = transitions[(prev_state, input_bit)]
                    dist = sum([ob != rb for ob, rb in zip(out_bits, rec_bits)])
                    metric = path_metrics[prev_state] + dist
                    if metric < new_metrics[state]:
                        new_metrics[state] = metric
                        new_paths[state] = paths[prev_state] + [input_bit]
        path_metrics = new_metrics
        paths = new_paths
        trellis.append(paths)  # For traceback

    best_state = min(path_metrics, key=lambda s: path_metrics[s])
    best_path = paths[best_state]
    errores = path_metrics[best_state]

    # Ahora compara la secuencia original (best_path) codificada vs. la recibida
    recodificada = codificador_convolucional(best_path)
    error_positions = []
    for i in range(n):
        rec_pair = received[2*i:2*i+2]
        cod_pair = recodificada[2*i:2*i+2]
        if rec_pair != cod_pair:
            error_positions.append(i)  # posición en la secuencia original

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
        print("Posiciones corregidas en la trama original:", error_positions)

if __name__ == "__main__":
    main()
