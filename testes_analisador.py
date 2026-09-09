"""Testes automatizados (doctest) para a Fase 1 do projeto.

Os valores esperados foram calculados manualmente em uma planilha ('amostra_legivel.csv'),
usando os 20 jogos válidos da amostra oficial ('amostra_steam.csv'):
  - Pergunta 1: 2 jogos gratuitos, 18 jogos pagos.
  - Pergunta 2: empate entre os anos 2017, 2021 e 2022, com 4 lançamentos cada.
  - Pergunta 3 (autoral): gênero Indie na liderança do ranking por pontuação
    composta (média entre aprovação e volume de avaliações normalizados), com
    15 jogos (13 avaliados), 79,9% de aprovação e pontuação 0,899. Apesar de
    Sports ter aprovação individual maior (85,6%), Indie tem uma base de
    avaliações muito maior (o gênero inclui Detention, o jogo mais avaliado da
    amostra), o que pesa mais na pontuação final do que a diferença de aprovação.

Os testes usam apenas a amostra e não dependem do arquivo completo ('steam_games.csv').

Para executar os testes, use no terminal, na mesma pasta dos demais arquivos:
    python -m doctest testes_analisador.py -v

"""

from analisador_steam import AnalisadorSteam

# Carrega a amostra uma única vez para que os testes possam reutilizar os mesmos dados.
_analisador = AnalisadorSteam('amostra_steam.csv')
_jogos_amostra = _analisador.carregar_dados()


def testar_pergunta1_precos():
    """Verifica a quantidade e o percentual de jogos gratuitos e pagos.

    Valores esperados para os 20 jogos válidos: 2 gratuitos, 18 pagos,
    correspondendo a 10% e 90% da amostra, respectivamente.

    >>> gratuitos, pagos, perc_gratuitos, perc_pagos = _analisador.analisar_precos(_jogos_amostra)
    >>> gratuitos
    2
    >>> pagos
    18
    >>> round(perc_gratuitos, 1)
    10.0
    >>> round(perc_pagos, 1)
    90.0
    """


def testar_pergunta2_ano_mais_frequente():
    """Verifica o(s) ano(s) com maior número de lançamentos.

    O resultado esperado é um empate entre 2017, 2021 e 2022, com 4 jogos
    lançados em cada ano.

    >>> anos_top, quantidade = _analisador.analisar_ano_mais_frequente(_jogos_amostra)
    >>> anos_top
    ['2017', '2021', '2022']
    >>> quantidade
    4
    """


def testar_pergunta3_ranking_generos():
    """Verifica o primeiro colocado no ranking de gêneros por pontuação composta
    (média entre aprovação e volume de avaliações; preço médio é reportado à
    parte, sem entrar na pontuação, conforme justificado na documentação do
    método).

    Para a amostra, considerando gêneros com pelo menos 1 jogo avaliado, o resultado
    esperado é Indie, com 15 jogos (13 avaliados), 79,9% de aprovação, preço médio
    de $12,52 e pontuação 0,899. O volume de avaliações do gênero (14.424, puxado
    por Detention) é o que garante a liderança mesmo com aprovação menor que a de
    Sports (85,6% em apenas 3 jogos avaliados).

    >>> ranking = _analisador.analisar_melhor_genero_entrada(_jogos_amostra, min_jogos=1)
    >>> ranking[0]['genero']
    'Indie'
    >>> ranking[0]['jogos']
    15
    >>> ranking[0]['jogos_avaliados']
    13
    >>> round(ranking[0]['aprovacao'], 1)
    79.9
    >>> round(ranking[0]['preco_medio'], 2)
    12.52
    >>> round(ranking[0]['pontuacao'], 3)
    0.899
    """


def testar_amostra_sem_registros_descartados():
    """Verifica se os 20 jogos sorteados foram lidos corretamente,
    sem descarte por desalinhamento de colunas.

    >>> resumo = _analisador.resumo_qualidade_dados()
    >>> resumo['validos']
    20
    >>> resumo['descartados']
    0
    """


if __name__ == "__main__":
    import doctest
    resultado = doctest.testmod(verbose=True)
    print()
    if resultado.failed == 0:
        print(f"Todos os testes passaram! ({resultado.attempted} verificações no total)")
    else:
        print(f"{resultado.failed} de {resultado.attempted} verificações falharam.")