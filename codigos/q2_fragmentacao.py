"""Particoes fixas: First-Fit, sem divisao nem fusao de particoes."""
from dataclasses import dataclass


@dataclass
class Particao:
    capacidade: int
    nome: str | None = None
    tamanho: int = 0

    @property
    def desperdicio(self):
        return self.capacidade - self.tamanho if self.nome is not None else 0


class Gerenciador:
    def __init__(self):
        self.particoes = [Particao(n) for n in (100, 150, 200, 250, 300)]

    def fragmentacao_total(self):
        return sum(p.desperdicio for p in self.particoes)

    def alocar_processo(self, nome, tamanho):
        if not isinstance(nome, str) or not nome.strip():
            raise ValueError("Nome deve ser um texto nao vazio.")
        nome = nome.strip()
        if type(tamanho) is not int or tamanho <= 0:
            raise ValueError("Tamanho deve ser inteiro positivo.")
        if any(p.nome == nome for p in self.particoes):
            raise ValueError("Processo ja alocado: " + nome)
        # A ordem original das particoes define o First-Fit.
        for i, p in enumerate(self.particoes, 1):
            if p.nome is None and p.capacidade >= tamanho:
                p.nome, p.tamanho = nome, tamanho
                print(f"{nome} ({tamanho}) -> particao {i} ({p.capacidade}); "
                      f"interna={p.desperdicio}; total={self.fragmentacao_total()}")
                return True
        print(f"FALHA: {nome} ({tamanho}); nenhuma particao livre comporta o processo.")
        return False

    def liberar_processo(self, nome):
        if not isinstance(nome, str) or not nome.strip():
            raise ValueError("Nome deve ser um texto nao vazio.")
        for p in self.particoes:
            if p.nome == nome.strip():
                p.nome, p.tamanho = None, 0
                print(f"{nome.strip()} liberado; interna total={self.fragmentacao_total()}")
                return True
        print(f"Processo nao encontrado: {nome}")
        return False

    def exibir_memoria(self):
        print("Particao | Capacidade | Processo | Usado | Interna")
        for i, p in enumerate(self.particoes, 1):
            print(f"{i:^8} | {p.capacidade:^10} | {p.nome or 'LIVRE':^8} | "
                  f"{p.tamanho:^5} | {p.desperdicio:^7}")
        livre = sum(p.capacidade for p in self.particoes if p.nome is None)
        usado = sum(p.tamanho for p in self.particoes)
        print(f"Usado={usado}; livre={livre}; fragmentacao interna={self.fragmentacao_total()}")
        assert usado + livre + self.fragmentacao_total() == 1000


def main():
    memoria = Gerenciador()
    memoria.alocar_processo("P1", 90)
    memoria.alocar_processo("P2", 140)
    memoria.alocar_processo("P3", 180)
    memoria.liberar_processo("P2")
    memoria.alocar_processo("P4", 100)
    memoria.alocar_processo("P5", 350)
    memoria.exibir_memoria()


if __name__ == "__main__":
    main()
