import pandas as pd

# Read from CSV to Pandas DataFrame
df = pd.read_csv("D:\School\Sem2\AI\data.csv", header=0)

# First five items
players= df[df['Age']>40]
print(players.head(26))

