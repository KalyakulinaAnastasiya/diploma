import numpy as np
import pickle

file = open('s_pop.txt', 'r')
line = file.readline()
line_list = line.rstrip().split('\t')
sample = line_list.index('sample')
pop = line_list.index('pop')
sample_list = []
dict_national = {}
list_fin = []
list_sp = []
list_it = []
list_br = []
fin = 0
br = 0
sp = 0
it = 0
temp = 0
for line in file:
    line_list = line.rstrip().split('\t')
    if line_list[pop] == "GBR":
        sample_list.append(line_list[sample])
        list_br.append(line_list[sample])
        br += 1
    if line_list[pop] == "FIN":
        sample_list.append(line_list[sample])
        list_fin.append(line_list[sample])
        fin += 1
    if line_list[pop] == "TSI":
        sample_list.append(line_list[sample])
        list_it.append(line_list[sample])
        it += 1
    if line_list[pop] == "IBS":
        sample_list.append(line_list[sample])
        list_sp.append(line_list[sample])
        sp += 1
dict_national['GBR'] = list_br
dict_national['FIN'] = list_fin
dict_national['IBS'] = list_sp
dict_national['TSI'] = list_it
file.close()

file = open('ALL.chrMT.phase3_callmom-v0_4.20130502.genotypes.vcf', 'r')
number_column_list = []
num_str = 0
i = 0
l_br = []
l_fin = []
l_sp = []
l_it = []
for line in file:
    if line[0] == "#":
        i += 1
    line_list = line.rstrip().split('\t')
    if line_list[0] == "#CHROM":
        for var in sample_list:
            if var in line_list:
                number_column_list.append(line_list.index(var))
                if var in dict_national['GBR']:
                    l_br.append(line_list.index(var) - i + 1)
                if var in dict_national['FIN']:
                    l_fin.append(line_list.index(var) - i + 1)
                if var in dict_national['IBS']:
                    l_sp.append(line_list.index(var) - i + 1)
                if var in dict_national['TSI']:
                    l_it.append(line_list.index(var) - i + 1)
    num_str += 1
num_col = len(line_list) - i + 1
num_str -= i
dict_national['GBR'] = l_br
dict_national['FIN'] = l_fin
dict_national['IBS'] = l_sp
dict_national['TSI'] = l_it
file.close()

file = open('ALL.chrMT.phase3_callmom-v0_4.20130502.genotypes.vcf', 'r')
x_table = np.zeros((num_str, num_col), dtype=np.float)
q = 0
for line_num, line in enumerate(file):
    if line_num > i - 1:
        line_list = line.rstrip().split('\t')
        k = 0
        while k < num_col:
            x_table[q, k] = line_list[k + i - 1]
            k += 1
        q += 1
file.close()

with open("x_table", "wb") as handle:
    pickle.dump(x_table, handle, protocol = pickle.HIGHEST_PROTOCOL)
with open("dictinary", "wb") as handle:
    pickle.dump(dict_national, handle, protocol = pickle.HIGHEST_PROTOCOL)