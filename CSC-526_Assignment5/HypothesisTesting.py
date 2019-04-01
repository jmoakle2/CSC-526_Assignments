# Justin Oakley
# CSC-526 Assignment 5: Hypothesis Testing
# 04/08/19

import pandas as pd, numpy as np
from scipy import stats

S = pd.read_csv("SemanticSimilarityScores.tsv", sep='\t')
S_cols = S.drop(columns='Character Number').columns

for col in S_cols:
    S['norm_' + col] = (S[col] - S[col].min()) / (S[col].max() - S[col].min())

S = S.drop(columns=S_cols)
ttest = stats.ttest_rel(S['norm_SimJ Score MACHINE'], S['norm_SimJ Score HUMAN'])
print(ttest)