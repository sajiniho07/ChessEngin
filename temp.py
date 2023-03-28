import pandas as pd

matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

df = pd.DataFrame(matrix)

df.to_csv('matrix.csv', index=False, header=True)
