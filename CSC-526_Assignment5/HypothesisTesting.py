# Justin Oakley
# CSC-526 Assignment 5: Hypothesis Testing
# 04/08/19

import pandas as pd, numpy as np
from scipy import stats

# Import data to a Pandas dataframe.
S = pd.read_csv("SemanticSimilarityScores.tsv", sep='\t')

# Take a sample size of 50 with replacement.
sample = S.sample(n=50, replace=True)

# Create a,b for each type of similarity using the Semantic Similarity Scores' columns.
simj_a = sample['SimJ Score MACHINE']
simj_b = sample['SimJ Score HUMAN']
nic_a = sample['NIC Score MACHINE']
nic_b = sample['NIC Score HUMAN']

# Run statistic tests.
t_simj, p_simj = stats.ttest_ind(simj_a, simj_b)
t_nic, p_nic = stats.ttest_ind(simj_a, simj_b)

print("t-Score of Jaccard Similarity Scores: %s\np-Value of Jaccard Similiarity Scores %s" % (t_simj, p_simj))
print("t-Score of Resnik Similarity Scores: %s\np-Value of Resnik Similiarity Scores %s" % (t_nic, p_nic))