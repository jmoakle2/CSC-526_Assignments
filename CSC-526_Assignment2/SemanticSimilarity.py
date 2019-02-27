# Justin Oakley
# CSC-526 Assignment 2: Semantic Similarity
# 02/27/19

import csv, re, math

# This method calculates all pairs between the given genes using Jaccard similarity.
def all_pairs_sim_j(gene1, gene2, ids_1, ids_2):
    pairs = [(x[0], y[0]) for x in ids_1 for y in ids_2]
    values = [len(set(x + y))/len(x + y) for x in gene1 for y in gene2]
    return list(zip(pairs, values))

# This method calculates the best pairs between the given genes using Jaccard similarity.
def best_pairs_sim_j(all_pairs, original):
    all_pairs = [max([x for x in all_pairs if x[0][0] == y[0]]) for y in original]
    return all_pairs

# This method calculates the best pairs between the given genes using Resnik similarity.
def best_pairs_sim_resnik(gene1, gene2):
    lcs = []

    for x in gene1:
        for y in gene2:
            for x_item in x:
                if x_item in y:
                    lcs.append(x_item)
                    break

    values = [0 - math.log10((len([item for x in gene1 if item in x])
                              + len([item for y in gene2 if item in y])) / 2) for item in lcs]

    return list(zip(lcs, values))

# The following code reads the "ontology_ids_superclasses.tsv" file, which contains all the superclasses that were
# retrieved from the Java program file, and the "semantic_similarity_ids.txt" file, which contains all the GO
# identifiers that are to be utilized for the assignment. Then after reading said files, the data is cleaned and
# placed into lists.
with open('ontology_ids_superclasses.tsv') as superclasses, open('semantic_similarity_ids.txt', 'r') as ids:
    supr_clses_reader = [(i[0], i[1].split(',')) for i in csv.reader(superclasses, delimiter='\t')]
    subclass = [row[0] for row in supr_clses_reader]
    supr_clses = [row[1] for row in supr_clses_reader]
    explicit = []
    gene_names = []

    for ids in [re.split(" |,", row.rstrip("\n")) for row in ids]:
        gene_names.append(ids.pop(0))
        explicit.append([[x] for x in ids])

    # The inferred set of GO identifiers.
    inferred = [[x + supr_clses[subclass.index(x[0])] for x in gene] for gene in explicit]

    # 1. All Pairs using Jaccard Similarity
    num_1 = all_pairs_sim_j(inferred[0], inferred[2], explicit[0], explicit[2])

    print("All Pairs (Using Jaccard Similarity) between GeneA and GeneC:", num_1)
    print("All Pairs Average of GeneA and GeneC:", sum([x[1] for x in num_1]) / len(num_1))

    # 2. Best Pairs using Jaccard Similarity
    num_2 = best_pairs_sim_j(num_1, explicit[0])

    print("Best Pairs (Using Jaccard Similarity) between GeneA and GeneC:", num_2)
    print("Best Pairs Average of GeneA and GeneC:", sum([x[1] for x in num_2]) / len(num_2))

    # 3. Best Pairs using Resnik Similarity
    num_3 = best_pairs_sim_resnik(inferred[0], inferred[1])

    print("Best Pairs (Using Resnik Similarity) between GeneA and GeneB:", num_3)
    print("Best Pairs Average of GeneB and GeneC:", sum([x[1] for x in num_3]) / len(num_3))
