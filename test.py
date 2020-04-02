import argparse
import csv

anno_path = 'YG246_annotations.tsv'
product_path = 'Gene-Product-Table.txt'
struc_list = ['LSC', 'SSC', 'IRa', 'IRb']
product_dict = {}
sequin_block = ['>Features YG246']

with open(product_path) as product_file:
    product_reader = csv.reader(product_file, delimiter='\t')
    for product_row in product_reader:
        product_dict[product_row[0]] = product_row[1]

with open(anno_path) as anno_file:
    anno_reader = csv.DictReader(anno_file, delimiter='\t')
    for anno_row in anno_reader:
        if anno_row["Name"] == 'rps12': continue
            
        if anno_row["Name"] in struc_list: continue

        else:
            if anno_row["Type"] != 'exon' and int(anno_row["# Intervals"]) == 1:
                if anno_row["Direction"] == 'forward':
                    gene_block = f'{anno_row["Minimum"]}\t{anno_row["Maximum"]}\tgene\n\t\t\tgene\t{anno_row["Name"]}'
                    type_block = f'{anno_row["Minimum"]}\t{anno_row["Maximum"]}\t{anno_row["Type"]}\n\t\t\tproduct\t{product_dict.get(anno_row["Name"])}'
                    sequin_block.append(gene_block + '\n' + type_block)

                if anno_row["Direction"] == 'reverse':
                    gene_block = f'{anno_row["Maximum"]}\t{anno_row["Minimum"]}\tgene\n\t\t\tgene\t{anno_row["Name"]}'
                    type_block = f'{anno_row["Maximum"]}\t{anno_row["Minimum"]}\t{anno_row["Type"]}\n\t\t\tproduct\t{product_dict.get(anno_row["Name"])}'
                    sequin_block.append(gene_block + '\n' + type_block)

            if anno_row["Type"] != 'exon' and int(anno_row["# Intervals"]) > 1:
                if anno_row["Direction"] == 'forward':
                    gene_block = f'{anno_row["Minimum"]}\t{anno_row["Maximum"]}\tgene\n\t\t\tgene\t{anno_row["Name"]}'
                    type_block = f'{anno_row["Minimum"]}\t{anno_row["Maximum"]}\t{anno_row["Type"]}\n\t\t\tproduct\t{product_dict.get(anno_row["Name"])}'
                    sequin_block.append(gene_block + '\n' + type_block)
                    
                if anno_row["Direction"] == 'reverse':
                    gene_block = f'{anno_row["Maximum"]}\t{anno_row["Minimum"]}\tgene\n\t\t\tgene\t{anno_row["Name"]}'
                    type_block = f'{anno_row["Maximum"]}\t{anno_row["Minimum"]}\t{anno_row["Type"]}\n\t\t\tproduct\t{product_dict.get(anno_row["Name"])}'
                    sequin_block.append(gene_block + '\n' + type_block)

with open('test_sequin.txt', 'a') as sequin_file:
    sequin_join = '\n'.join(sequin_block)
    sequin_file.write(sequin_join)
