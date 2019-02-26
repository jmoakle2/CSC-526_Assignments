import csv,re,math

def sim_j(gene1, gene2):
    return [len(set(x + y))/len(x + y) for x in gene1 for y in gene2]

with open('ontology_ids_superclasses.tsv') as superclasses, open('semantic_similarity_ids.txt', 'r') as ids:
    supr_clses_reader = [(i[0], i[1].split(',')) for i in csv.reader(superclasses, delimiter='\t')]
    subclass = [row[0] for row in supr_clses_reader]
    supr_clses = [row[1] for row in supr_clses_reader]
    ss_ids = []
    gene_names = []
    for ids in [re.split(" |,", row.rstrip("\n")) for row in ids]:
        gene_names.append(ids.pop(0))
        ss_ids.append([[x] for x in ids])

    ss_ids = [[x + supr_clses[subclass.index(x[0])] for x in gene] for gene in ss_ids]

    print("Jaccard All Pairs similarity between GeneA and GeneC:", sim_j(ss_ids[0], ss_ids[2]))
    print("Jaccard Best Pairs similarity between GeneA and GeneC:", sim_j(ss_ids[0], ss_ids[2]))