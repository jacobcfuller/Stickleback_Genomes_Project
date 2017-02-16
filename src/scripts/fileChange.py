# to be run on sapelo
'''program to change/move a bunch of file names at once (for input into bowtie)
'''
import os

for d in os.listdir('.'):
    os.chdir(d)

    #change all files in dir
    [os.rename(f, f.replace('R1_001', '1')) for f in os.listdir('.') if not f.startswith('.')]

    [os.rename(f, f.replace('R2_001', '2')) for f in os.listdir('.') if not f.startswith('.')]


    [os.rename(f, f.replace(f[:(len(f)-12)], os.path.split(os.getcwd())[1])) for f in os.listdir('.') if not f.startswith('.')]

    for f in os.listdir('.'):
        os.rename(f, "../"+f)
    os.chdir("../")
