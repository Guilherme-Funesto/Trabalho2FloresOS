# Gerenciamento de Memória em Sistemas Operacionais

Pacote com as cinco questões e o bônus LRU do trabalho de Sistemas Operacionais do professor José Carlos Domingues Flores.

## Conteúdo

- `Relatorio_Gerenciamento_de_Memoria.pdf`: respostas teóricas, análise, evidências e referências. A capa tem campos preenchíveis para turma, data, oito nomes/RAs, representante e repositório.
- `Relatorio_editavel.md`: texto editável do relatório.
- `codigos/`: seis implementações e uma suíte de testes.
- `evidencias/`: imagens geradas diretamente dos registros reais de execução, sem alteração dos resultados. Não são capturas de tela.
- `capturas/`: instruções para acrescentar as capturas de terminal exigidas pelo professor; essa etapa permanece pendente.
- `resultados/`: saídas completas e registro do ambiente utilizado.
- `GUIA_APRESENTACAO.md`: perguntas para preparação do grupo.

## Preencher os dados depois

Abra o PDF em um leitor que suporte formulários, preencha a primeira página e salve uma cópia. Feche e reabra para confirmar que os dados foram salvos. Existem oito linhas para integrantes; preencha no mínimo cinco. Também é possível editar o texto de `Relatorio_editavel.md` em um editor de texto. Markdown não altera automaticamente o PDF.

## Pré-requisitos

- C: GCC ou Clang com suporte a C11. Também é possível usar `zig cc`.
- Python: CPython 3.10 ou posterior, sem pacotes externos para os programas. Os resultados do coletor apresentados no relatório usam CPython 3.12.14; a organização das gerações pode mudar em outras versões.
- Java: JDK 11 ou posterior (incluindo `javac`). Foi usado OpenJDK 25.0.4.

Abra o terminal na pasta `codigos`.

## Questão 1

```sh
gcc -std=c11 -O0 -Wall -Wextra -pedantic q1_alocacao.c -o q1
```

Windows PowerShell: `.\q1.exe`. Linux/macOS: `./q1`.

Confira os valores 1 a 5 no array estático e 10 a 19 no dinâmico. Os endereços mudam entre execuções. A diferença numérica não mede distância física na RAM.

## Questão 2

```sh
python q2_fragmentacao.py
```

Resultado: P4 ocupa a partição de 150; P5 falha; fragmentação interna final de 80 unidades, 370 utilizadas e 550 livres.

## Questão 3

```sh
javac -encoding UTF-8 Fifo.java
java Fifo 3 "7,0,1,2,0,3,0,4,2,3,0,3,2"
```

Também pode executar `java Fifo` e digitar os quadros e as referências quando solicitado. Resultado do exemplo: 10 faltas, 3 acertos e taxa de 76,92%.

## Questão 4

```sh
python q4_gc.py
```

Observe os quatro cenários: referência única, aliases, autorreferência e ciclo entre dois objetos. As estatísticas são acumuladas desde o início do interpretador; as variações isolam as coletas explícitas. O programa restaura o estado anterior do coletor automático.

## Questão 5

```sh
gcc -std=c11 -O0 -Wall -Wextra -pedantic q5_desempenho.c -o q5
```

Windows PowerShell: `.\q5.exe`. Linux/macOS: `./q5`.

Use `-O0`, feche aplicativos pesados e preserve todas as sete rodadas. Os tempos não precisam reproduzir os valores do relatório. A fórmula é `100 * (media_heap - media_local) / media_local`. O teste inclui acessos, funções e laços; não é uma medida isolada do alocador. Se a média local for zero, o programa informa resolução insuficiente.

## Bônus

```sh
python bonus_lru.py 3 "7,0,1,2,0,3,0,4,2,3,0,3,2"
```

Sem argumentos, o programa pergunta os dados. Resultado: FIFO com 10 faltas e LRU com 9. A redução é de uma falta, 10% na contagem de faltas ou 7,69 pontos percentuais na taxa.

## Testes

```sh
javac -encoding UTF-8 Fifo.java
python testes.py --java
```

São 11 testes, com casos aleatórios reproduzíveis e verificação cruzada Java/Python. Sem `--java`, os dois testes Java são ignorados. Os arquivos `.class` são gerados pela compilação e não precisam ser enviados ao repositório.

## Entrega e apresentação

O enunciado informa prazo até **18/11** e apresentações a partir de **19/11**, sem indicar o ano. O trabalho vale **3,0 pontos**, com bônus de **0,3**. Exige grupo de no mínimo cinco pessoas e participação de todos no desenvolvimento e na apresentação. Trabalho individual não é permitido.

Antes de entregar:

1. Preencher os dados reais do grupo na capa.
2. Todos devem revisar, compreender e executar os programas; o enunciado prevê explicação e execução de código sorteado.
3. Produzir as capturas de tela seguindo `capturas/COMO_OBTER_CAPTURAS.md`. Criar ou usar um repositório GitHub e publicar o PDF, fontes, capturas e instruções. Isso ainda não foi feito por este pacote.
4. Testar o acesso ao link e preencher o campo do repositório no PDF.
5. Somente o representante deve enviar o PDF, o link e os nomes/RAs para `jose.flores@unicesumar.edu.br`.
6. Usar exatamente o assunto: `ESOFT4-SO-2o Bimestre-Trabalho Prático 1`.

O enunciado atribui 50% da avaliação à correção técnica, 20% à organização do código, 15% aos comentários e 15% à análise. Também informa nota zero para cópias, redução da nota por atraso e por não apresentação, e não aceita entregas após a data da apresentação. Consulte o documento original para todas as regras. Este pacote não foi publicado nem enviado por e-mail.
