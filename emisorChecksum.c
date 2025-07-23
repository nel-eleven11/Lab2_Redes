#include <stdio.h>
#include <string.h>
#include <stdint.h>

void fletcher16(const uint8_t *data, int len, uint16_t *c1, uint16_t *c2) {
    *c1 = 0;
    *c2 = 0;
    for (int i=0; i<len; i++) {
        *c1 = (*c1 + data[i]) % 255;
        *c2 = (*c2 + *c1) % 255;
    }
}

int main() {
    char trama[256];
    printf("Ingrese la trama (en binario): ");
    scanf("%s", trama);
    uint16_t c1, c2;
    fletcher16((uint8_t *)trama, strlen(trama), &c1, &c2);
    FILE *f = fopen("message.txt", "w");
    fprintf(f, "%s%02X%02X", trama, c1, c2);
    fclose(f);
    printf("Mensaje + checksum: %s%02X%02X\n", trama, c1, c2);
    return 0;
}
