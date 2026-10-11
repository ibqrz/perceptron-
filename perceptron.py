"""
Perceptron de Aprovação de Empréstimo (menu interativo no terminal)

Entradas (escala de 0 a 10):
    x1: Histórico de Crédito
    x2: Renda Comprovada
    x3: Estabilidade no Emprego

Pesos: w1 = 0.5, w2 = 0.3, w3 = 0.2
Bias:  b = -5.0 (corte de aprovação)
Regra: soma = x1*w1 + x2*w2 + x3*w3 + b  ->  soma >= 0 APROVADO, senão NEGADO

Uso:  python perceptron_emprestimo.py
"""
import os
import sys
from datetime import datetime

# ---------- cores (desligadas automaticamente se o terminal não suportar) ----------
if os.name == "nt":
    os.system("")                      # habilita códigos ANSI no terminal do Windows 10+
USAR_COR = sys.stdout.isatty() and not os.environ.get("NO_COLOR")


def cor(texto, codigo):
    return f"\033[{codigo}m{texto}\033[0m" if USAR_COR else texto


def azul(t):     return cor(t, "1;36")
def verde(t):    return cor(t, "1;32")
def vermelho(t): return cor(t, "1;31")
def amarelo(t):  return cor(t, "1;33")
def magenta(t):  return cor(t, "1;35")
def cinza(t):    return cor(t, "90")


# ---------- parâmetros do Perceptron ----------
ENTRADAS = [
    ("x1", "Histórico de Crédito", 0.5),
    ("x2", "Renda Comprovada", 0.3),
    ("x3", "Estabilidade no Emprego", 0.2),
]
BIAS = -5.0
LARGURA_BARRA = 10

historico = []          # avaliações feitas durante a sessão


def hora():
    return datetime.now().strftime("%H:%M")


# ---------- lógica do Perceptron ----------
def perceptron_emprestimo(x1, x2, x3):
    """Retorna (soma, contribuições por entrada, aprovado?)."""
    valores = (x1, x2, x3)
    contribuicoes = [v * w for v, (_, _, w) in zip(valores, ENTRADAS)]
    soma = sum(contribuicoes) + BIAS
    return soma, contribuicoes, soma >= 0


# ---------- entrada de dados ----------
def ler_nota(chave, nome):
    """Lê um número de 0 a 10. Retorna None se o usuário digitar 'c' (cancelar)."""
    while True:
        bruto = input(f"  {azul(chave)} {nome} {cinza('(0 a 10, c = cancelar)')} > ").strip().lower()
        if bruto == "c":
            return None
        try:
            valor = float(bruto.replace(",", "."))
        except ValueError:
            print(vermelho("  ✗ Valor inválido. Digite um número, por exemplo 7 ou 7,5."))
            continue
        if not 0 <= valor <= 10:
            print(vermelho(f"  ✗ O valor deve estar entre 0 e 10 (recebido: {valor:g})."))
            continue
        return valor


# ---------- telas ----------
def limpar_tela():
    if USAR_COR:
        sys.stdout.write("\033[2J\033[H")
        sys.stdout.flush()
    else:
        os.system("cls" if os.name == "nt" else "clear")


def mostrar_banner():
    print()
    print(azul("  ╔══════════════════════════════════════════════╗"))
    print(azul("  ║    PERCEPTRON - APROVAÇÃO DE EMPRÉSTIMO      ║"))
    print(azul("  ╚══════════════════════════════════════════════╝"))
    print()


def mostrar_menu():
    print(azul("  MENU PRINCIPAL"))
    print(cinza("  " + "─" * 46))
    print(f"  {amarelo('1')}  Avaliar um novo cliente")
    print(f"  {amarelo('2')}  Rodar os 2 perfis de teste")
    print(f"  {amarelo('3')}  Ver histórico de avaliações")
    print(f"  {amarelo('4')}  Ver regras do Perceptron")
    print(f"  {amarelo('5')}  Limpar a tela")
    print(f"  {amarelo('0')}  Sair")
    print(cinza("  " + "─" * 46))


