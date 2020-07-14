import pandas as pd
import numpy as np

df = pd.DataFrame(np.random.randn(50, 4), columns=list('ABCD'))

for row in df.itertuples():
    df._set_value(row.Index, 'test', row.D)

print(df.head())