# Importa bibliotecas usadas.
import csv
import re


class AnalisadorSteam:
    def __init__(self, caminho_arquivo):
        """Construtor da classe. Recebe o caminho do arquivo CSV e o armazena
        no atributo 'caminho_arquivo' para ser utilizado pelos métodos de leitura e análise."""
        self.caminho_arquivo = caminho_arquivo
        # Métricas de qualidade da última carga realizada (preenchidas em carregar_dados).
        self.registros_totais = 0
        self.registros_validos = 0
        self.registros_descartados = 0

    @staticmethod
    def limpar_e_dividir_linha(linha_bruta):
        """Limpa cada linha do arquivo e separa os dados em colunas.

        Algumas linhas do arquivo possuem aspas envolvendo os dados e ';' no final.
        Esses caracteres são ajustados antes da separação das colunas com csv.reader.

        O método também é usado pelo gerar_amostra.py para evitar código repetido.

        Retorna uma lista com as colunas encontradas.
        """
        linha_bruta = linha_bruta.strip().strip(';')
        if not linha_bruta:
            return []

        if linha_bruta.startswith('"') and linha_bruta.endswith('"'):
            linha_bruta = linha_bruta[1:-1].replace('""', '"')

        try:
            return next(csv.reader([linha_bruta]))
        except StopIteration:
            return []

    def carregar_dados(self):
        """Lê o arquivo CSV e retorna os registros válidos em uma lista de dicionários.

        Algumas linhas do arquivo possuem vírgulas dentro dos campos de texto, o que pode
        fazer com que os dados sejam separados em colunas erradas. Por isso, cada linha é 
        conferida antes de ser adicionada aos dados.

        Linhas com quantidades diferente de colunas são descartadas. Os contadores de
        registros totais, válidos e descartados permitem acompanhar o resultado da leitura.
        """
        self.registros_totais = 0
        self.registros_validos = 0
        self.registros_descartados = 0

        try:
            with open(self.caminho_arquivo, mode='r', encoding='utf-8') as f:
                cabecalho_linha = f.readline()

                if not cabecalho_linha:
                    return []

                # Lê o cabeçalho, removendo espaços e separando as colunas por vírgula.
                cabecalho = cabecalho_linha.strip().strip(';').split(',')
                num_colunas_esperado = len(cabecalho)
                dados_processados = []

                # Processa o arquivo linha a linha, em vez de carregar tudo de uma
                # vez com readlines().
                for linha_bruta in f:
                    if not linha_bruta.strip().strip(';'):
                        continue

                    self.registros_totais += 1
                    colunas = self.limpar_e_dividir_linha(linha_bruta)

                    # Descarta linhas que possuem uma quantidade diferente
                    # de colunas.
                    # Assim, evitando que os dados de uma coluna sejam
                    # atribuídos incorretamente a outra.
                    if len(colunas) != num_colunas_esperado:
                        self.registros_descartados += 1
                        continue

                    dados = dict(zip(cabecalho, colunas))
                    dados_processados.append(dados)
                    self.registros_validos += 1

                return dados_processados

        except FileNotFoundError:
            # Tratamento de exceção: mostra uma mensagem caso o arquivo não
            # seja encontrado, evitando que o programa quebre de forma abrupta.
            print(f"Erro: O arquivo '{self.caminho_arquivo}' não foi encontrado.")
            return []

    def resumo_qualidade_dados(self):
        """Retorna um resumo da qualidade da última carga realizada por carregar_dados():
        quantos registros foram lidos ao todo, quantos foram considerados válidos e
        quantos foram descartados por inconsistência estrutural na fonte, incluindo o
        percentual de descarte. Deve ser chamado sempre após carregar_dados().
        """
        if self.registros_totais == 0:
            return {
                'total': 0,
                'validos': 0,
                'descartados': 0,
                'perc_descartados': 0.0,
            }

        perc_descartados = (self.registros_descartados / self.registros_totais) * 100
        return {
            'total': self.registros_totais,
            'validos': self.registros_validos,
            'descartados': self.registros_descartados,
            'perc_descartados': perc_descartados,
        }

    def analisar_precos(self, jogos):
        """Pergunta 1: Calcula a quantidade e a porcentagem de jogos gratuitos e pagos.

        Um jogo com o campo Price vazio ou não numérico não é contado como gratuito.
        """
        gratuitos = 0
        pagos = 0

        for jogo in jogos:
            preco_str = str(jogo.get('Price', '')).strip()
            if preco_str == '':
                # Preço ausente: não é dado suficiente pra classificar o jogo como
                # gratuito ou pago, então ele não entra na contagem de nenhum dos dois.
                continue

            try:
                preco = float(preco_str)
            except ValueError:
                # Tratamento de exceção: preço que não é um número válido também
                # não permite classificar o jogo, pelo mesmo motivo do caso acima.
                continue

            if preco == 0.0:
                gratuitos += 1
            else:
                pagos += 1

        total_considerado = gratuitos + pagos
        if total_considerado == 0:
            return 0, 0, 0.0, 0.0

        perc_gratuitos = (gratuitos / total_considerado) * 100
        perc_pagos = (pagos / total_considerado) * 100

        return gratuitos, pagos, perc_gratuitos, perc_pagos

    def analisar_ano_mais_frequente(self, jogos):
        """Pergunta 2: Identifica o(s) ano(s) com o maior volume de lançamentos.

        Em caso de empate entre dois ou mais anos com a mesma contagem máxima de
        lançamentos, retorna uma lista com todos os anos empatados (ordenada), 
        em vez de escolher um deles arbitrariamente.
        """
        anos_lancamento = {}

        for jogo in jogos:
            data_str = str(jogo.get('Release date', '')).strip()
            ano_match = re.search(r'\d{4}', data_str)
            if ano_match:
                ano = ano_match.group()
                anos_lancamento[ano] = anos_lancamento.get(ano, 0) + 1

        if not anos_lancamento:
            return [], 0

        maior_contagem = max(anos_lancamento.values())
        anos_top = sorted(ano for ano, qtd in anos_lancamento.items() if qtd == maior_contagem)

        return anos_top, maior_contagem

    def analisar_melhor_genero_entrada(self, jogos, min_jogos=3):
        """Pergunta 3 (Autoral): para cada gênero (um jogo pode pertencer a vários),
        calcula uma pontuação que combina aprovação do público e volume de
        avaliações, indicando possíveis oportunidades de entrada para a Fun Corp.
        Só entram no ranking gêneros com pelo menos 'min_jogos' jogos avaliados
        (com ao menos uma avaliação positiva ou negativa), para que catálogos
        grandes e pouco avaliados não distorçam a aprovação.

            pontuacao = (aprovacao_normalizada + volume_normalizado) / 2

        Aprovação é dividida por 100 (escala 0 a 1); volume é o total de
        avaliações do gênero dividido pelo maior total entre os gêneros
        filtrados. O preço médio também é calculado e devolvido, mas fica de
        fora da pontuação, servindo só como informação complementar.

        """
        stats_por_genero = {}

        for jogo in jogos:
            genero_str = str(jogo.get('Genres', '')).strip()
            if not genero_str:
                continue
            generos = [g.strip() for g in genero_str.split(',') if g.strip()]

            try:
                positivas = int(jogo.get('Positive', 0) or 0)
            except ValueError:
                positivas = 0
            try:
                negativas = int(jogo.get('Negative', 0) or 0)
            except ValueError:
                negativas = 0
            try:
                preco = float(jogo.get('Price', 0) or 0)
            except ValueError:
                preco = 0.0

            # Um jogo só é considerado "avaliado" quando tem pelo menos uma avaliação
            # positiva ou negativa. Ele continua contando para o preço médio do
            # gênero mesmo sem avaliação, mas não entra no filtro de min_jogos.
            avaliacoes_do_jogo = positivas + negativas

            for genero in generos:
                if genero not in stats_por_genero:
                    stats_por_genero[genero] = {
                        'jogos': 0,
                        'jogos_avaliados': 0,
                        'positivas': 0,
                        'negativas': 0,
                        'soma_preco': 0.0,
                    }
                stats_por_genero[genero]['jogos'] += 1
                if avaliacoes_do_jogo > 0:
                    stats_por_genero[genero]['jogos_avaliados'] += 1
                stats_por_genero[genero]['positivas'] += positivas
                stats_por_genero[genero]['negativas'] += negativas
                stats_por_genero[genero]['soma_preco'] += preco

        resultado = []
        for genero, dados in stats_por_genero.items():
            # O filtro sobre jogos avaliados, e não sobre a quantidade total
            # de jogos do gênero.
            if dados['jogos_avaliados'] < min_jogos:
                continue
            total_avaliacoes = dados['positivas'] + dados['negativas']
            if total_avaliacoes == 0:
                continue
            aprovacao = (dados['positivas'] / total_avaliacoes) * 100
            preco_medio = dados['soma_preco'] / dados['jogos']
            resultado.append({
                'genero': genero,
                'jogos': dados['jogos'],
                'jogos_avaliados': dados['jogos_avaliados'],
                'aprovacao': aprovacao,
                'preco_medio': preco_medio,
                'total_avaliacoes': total_avaliacoes,
            })

        if not resultado:
            return resultado

        # Maior volume de avaliações entre os gêneros que passaram no filtro,
        # usado como referência (valor 1.0) na normalização.
        maior_total_avaliacoes = max(item['total_avaliacoes'] for item in resultado)

        for item in resultado:
            aprovacao_normalizada = item['aprovacao'] / 100
            volume_normalizado = (
                item['total_avaliacoes'] / maior_total_avaliacoes if maior_total_avaliacoes > 0 else 0.0
            )

            # Peso igual para os dois indicadores..
            item['pontuacao'] = (aprovacao_normalizada + volume_normalizado) / 2

        resultado.sort(key=lambda x: x['pontuacao'], reverse=True)
        return resultado
