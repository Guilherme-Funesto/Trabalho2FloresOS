import java.util.ArrayDeque;
import java.util.HashSet;
import java.util.Locale;
import java.util.Queue;
import java.util.Scanner;
import java.util.Set;

/** FIFO: a fila vai da pagina mais antiga para a mais nova. */
public class Fifo {
    public static int simular(int capacidade, int[] paginas, boolean mostrar) {
        if (capacidade <= 0 || paginas == null || paginas.length == 0)
            throw new IllegalArgumentException("Informe frames positivos e referencias nao vazias.");
        Queue<Integer> fila = new ArrayDeque<>();
        Set<Integer> presentes = new HashSet<>();
        int faltas = 0;
        for (int pagina : paginas) {
            if (pagina < 0) throw new IllegalArgumentException("Paginas devem ser nao negativas.");
            String evento = "Page Hit";
            if (!presentes.contains(pagina)) {
                faltas++;
                evento = "Page Fault";
                if (fila.size() == capacidade) {
                    int removida = fila.remove();
                    presentes.remove(removida);
                    evento += " (substituiu " + removida + ")";
                }
                fila.add(pagina);
                presentes.add(pagina);
            }
            // Um acerto NAO muda a ordem: FIFO considera chegada, nao ultimo uso.
            if (mostrar) System.out.printf("Ref: %d | Frames: %s | %s | Faltas: %d%n",
                    pagina, fila, evento, faltas);
        }
        if (mostrar) System.out.printf(Locale.ROOT,
                "Total: %d referencias; %d faltas; %d acertos; taxa: %.2f%%%n",
                paginas.length, faltas, paginas.length - faltas, 100.0 * faltas / paginas.length);
        return faltas;
    }

    public static void main(String[] args) {
        try (Scanner entrada = new Scanner(System.in)) {
            String quantidade;
            String sequencia;
            if (args.length == 2) {
                quantidade = args[0]; sequencia = args[1];
            } else if (args.length == 0) {
                System.out.println("Numero de frames:");
                quantidade = entrada.nextLine();
                System.out.println("Referencias separadas por espacos ou virgulas:");
                sequencia = entrada.nextLine();
            } else throw new IllegalArgumentException("Uso: java Fifo 3 \"7,0,1,2\"");
            int capacidade = Integer.parseInt(quantidade.trim());
            if (sequencia.trim().isEmpty()) throw new IllegalArgumentException("Sequencia vazia.");
            String[] partes = sequencia.trim().split("[,\\s]+");
            int[] paginas = new int[partes.length];
            for (int i = 0; i < partes.length; i++) paginas[i] = Integer.parseInt(partes[i]);
            System.out.println("FIFO | ordem de chegada: mais antiga -> mais nova");
            simular(capacidade, paginas, true);
        } catch (IllegalArgumentException | java.util.NoSuchElementException erro) {
            System.err.println("Erro de entrada: " + erro.getMessage());
            System.exit(1);
        }
    }
}
