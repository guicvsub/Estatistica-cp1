import pandas as pd 

# Carregar o CSV compactado
df = pd.read_csv(r"dadosnovos\arquivos.csv.gz", compression="gzip")  

# Salvar como CSV normal
df.to_csv("dados_convertido.csv", index=False)  

print("Conversão concluída!")
