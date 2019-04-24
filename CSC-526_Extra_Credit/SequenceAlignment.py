import pandas as pd, numpy as np

t = "TCAGTTGCC"
s = "AGGTTG"

score_matrix = np.empty([len(s), len(t)])
score_matrix[0] = 0
score_matrix[0][:] = 0

print(pd.DataFrame(score_matrix))