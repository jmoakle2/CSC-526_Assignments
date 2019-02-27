import csv,re,math

def all_pairs_sim_j(gene1, gene2, ids_1, ids_2):
    pairs = [(x[0],y[0]) for x in ids_1 for y in ids_2]
    values = [len(set(x + y))/len(x + y) for x in gene1 for y in gene2]
    return list(zip(pairs, values))

def best_pairs_sim_j(all_pairs, original):
    all_pairs = [max([x for x in all_pairs if x[0][0] == y[0]]) for y in original]
    return all_pairs

def best_pairs_sim_resnik(gene1, gene2):
    lcs = []
    for x in gene1:
        for y in gene2:
            for x_item in x:
                if x_item in y:
                    lcs.append(x_item)
                    break
    values = [0 - math.log10((len([item for x in gene1 if item in x])
                              + len([item for y in gene2 if item in y])) / 2)
              for item in lcs]
    return list(zip(lcs, values))

with open('ontology_ids_superclasses.tsv') as superclasses, open('semantic_similarity_ids.txt', 'r') as ids:
    supr_clses_reader = [(i[0], i[1].split(',')) for i in csv.reader(superclasses, delimiter='\t')]
    subclass = [row[0] for row in supr_clses_reader]
    supr_clses = [row[1] for row in supr_clses_reader]
    ss_ids = []
    gene_names = []
    for ids in [re.split(" |,", row.rstrip("\n")) for row in ids]:
        gene_names.append(ids.pop(0))
        ss_ids.append([[x] for x in ids])

    inferred = [[x + supr_clses[subclass.index(x[0])] for x in gene] for gene in ss_ids]
    num_1 = all_pairs_sim_j(inferred[0], inferred[2], ss_ids[0], ss_ids[2])
    print("Jaccard All Pairs similarity between GeneA and GeneC:", num_1)
    num_2 = best_pairs_sim_j(num_1, ss_ids[0])
    print("Jaccard Best Pairs similarity between GeneA and GeneC:", num_2)
    num_3 = best_pairs_sim_resnik(inferred[0], inferred[1])
    print("Resnik Best Pairs similarity between GeneA and GeneB:", num_3)