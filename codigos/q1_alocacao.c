/* Questao 1: duracao estatica e alocacao dinamica. */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <inttypes.h>

int main(void) {
    /* static garante duracao estatica; um array local sem static seria automatico. */
    static int fixo[5] = {1, 2, 3, 4, 5};
    int *dinamico = malloc(10 * sizeof *dinamico);
    if (dinamico == NULL) {
        fprintf(stderr, "Erro: memoria insuficiente.\n");
        return EXIT_FAILURE;
    }
    for (int i = 0; i < 10; ++i) dinamico[i] = 10 + i;
    puts("ARRAY ESTATICO: 5 inteiros");
    for (int i = 0; i < 5; ++i)
        printf("[%d] valor=%2d endereco=%p\n", i, fixo[i], (void *)&fixo[i]);
    puts("ARRAY DINAMICO: 10 inteiros");
    for (int i = 0; i < 10; ++i)
        printf("[%d] valor=%2d endereco=%p\n", i, dinamico[i], (void *)&dinamico[i]);
    /* Nao subtrair ponteiros de objetos distintos: seria comportamento indefinido.
       uintptr_t permite comparar suas representacoes numericas neste ambiente.
       A conversao depende da implementacao; nao mede distancia fisica da RAM. */
    uintptr_t a = (uintptr_t)(void *)fixo;
    uintptr_t b = (uintptr_t)(void *)dinamico;
    uintptr_t distancia = a >= b ? a - b : b - a;
    printf("Diferenca numerica absoluta dos enderecos: %" PRIuPTR "\n", distancia);
    puts("Enderecos virtuais; o layout depende do sistema e da execucao.");
    free(dinamico);
    dinamico = NULL;
    puts("Memoria dinamica liberada.");
    return EXIT_SUCCESS;
}