def mostrar_regras():
    print()
    print(azul("  REGRAS DO PERCEPTRON"))
    print(cinza("  " + "─" * 46))
    for chave, nome, peso in ENTRADAS:
        print(f"  {azul(chave)}  {nome:<26} peso {amarelo(f'{peso:.1f}')}")
    print(f"  {azul('b ')}  {'Bias (corte de aprovação)':<26} {amarelo(f'{BIAS:+.1f}')}")
    print(cinza("  " + "─" * 46))
    print("  soma = x1·w1 + x2·w2 + x3·w3 + b")
    print(f"  soma {verde('>= 0')}  →  {verde('Empréstimo APROVADO')}")
    print(f"  soma {vermelho('<  0')}  →  {vermelho('Empréstimo NEGADO')}")
    print()


def barra(contribuicao, maximo):
    cheios = round(contribuicao / maximo * LARGURA_BARRA) if maximo else 0
    return "█" * cheios + cinza("░" * (LARGURA_BARRA - cheios))


def exibir_resultado(nome_cliente, valores):
    soma, contribuicoes, aprovado = perceptron_emprestimo(*valores)
    historico.append((hora(), nome_cliente, valores, soma, aprovado))

    print()
    print(magenta(f"  ╭─ Cliente: {nome_cliente} " + "─" * max(2, 32 - len(nome_cliente))))
    for (chave, nome, peso), valor, contrib in zip(ENTRADAS, valores, contribuicoes):
        print(f"  │ {azul(chave)} {nome:<24} {valor:>4g} × {peso:.1f} = {contrib:>4.2f}  "
              f"{verde(barra(contrib, peso * 10))}")
    print(f"  │ {azul('b ')} {'Bias':<24} {'':>4}   {'':>3}   {BIAS:>+5.2f}")
    print(cinza("  │ " + "─" * 44))
    cor_soma = verde if aprovado else vermelho
    print(f"  │ Soma ponderada + bias: {cor_soma(f'{soma:+.2f}')}")
    if aprovado:
        print(f"  ╰─ {verde('✓ Empréstimo APROVADO')}")
    else:
        print(f"  ╰─ {vermelho('✗ Empréstimo NEGADO')}")
    print()


def avaliar_novo_cliente():
    print()
    print(azul("  NOVA AVALIAÇÃO"))
    print(cinza("  " + "─" * 46))
    nome = input(f"  {azul('Nome do cliente')} {cinza('(ENTER = Cliente)')} > ").strip() or "Cliente"
    valores = []
    for chave, descricao, _ in ENTRADAS:
        v = ler_nota(chave, descricao)
        if v is None:
            print(amarelo("  ! Avaliação cancelada.\n"))
            return
        valores.append(v)
    exibir_resultado(nome, tuple(valores))


def rodar_perfis_de_teste():
    print()
    print(azul("  PERFIS DE TESTE"))
    exibir_resultado("Ana (bom perfil)", (8, 7, 9))
    exibir_resultado("Bruno (perfil de risco)", (3, 5, 2))


def mostrar_historico():
    print()
    print(azul("  HISTÓRICO DA SESSÃO"))
    print(cinza("  " + "─" * 62))
    if not historico:
        print(cinza("  Nenhuma avaliação feita ainda."))
        print()
        return
    for h, nome, (x1, x2, x3), soma, aprovado in historico:
        decisao = verde("APROVADO") if aprovado else vermelho("NEGADO  ")
        print(f"  {cinza(h)}  {nome[:22]:<22} ({x1:g}, {x2:g}, {x3:g})  "
              f"{soma:>+6.2f}  {decisao}")
    total = len(historico)
    aprov = sum(1 for item in historico if item[4])
    print(cinza("  " + "─" * 62))
    print(f"  {total} avaliação(ões): {verde(str(aprov) + ' aprovada(s)')}, "
          f"{vermelho(str(total - aprov) + ' negada(s)')}")
    print()


def main():
    limpar_tela()
    mostrar_banner()
    try:
        while True:
            mostrar_menu()
            opcao = input(f"  {azul('opção')} > ").strip()

            if opcao == "1":
                avaliar_novo_cliente()
            elif opcao == "2":
                rodar_perfis_de_teste()
            elif opcao == "3":
                mostrar_historico()
            elif opcao == "4":
                mostrar_regras()
            elif opcao == "5":
                limpar_tela()
                mostrar_banner()
            elif opcao == "0":
                break
            else:
                print(vermelho("  ✗ Opção inválida. Escolha um número do menu.\n"))
    except (EOFError, KeyboardInterrupt):
        print()
    print(cinza("\n  Encerrando a simulação. Até logo!"))


if __name__ == "__main__":
    main()