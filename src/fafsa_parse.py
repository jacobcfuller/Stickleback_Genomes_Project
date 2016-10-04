import os

# I'll assume you saved the fasta file to your Desktop
os.chdir("/home/jcfuller/Documents/White_lab/Stickleback_Genomes_Project/depth_analysis")

fasta_file = 'revisedAssemblyUnmasked.fa'

name_list = []
length_list = []
current_length = 0

with open(fasta_file, 'rt') as file:
    for line in file:
        # Lines with names of sequences
        if line.startswith('>'):
            name_list += [line.strip().lstrip('>')]
            # If current_length == 0, then this must be the first line, so no need to
            # append to length_list yet
            if current_length > 0:
                length_list += [current_length]
            # Reset current_length, an object holding the current chromo's sequence length
            current_length = 0
        # Sequence lines
        else:
            current_length += len(line.strip())
# Append current_length to length_list one last time to add the last chromosome's length
length_list += [current_length]
print('done')

length_dict = {x:y for x,y in zip(name_list, length_list)}

print(length_dict)
