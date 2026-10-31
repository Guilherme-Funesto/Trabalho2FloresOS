/* Um milhao de vidas de variaveis locais vs malloc/free de um inteiro.
   Nao mede apenas o alocador: inclui chamada, escrita, leitura e controle.
   Compile SEM otimizacao (-O0 no GCC/Clang) para preservar o experimento.
   volatile torna os acessos observaveis; noinline evita integrar as funcoes.
   Tempos variam com CPU, carga, compilador, cache e alocador. O heap pode
   reutilizar o mesmo bloco; nao ha um milhao de objetos simultaneamente. */
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#if defined(_MSC_VER)
#define NOINLINE __declspec(noinline)
#elif defined(__GNUC__) && !defined(__TINYC__)
#define NOINLINE __attribute__((noinline))
#else
#define NOINLINE
#endif
#define N 1000000
#define REPETICOES 7

static NOINLINE int local(int valor) {
    volatile int x = valor;
    return x; /* A duracao automatica termina no retorno. */
}

static NOINLINE int heap(int valor) {
    int *p = malloc(sizeof *p);
    if (!p) { fputs("Erro de alocacao.\n", stderr); exit(EXIT_FAILURE); }
    *(volatile int *)p = valor;
    int resultado = *(volatile int *)p;
    free(p);
    return resultado;
}

static double medir(int (*operacao)(int), unsigned long long *soma) {
    clock_t inicio = clock();
    if (inicio == (clock_t)-1) { fputs("Relogio indisponivel.\n", stderr); exit(1); }
    unsigned long long total = 0;
    for (int i = 0; i < N; i++) total += (unsigned int)operacao(i);
    clock_t fim = clock();
    if (fim == (clock_t)-1) { fputs("Relogio indisponivel.\n", stderr); exit(1); }
    *soma = total;
    return (double)(fim - inicio) / CLOCKS_PER_SEC;
}

int main(void) {
    unsigned long long s1 = 0, s2 = 0;
    double total_local = 0, total_heap = 0;
    /* Aquecimento excluido da media. */
    for (int i = 0; i < 10000; i++) { s1 += local(i); s2 += heap(i); }
    printf("Operacoes por teste: %d; repeticoes: %d; CLOCKS_PER_SEC=%ld\n",
           N, REPETICOES, (long)CLOCKS_PER_SEC);
    puts("Rodada | Local/pilha (s) | Heap (s)");
    for (int r = 0; r < REPETICOES; r++) {
        double a, b;
        /* Alternar a ordem reduz o vies de aquecimento/carga progressiva. */
        if (r % 2 == 0) { a = medir(local, &s1); b = medir(heap, &s2); }
        else { b = medir(heap, &s2); a = medir(local, &s1); }
        if (s1 != 499999500000ULL || s2 != s1) return EXIT_FAILURE;
        printf("%6d | %15.6f | %.6f\n", r + 1, a, b);
        total_local += a; total_heap += b;
    }
    double media_local = total_local / REPETICOES;
    double media_heap = total_heap / REPETICOES;
    printf("Media local: %.9f s\nMedia heap: %.9f s\n", media_local, media_heap);
    if (media_local > 0) {
        printf("Tempo adicional do heap relativo ao local: %.2f%%\n",
               (media_heap - media_local) / media_local * 100);
        printf("Razao heap/local: %.2fx\n", media_heap / media_local);
    } else puts("Resolucao insuficiente: percentual indefinido.");
    printf("Checksums: %llu / %llu\n", s1, s2);
    puts("Resultado depende do ambiente; nao representa custo puro de alocacao.");
    /* Em geral, o quadro local usa ajuste do stack pointer, enquanto malloc/free
       consultam estruturas do alocador. Isso explica a tendencia, nao garante
       um percentual universal. clock() tem semantica/resolucao da biblioteca C. */
    return EXIT_SUCCESS;
}
