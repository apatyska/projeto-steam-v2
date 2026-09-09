"""Script usado durante o desenvolvimento para investigar o descarte de registros
do arquivo 'steam_games.csv' por diferença no número de colunas.

Não faz parte das três perguntas do projeto, mas foi usado para identificar
as linhas com problemas e definir a regra de validação adotada em
AnalisadorSteam.carregar_dados(): descartar linhas com número de colunas
diferente do cabeçalho.

O script reutiliza limpar_e_dividir_linha() da classe AnalisadorSteam para
evitar repetir a lógica de limpeza dos dados.

Uso: python diagnostico_dados.py [numero_da_linha]
Sem informar uma linha, mostra um resumo dos problemas encontrados no arquivo.
Informando uma linha, mostra os detalhes das colunas encontradas nela.
"""

import sys

from analisador_steam import AnalisadorSteam

ARQUIVO = 'steam_games.csv'


def panorama_geral():
    """Conta as linhas com número de colunas diferente do cabeçalho
    e mostra alguns exemplos."""
    with open(ARQUIVO, mode='r', encoding='utf-8') as f:
        linhas = f.readlines()

    cabecalho = linhas[0].strip().strip(';').split(',')
    num_esperado = len(cabecalho)
    print(f"Colunas esperadas (pelo cabeçalho): {num_esperado}")

    linhas_com_problema = 0
    exemplos = []

    for i, linha_bruta in enumerate(linhas[1:], start=2):
        if not linha_bruta.strip().strip(';'):
            continue

        colunas = AnalisadorSteam.limpar_e_dividir_linha(linha_bruta)

        if len(colunas) != num_esperado:
            linhas_com_problema += 1
            if len(exemplos) < 5:
                appid = colunas[0] if colunas else None
                nome = colunas[1] if len(colunas) > 1 else None
                exemplos.append((i, len(colunas), appid, nome))

    print(f"Total de linhas: {len(linhas) - 1}")
    print(f"Linhas com número de colunas diferente do esperado: {linhas_com_problema}")
    print("\nExemplos (nº da linha no arquivo, colunas encontradas, AppID, Name):")
    for ex in exemplos:
        print(f"  {ex}")


def detalhar_linha(numero_linha):
    """Mostra as colunas de uma linha específica e compara com o cabeçalho"""
    with open(ARQUIVO, mode='r', encoding='utf-8') as f:
        linhas = f.readlines()

    cabecalho = linhas[0].strip().strip(';').split(',')
    linha_bruta = linhas[numero_linha - 1]  # -1 porque a lista é 0-indexada

    print("Conteúdo da linha (primeiros 600 caracteres):")
    print(linha_bruta[:600])

    colunas = AnalisadorSteam.limpar_e_dividir_linha(linha_bruta)
    print(f"\nColuna encontradas: {len(colunas)} (esperado: {len(cabecalho)})")

    for i, valor in enumerate(colunas):
        nome_esperado = cabecalho[i] if i < len(cabecalho) else "(coluna extra, sem correspondência)"
        print(f"[{i}] {nome_esperado}: {valor[:60]}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        detalhar_linha(int(sys.argv[1]))
    else:
        panorama_geral()
