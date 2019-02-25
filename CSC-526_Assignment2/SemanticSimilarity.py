import csv,re

with open('ontology_ids_superclasses.tsv') as superclasses, open('semantic_similarity_ids.txt', 'r') as ids:
    supr_clses_reader = [(i[0], i[1].split(',')) for i in csv.reader(superclasses, delimiter='\t')]
    subclass = [row[0] for row in supr_clses_reader]
    supr_clses = [row[1] for row in supr_clses_reader]
    ss_ids = []
    gene_names = []
    for id in [re.split(" |,", row.rstrip("\n")) for row in ids]:
        gene_names.append(id.pop(0))
        for item in id:
            if item in subclass:
                item_index = subclass.index(item)
                for sc in supr_clses[item_index]:
                    id.append(sc)
        ss_ids.append(id)

    