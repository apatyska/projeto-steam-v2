# Programação para Dados — Projeto Final (Fase 1)

**Autora:** Patrícia do Amaral Tyska
**Disciplina:** Programação para Dados — PUCRS Online
**Tema:** Análise exploratória da base de jogos da Steam para apoiar a estratégia de expansão da Fun Corp. para o mercado de jogos digitais

---

## Contexto

A Fun Corp., empresa até então focada em jogos de tabuleiro e action figures, planeja entrar no mercado de jogos digitais. Este projeto analisa uma base com mais de 70 mil jogos publicados na Steam (coletada em maio de 2023) para responder três perguntas de negócio que embasam essa decisão.

A Fase 1 usa apenas recursos nativos de Python (listas, dicionários, arquivos, exceções, orientação a objetos), sem `pandas`, `numpy` ou `matplotlib`, conforme escopo da disciplina.

## Perguntas respondidas

| # | Pergunta | Onde está a resposta |
| --- | --- | --- |
| 1 | Qual o percentual de jogos gratuitos e pagos na plataforma? | `AnalisadorSteam.analisar_precos()` |
| 2 | Qual o ano com o maior número de novos jogos? | `AnalisadorSteam.analisar_ano_mais_frequente()` |
| 3 | *(autoral)* Qual gênero representa a melhor oportunidade de entrada, considerando aprovação do público e volume de avaliações? | `AnalisadorSteam.analisar_melhor_genero_entrada()` |

O relatório completo, com discussão dos resultados e visualizações, está em `Fase1_ProgramacaoParaDados_PatriciaTyska.pdf`.

## Base de dados

O arquivo `steam_games.csv` (~73 mil linhas) não está versionado neste repositório por questão de tamanho. Para rodar o projeto localmente, baixe a base pelo link disponibilizado pela disciplina e coloque o arquivo na raiz do projeto, com esse mesmo nome:

**Download:** [Base de dados Steam (Google Drive)](https://drive.google.com/drive/folders/1iSrASnt0vkSNjq66a3RVdy5adFiw5qqX)

## Estrutura do projeto

```
├── analisador_steam.py            # Classe AnalisadorSteam: carga e análise dos dados
├── main.py                        # Executa as 3 perguntas sobre o arquivo completo e a amostra
├── testes_analisador.py           # Testes automatizados (doctest) contra gabarito calculado manualmente
├── gerar_amostra.py                # Gera a amostra de 20 jogos usada nos testes
├── exportar_amostra_legivel.py    # Exporta a amostra em formato simplificado, para conferência manual
├── diagnostico_dados.py           # Script auxiliar de investigação de inconsistências no CSV original
├── steam_games.csv                # Base completa (~70 mil jogos) — não versionada, ver seção "Base de dados"
├── amostra_steam.csv              # Amostra de 20 jogos, formato original
└── amostra_legivel.csv            # Amostra de 20 jogos, colunas simplificadas
```

## Como executar

> Requer o `steam_games.csv` na raiz do projeto — veja a seção "Base de dados" acima.

**Rodar a análise completa (arquivo completo + amostra):**
```bash
python main.py
```

**Rodar os testes automatizados:**
```bash
python -m doctest testes_analisador.py -v
```

## Sobre a implementação

A classe `AnalisadorSteam` concentra toda a lógica de leitura e análise, expondo uma interface simples para quem for consumi-la:

```python
from analisador_steam import AnalisadorSteam

analisador = AnalisadorSteam('steam_games.csv')
jogos = analisador.carregar_dados()

gratuitos, pagos, perc_gratuitos, perc_pagos = analisador.analisar_precos(jogos)
anos_top, quantidade = analisador.analisar_ano_mais_frequente(jogos)
ranking = analisador.analisar_melhor_genero_entrada(jogos, min_jogos=50)
```

**Tratamento de inconsistências:** parte dos registros do CSV original tem vírgulas não isoladas por aspas no campo `About the game`, o que desloca as colunas seguintes. Esses registros são identificados e descartados de forma transparente durante a carga, com métricas de qualidade disponíveis em `resumo_qualidade_dados()`.

**Pergunta autoral:** combina aprovação do público e volume de avaliações em uma pontuação única por gênero, normalizada e com peso igual para os dois fatores. Metodologia completa e discussão dos resultados no PDF.

## Testes

Os testes usam uma amostra de 20 jogos (sorteados a partir do jogo 21 em diante do arquivo completo, para não reutilizar os 20 primeiros registros já conhecidos). Os valores esperados foram calculados manualmente em planilha a partir de `amostra_legivel.csv` e conferidos automaticamente contra a saída do código via `doctest`.
