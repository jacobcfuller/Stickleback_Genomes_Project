# Calculating values using PopGenome in R and using python


from rpy2.robjects.packages import importr


def Roman():
    data = []
    new_chr = []
    with open("Chromosomes_Size.txt", 'r') as input:
        for line in input:
            data += line.split()
        chr = data[2::2]
        for value in chr:
            if value == "1":
                new_chr.append("chrI")
            elif value == "2":
                new_chr.append("chrII")
            elif value == "3":
                new_chr.append("chrIII")
            elif value == "4":
                new_chr.append("chrIV")
            elif value == "5":
                new_chr.append("chrV")
            elif value == "6":
                new_chr.append("chrVI")
            elif value == "7":
                new_chr.append("chrVII")
            elif value == "8":
                new_chr.append("chrVIII")
            elif value == "9":
                new_chr.append("chrIX")
            elif value == "10":
                new_chr.append("chrX")
            elif value == "11":
                new_chr.append("chrXI")
            elif value == "12":
                new_chr.append("chrXII")
            elif value == "13":
                new_chr.append("chrXIII")
            elif value == "14":
                new_chr.append("chrXIV")
            elif value == "15":
                new_chr.append("chrXV")
            elif value == "16":
                new_chr.append("chrXVI")
            elif value == "17":
                new_chr.append("chrXVII")
            elif value == "18":
                new_chr.append("chrXVIII")
            elif value == "19":
                new_chr.append("chrXIX")
            elif value == "20":
                new_chr.append("chrXX")
            elif value == "21":
                new_chr.append("chrXXI")
    return new_chr


def calc_within():
    data = []
    chr_roman = Roman()
    new_results = []
    with open("PS_sizes.txt", 'r') as input, open("PopGenome_PS.txt", 'a') as output:
        for line in input:
            data += line.split()
        chr_num = data[2::2]
        size = data[3::2]
        pop = importr('PopGenome')
        header = "File" + '\t' + "Chr" + '\t' + "Start Pos" + '\t' + "End Pos" + '\t' + "Pi_within" + '\t' + "TajD" + '\t' + "Watt Theta" + '\n'
        output.write(header)
        i = 1
        for index, value in enumerate(chr_roman):
            startpos = 1
            endpos = 2000
            while i < int(size[index]):
                filename = "PS" + str(chr_num[index]) + "B.vcf.gz"
                thing = pop.readVCF(filename,numcols=10,tid=value,frompos=startpos,topos=endpos,include_unknown=True)
                neut = pop.neutrality_stats(thing)
                x = pop.get_neutrality(neut,theta = True)
                results_neut = x[0]
                results_neut = [str(a) for a in results_neut]
                for val in results_neut:
                    if val == "NA":
                        new_results.append("0")
                    else:
                        new_results.append(val)
                tajD = str(round(float(new_results[0]), 6))
                theta = round(float(new_results[10]) / 2000, 6)
                watt_theta = str(theta)
                diver = pop.diversity_stats(thing,pi = True)
                y = pop.get_diversity(diver)
                results_div = y[0]
                pi = str(round(results_div[2] /2000,6))
                final = str(filename) + '\t' + value + '\t' + str(i) + '\t' + str(i+1999) + '\t' + pi + '\t' + tajD + '\t' + watt_theta + '\n'
                output.write(final)
                new_results = []
                startpos += 1000
                endpos += 1000
                i += 1000
            i = 1

calc_within()
