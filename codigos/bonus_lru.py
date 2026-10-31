"""FIFO e LRU sobre a MESMA entrada; ordem exibida indica a proxima vitima."""
import argparse
from collections import OrderedDict


def simular(capacidade, referencias, lru=False, mostrar=True):
    if type(capacidade) is not int or capacidade <= 0 or not referencias:
        raise ValueError("Frames devem ser positivos e a sequencia nao pode ser vazia.")
    memoria = OrderedDict()
    faltas = 0
    for tempo, pagina in enumerate(referencias, 1):
        if type(pagina) is not int or pagina < 0:
            raise ValueError("Paginas devem ser inteiros nao negativos.")
        evento = "Hit"
        if pagina not in memoria:
            faltas += 1
            evento = "Fault"
            if len(memoria) == capacidade:
                vitima, _ = memoria.popitem(last=False)
                evento += f" (saiu {vitima})"
            memoria[pagina] = tempo
        elif lru:
            # Atualiza timestamp e move o acesso para o fim (mais recente).
            memoria[pagina] = tempo
            memoria.move_to_end(pagina)
        if mostrar:
            print(f"Ref {pagina:2} | {list(memoria)!s:12} | {evento:19} | faltas={faltas}")
    return faltas


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("frames", type=int, nargs="?")
    parser.add_argument("referencias", nargs="?")
    args = parser.parse_args()
    try:
        n = args.frames if args.frames is not None else int(input("Numero de frames: "))
        texto = args.referencias if args.referencias is not None else input("Referencias: ")
        paginas = [int(x) for x in texto.replace(",", " ").split()]
        print("FIFO: ordem de chegada")
        fifo = simular(n, paginas)
        print("\nLRU: menos recente -> mais recente (timestamps de acesso)")
        lru = simular(n, paginas, lru=True)
        print(f"\nFIFO: {fifo} faltas; taxa={fifo / len(paginas):.2%}")
        print(f"LRU:  {lru} faltas; taxa={lru / len(paginas):.2%}")
        print(f"Diferenca FIFO - LRU: {fifo - lru} faltas")
        if lru < fifo: print("LRU teve menos faltas nesta sequencia: aproveitou acessos recentes.")
        elif lru == fifo: print("Empate nesta sequencia; as politicas podem divergir em outras.")
        else: print("FIFO teve menos faltas nesta sequencia; recencia nao garante previsao perfeita.")
        print("LRU atualiza a ordem em cada acerto; FIFO so altera a fila nas faltas.")
        print("Uma sequencia nao demonstra superioridade universal.")
    except (ValueError, EOFError) as erro:
        parser.error(str(erro))


if __name__ == "__main__":
    main()
