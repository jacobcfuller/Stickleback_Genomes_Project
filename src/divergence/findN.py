#!/home/jcfuller/anaconda3/bin/python3.5

fa_file = ("/home/jcfuller/Documents/White_lab/Stickleback_Genomes_Project/doc"
           "/Y_Chr_JoinedAssembly.fa")

pos = 0
with open(fa_file) as fa:
    header = next(fa)
    for line in fa:
        if ">" in line:
            break
        if "N" in line:
            pos += len(line.split('N')[0])
            break
        pos += len(line.strip())
