"""Demonstracao voltada ao CPython, com coleta automatica restaurada ao final."""
import gc
import platform
import sys
import weakref


class Objeto:
    def __init__(self, nome):
        self.nome = nome
        self.dados = bytearray(1_000_000)  # Array de 1 MB; sem milhoes de prints.
        self.referencia = None
        print(f"CRIADO: {nome} (dados: {len(self.dados)} bytes)")

    def __del__(self):
        print(f"DESTRUIDO: {self.nome}")


def main():
    print(f"Ambiente: {platform.python_implementation()} {platform.python_version()}")
    if platform.python_implementation() != "CPython":
        raise RuntimeError("Execute no CPython para observar contagem de referencias.")
    gc.collect()
    antes = gc.get_stats()
    estava_ativo = gc.isenabled()
    # Desliga apenas coletas automaticas de ciclos; contagem continua funcionando.
    gc.disable()
    try:
        print("\nCENARIO 1: referencia unica")
        a = Objeto("A")
        print("getrefcount(A):", sys.getrefcount(a), "(inclui referencia temporaria)")
        observador = weakref.ref(a)  # Nao mantem o objeto vivo.
        del a
        print("A destruido imediatamente:", observador() is None)

        print("\nCENARIO 2: duas referencias ao mesmo objeto")
        b = Objeto("B")
        alias = b
        print("getrefcount(B):", sys.getrefcount(b))
        observador = weakref.ref(b)
        del b
        print("B continua vivo pelo alias:", observador() is not None)
        print("getrefcount(alias):", sys.getrefcount(alias))
        del alias
        print("B destruido ao remover ultimo alias:", observador() is None)

        print("\nCENARIO 3: autorreferencia sem raiz externa")
        c = Objeto("C")
        c.referencia = c
        print("getrefcount(C):", sys.getrefcount(c))
        observador = weakref.ref(c)
        del c
        print("C continua vivo pelo ciclo:", observador() is not None)
        print("Inalcancaveis encontrados por gc.collect():", gc.collect())
        print("C coletado:", observador() is None)

        print("\nCENARIO 4: ciclo entre dois objetos")
        d, e = Objeto("D"), Objeto("E")
        d.referencia, e.referencia = e, d
        rd, re = weakref.ref(d), weakref.ref(e)
        del d, e
        print("Ciclo vivo antes da coleta:", rd() is not None and re() is not None)
        print("Inalcancaveis encontrados por gc.collect():", gc.collect())
        print("D e E coletados:", rd() is None and re() is None)
        print("\nESTATISTICAS gc.get_stats() (acumuladas e variacoes)")
        for i, (inicio, fim) in enumerate(zip(antes, gc.get_stats())):
            delta = {k: fim[k] - inicio[k] for k in fim}
            print(f"Geracao {i}: {fim}")
            print(f"  Variacao: {delta}")
    finally:
        if estava_ativo:
            gc.enable()
        print("Coleta automatica restaurada:", gc.isenabled())


if __name__ == "__main__":
    main()
