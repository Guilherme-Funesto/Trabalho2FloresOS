# Preparação para a apresentação

Todos os integrantes devem conseguir executar e explicar qualquer uma das questões. Organizem a revisão entre vocês, mas façam uma rodada conjunta cobrindo os seis programas.

## Questão 1

- Por que foi usado `static`? Para garantir duração estática; um array local de tamanho fixo sem essa palavra teria duração automática.
- Por que testar `malloc`? Ele pode retornar `NULL`; acessar esse resultado seria inválido.
- Por que não fazer `dinamico - fixo`? A subtração de ponteiros só é definida nas condições previstas para o mesmo array. O código converte para `uintptr_t` e compara representações numéricas.
- O endereço é físico? Não: o processo observa seu espaço de endereços virtual.

## Questão 2

- Por que P4 fica na partição de 150? First-Fit percorre a ordem original; a de 100 está ocupada por P1.
- Como calcular 80? `(100 - 90) + (150 - 100) + (200 - 180)`.
- Por que P5 falha com 550 livres? Nenhuma partição fixa comporta 350 e não há fusão de partições.
- As partições livres contam como fragmentação interna? Não. Só a sobra dentro das partições ocupadas.

## Questão 3

- Um acerto modifica a fila? Não, FIFO considera o momento de chegada.
- Para que o `HashSet`? Consultar presença sem percorrer toda a fila.
- Por que dividir por 13? É o total de referências, não o número de páginas distintas.
- O que é Belady? Aumentar quadros pode aumentar faltas no FIFO. Demonstrem a sequência de teste registrada no relatório.

## Questão 4

- `del` sempre destrói? Não: remove uma referência; outros aliases podem manter o objeto vivo.
- Por que `getrefcount` retorna 2 para um objeto com um nome? A chamada cria uma referência temporária.
- Por que desligar `gc`? Para observar os ciclos antes da coleta explícita. Isso não desativa a contagem de referências.
- Por que `weakref`? Permite observar sem manter o objeto vivo.
- `gc.collect()` retorna bytes? Não, a contagem de objetos inalcançáveis encontrados.

## Questão 5

- Por que C? Permite comparar variável automática e alocação explícita de um objeto do mesmo tipo.
- Por que sete rodadas e alternância? Para reduzir dependência de uma medição isolada e viés da ordem.
- Por que `volatile`, `noinline` e `-O0`? Para ajudar a preservar operações e chamadas no ensaio didático.
- A variável local necessariamente fica na pilha em toda compilação? Não; a linguagem define duração, e compiladores podem usar registradores. O ensaio controla a otimização no ambiente registrado.
- O percentual vale para qualquer computador? Não; o tempo inclui outras operações e depende do ambiente.

## Bônus

- FIFO e LRU diferem em qual regra? Ordem de chegada versus último acesso.
- Por que mover a página no acerto? Seu último uso acabou de mudar.
- LRU é sempre melhor? Não para toda sequência; neste exemplo houve uma falta a menos.
- Diferença entre 10% e 7,69? O primeiro é a redução relativa da contagem de faltas; o segundo é a diferença em pontos percentuais entre as taxas.

## Ensaio final

Baixem o repositório em uma pasta nova, compilem, executem e expliquem uma questão sorteada sem depender de arquivos gerados anteriormente. Confiram que o PDF preenchido, os códigos e as capturas estão acessíveis pelo link que será enviado.
