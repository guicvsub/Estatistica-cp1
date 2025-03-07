import pandas as pd  

df = pd.read_csv("arquivo.csv.gz", compression="gzip")  
print(df.head())  # Exibir as primeiras linhas  
