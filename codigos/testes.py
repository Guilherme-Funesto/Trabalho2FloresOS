"""Testes de invariantes e casos de borda. Rode: python testes.py
Para validar tambem Java: javac Fifo.java; python testes.py --java
"""
import contextlib
import io
import random
import subprocess
import sys
import unittest
from pathlib import Path
from q2_fragmentacao import Gerenciador
from bonus_lru import simular

EXEMPLO = [7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2]
JAVA = "--java" in sys.argv
if JAVA:
    sys.argv.remove("--java")


class MemoriaTest(unittest.TestCase):
    def setUp(self):
        self.saida = contextlib.redirect_stdout(io.StringIO())
        self.saida.__enter__()

    def tearDown(self):
        self.saida.__exit__(None, None, None)

    def test_sequencia_enunciado(self):
        m = Gerenciador()
        for nome, n in [("P1", 90), ("P2", 140), ("P3", 180)]:
            self.assertTrue(m.alocar_processo(nome, n))
        self.assertEqual(m.fragmentacao_total(), 40)
        self.assertTrue(m.liberar_processo("P2"))
        self.assertTrue(m.alocar_processo("P4", 100))
        self.assertFalse(m.alocar_processo("P5", 350))
        self.assertEqual(m.fragmentacao_total(), 80)
        self.assertEqual(m.particoes[1].nome, "P4")
        m.exibir_memoria()

    def test_limites_e_reuso(self):
        m = Gerenciador()
        for i, n in enumerate((100, 150, 200, 250, 300)):
            self.assertTrue(m.alocar_processo(str(i), n))
        self.assertEqual(m.fragmentacao_total(), 0)
        self.assertFalse(m.alocar_processo("extra", 1))
        self.assertFalse(m.liberar_processo("ausente"))
        self.assertTrue(m.liberar_processo("0"))
        self.assertTrue(m.alocar_processo("novo", 100))

    def test_invalidos(self):
        m = Gerenciador()
        for nome, n in [("", 10), (None, 10), ("a", 0), ("a", -1), ("a", 1.5), ("a", True)]:
            with self.subTest(nome=nome, n=n), self.assertRaises(ValueError):
                m.alocar_processo(nome, n)
        m.alocar_processo("a", 10)
        with self.assertRaises(ValueError):
            m.alocar_processo("a", 20)

    def test_conservacao_aleatoria(self):
        rng = random.Random(42)
        m = Gerenciador()
        for i in range(200):
            m.alocar_processo(f"p{i}", rng.randint(1, 400))
            if i % 2 == 0:
                ocupadas = [p for p in m.particoes if p.nome is not None]
                if ocupadas: m.liberar_processo(rng.choice(ocupadas).nome)
            self.assertEqual(sum(p.tamanho for p in m.particoes) + m.fragmentacao_total()
                             + sum(p.capacidade for p in m.particoes if p.nome is None), 1000)


class PaginasTest(unittest.TestCase):
    def test_enunciado(self):
        self.assertEqual(simular(3, EXEMPLO, mostrar=False), 10)
        self.assertEqual(simular(3, EXEMPLO, lru=True, mostrar=False), 9)

    def test_belady(self):
        refs = [1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5]
        self.assertEqual(simular(3, refs, mostrar=False), 9)
        self.assertEqual(simular(4, refs, mostrar=False), 10)

    def test_limites(self):
        for lru in (False, True):
            self.assertEqual(simular(1, [1, 1, 2, 2, 1], lru, False), 3)
            self.assertEqual(simular(10, [1, 2, 1, 3], lru, False), 3)
            self.assertEqual(simular(2, [7], lru, False), 1)

    def test_invalidos(self):
        for n, refs in [(0, [1]), (-1, [1]), (2, []), (2, [-1]), (2, [1.5])]:
            with self.subTest(n=n, refs=refs), self.assertRaises(ValueError):
                simular(n, refs, mostrar=False)

    def test_lru_contra_oraculo_independente(self):
        rng = random.Random(123)
        # Oraculo: busca para tras na sequencia, sem OrderedDict ou timestamps.
        for _ in range(100):
            refs = [rng.randrange(6) for _ in range(30)]
            n = rng.randint(1, 5)
            presentes, faltas = set(), 0
            for i, p in enumerate(refs):
                if p not in presentes:
                    faltas += 1
                    if len(presentes) == n:
                        reverso = refs[:i][::-1]
                        presentes.remove(max(presentes, key=reverso.index))
                    presentes.add(p)
            self.assertEqual(simular(n, refs, True, False), faltas)

    @unittest.skipUnless(JAVA, "Use --java apos compilar Fifo.java")
    def test_java_mesma_entrada(self):
        import re
        rng = random.Random(321)
        for refs, n in [(EXEMPLO, 3)] + [([rng.randrange(5) for _ in range(20)], rng.randint(1, 4)) for _ in range(10)]:
            proc = subprocess.run(["java", "-cp", str(Path(__file__).parent), "Fifo", str(n),
                                   ",".join(map(str, refs))], capture_output=True, text=True)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            faltas = int(re.search(r"referencias; (\d+) faltas", proc.stdout).group(1))
            self.assertEqual(faltas, simular(n, refs, mostrar=False))

    @unittest.skipUnless(JAVA, "Use --java apos compilar Fifo.java")
    def test_java_invalidos(self):
        for n, refs in [("0", "1"), ("a", "1"), ("2", ""), ("2", "-1"), ("2", "abc")]:
            proc = subprocess.run(["java", "-cp", str(Path(__file__).parent), "Fifo", n, refs],
                                  capture_output=True, text=True)
            self.assertNotEqual(proc.returncode, 0)
            self.assertIn("Erro de entrada", proc.stderr)


if __name__ == "__main__":
    unittest.main(verbosity=2)
