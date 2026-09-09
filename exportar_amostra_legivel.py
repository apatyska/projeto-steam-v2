import csv

from analisador_steam import AnalisadorSteam

# Campos usados para conferir manualmente os dados das Perguntas 1 e 2
CAMPOS = ['AppID', 'Name', 'Release date', 'Price', 'Genres', 'Positive', 'Negative']

analisador = AnalisadorSteam('amostra_steam.csv')
jogos = analisador.carregar_dados()

with open('amostra_legivel.csv', mode='w', encoding='utf-8', newline='') as f:
    escritor = csv.DictWriter(f, fieldnames=CAMPOS)
    escritor.writeheader()
    for jogo in jogos:
        escritor.writerow({campo: jogo.get(campo, '') for campo in CAMPOS})

print(f"Arquivo 'amostra_legivel.csv' gerado com sucesso: {len(jogos)} jogos exportados.")
print("O arquivo está em formato CSV, separado por vírgulas, e pode ser aberto no Excel ou Google Sheets.")
