import random

from analisador_steam import AnalisadorSteam

arquivo_origem = 'steam_games.csv'
arquivo_destino = 'amostra_steam.csv'

# Lê todas as linhas do arquivo original.
with open(arquivo_origem, mode='r', encoding='utf-8') as f:
    linhas = f.readlines()

# Lê o cabeçalho e conta a quantidade de colunas.
linha_cabecalho = linhas[0]
num_colunas_esperado = len(linha_cabecalho.strip().strip(';').split(','))

# Descarta os 20 primeiros jogos antes do sorteio.
candidatas = linhas[21:]

# Mantém apenas as linhas que possuem a mesma quantidade de colunas do cabeçalho.
# Assim, evitando sortear linhas com dados fora das colunas corretas.
linhas_validas = [
    linha for linha in candidatas
    if len(AnalisadorSteam.limpar_e_dividir_linha(linha)) == num_colunas_esperado
]

amostra = random.sample(linhas_validas, 20)

# Salva a amostra mantendo o formato original das linhas.
# Assim, ela pode ser lida pelo carregar_dados() da mesma forma que o arquivo completo.
with open(arquivo_destino, mode='w', encoding='utf-8', newline='') as f:
    f.write(linha_cabecalho)
    f.writelines(amostra)

print(f"Amostra gerada com {len(amostra)} jogos válidos!")
print(f"({len(linhas_validas)} linhas válidas disponíveis para sorteio, "
      f"de {len(candidatas)} linhas analisadas)")
