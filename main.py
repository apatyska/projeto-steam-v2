from analisador_steam import AnalisadorSteam


def exibir_qualidade_dados(analisador):
    """Exibe a quantidade de registros lidos, válidos e descartados."""
    resumo = analisador.resumo_qualidade_dados()
    print(f"Registros lidos: {resumo['total']} | "
          f"Válidos: {resumo['validos']} | "
          f"Descartados: {resumo['descartados']} "
          f"({resumo['perc_descartados']:.1f}% da base)")


def exibir_resultados(nome_conjunto, analisador, jogos, min_jogos_genero):
    """Executa as três perguntas e exibe os resultados."""
    print(f"\n Resultados - {nome_conjunto} ({len(jogos)} jogos válidos)")
    exibir_qualidade_dados(analisador)

    # Pergunta 1
    gratuitos, pagos, perc_g, perc_p = analisador.analisar_precos(jogos)
    print(f"1. Jogos Gratuitos: {perc_g:.1f}% ({gratuitos}) | Pagos: {perc_p:.1f}% ({pagos})")

    # Pergunta 2
    anos_top, qtd_ano = analisador.analisar_ano_mais_frequente(jogos)
    if len(anos_top) <= 1:
        ano_exibido = anos_top[0] if anos_top else "Desconhecido"
        print(f"2. Ano com mais lançamentos: {ano_exibido} ({qtd_ano} jogos)")
    else:
        anos_str = ", ".join(anos_top)
        print(f"2. Anos com mais lançamentos (empate): {anos_str} ({qtd_ano} jogos cada)")

    # Pergunta 3 (Autoral)
    ranking_generos = analisador.analisar_melhor_genero_entrada(jogos, min_jogos=min_jogos_genero)
    plural = "jogo avaliado" if min_jogos_genero == 1 else "jogos avaliados"
    print(f"3. Melhores gêneros para entrada no mercado "
          f"(considerando apenas gêneros com pelo menos {min_jogos_genero} {plural}):")
    for item in ranking_generos[:5]:
        print(f"   {item['genero']}: pontuação {item['pontuacao']:.3f} | "
              f"{item['aprovacao']:.1f}% aprovação | preço médio ${item['preco_medio']:.2f} | "
              f"{item['jogos']} jogos ({item['jogos_avaliados']} avaliados)")


if __name__ == "__main__":
    # No arquivo completo, entram no ranking apenas gêneros com pelo menos 50 jogos,
    # pois gêneros com poucos jogos podem apresentar uma aprovação alta, sem representar
    # um resultado consistente para o conjunto de jogos daquele gênero.
    analisador_completo = AnalisadorSteam('steam_games.csv')
    jogos_completo = analisador_completo.carregar_dados()
    exibir_resultados("Arquivo Completo", analisador_completo, jogos_completo, min_jogos_genero=50)

    # Na amostra de 20 jogos, entra no ranking qualquer gênero com pelo menos 1 jogo,
    # pois um limite maior poderia deixar alguns deles de fora.
    analisador_amostra = AnalisadorSteam('amostra_steam.csv')
    jogos_amostra = analisador_amostra.carregar_dados()
    exibir_resultados("Amostra (20 jogos)", analisador_amostra, jogos_amostra, min_jogos_genero=1)
