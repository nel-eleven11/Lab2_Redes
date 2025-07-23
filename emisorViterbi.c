#include <stdio.h>
#include <string.h>

int main() {
    char trama[256];
    char salida[512];
    printf("Ingrese la trama en binario: ");
    scanf("%s", trama);
    int n = strlen(trama);
    int state = 0; // Estado: los últimos 2 bits
    int j = 0;
    for (int i = 0; i < n; i++) {
        int bit = trama[i] - '0';

        // Construye el estado extendido para los polinomios (3 bits)
        int full_state = ((state << 1) | bit) & 0b111; // K=3

        // G1 = 111, G2 = 101
        int o1 = bit ^ ((full_state >> 1) & 1) ^ ((full_state >> 2) & 1);
        int o2 = bit ^ ((full_state >> 2) & 1);

        salida[j++] = o1 + '0';
        salida[j++] = o2 + '0';

        // Actualiza el estado a los últimos 2 bits (memoria)
        state = ((state << 1) | bit) & 0b11; // solo 2 bits de estado
    }
    salida[j] = '\0';

    FILE *f = fopen("message.txt", "w");
    fprintf(f, "%s", salida);
    fclose(f);

    printf("Trama codificada: %s\n", salida);
    return 0;
}
