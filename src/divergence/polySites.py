#!/home/jcfuller/anaconda3/bin/python3.5
'''Finds snps unique to Y chromosome
'''
# Must remove 82M19 unordered scaffold before using this
import argparse
import math
import pandas as pd

Y_len = 12341907


def makeDF(snpTable):
    '''Import Y chromosome SNP call table into panda dataframe.
       table should have 3 columns in the following order:
       POS  REF  ALT
       Only uses POS for now, but retain others for future functionality
    '''
    snpDF = pd.read_table(snpTable, low_memory=False)

    return snpDF


# reaches maximum recusion if too many 0s?
def fillInZeros(maleDF, index, winCount, incr):
    '''If the bp location of the next SNP call is greater than window size,
       fill in with '0' for 0 SNPs in that window.
       Increments winCount and returns the new count for slideWindow.
    '''
    mDF = maleDF
    while(mDF.iloc[index+1]['POS'] >= (incr*winCount)):
        print(str(incr*winCount)+'\t'+'0')
        winCount += 1
    else:
        return winCount


def slideWindow(maleFile, femaleFile, incr, name):
    '''Sliding window count of SNPs that are present in male Y VCF, but not
       female, assuming that these are unique Y chr polymorphisms.
       Prints bp position and snp count for that window.
    '''
    mDF = makeDF(maleFile)
    fDF = makeDF(femaleFile)
    # file header
    print("pos"+'\t'+name)
    snpCount = 0
    winCount = 1
    # remember DF is 0-index
    for index in mDF.index:
        # If SNP call doesn't exist in female, count
        if((mDF.iloc[index]['POS'] in fDF['POS'].values) is False):
            snpCount += 1
        # this may need to be modified, but right now fixes table end
        if(index == (len(mDF)-1)):
            print(str(incr*winCount)+'\t'+str(snpCount))
            end = math.ceil((Y_len - incr*winCount)/1000)
            for i in range(end):
                winCount += 1
                print(str(incr*winCount)+'\t'+"0")
            return()
        # need to figure out tail end of dataframe
        if(mDF.iloc[index+1]['POS'] >= (incr*winCount)):
            print(str(incr*winCount)+'\t'+str(snpCount))
            # reset counter
            snpCount = 0
            # check if there are actually snps in the next window
            winCount += 1
            winCount = fillInZeros(mDF, index, winCount, incr)


# ======================== #
#           Main           #
# ======================== #


if __name__ == '__main__':
    ScriptDescript = '''Sliding window SNP count'''
    Parser = argparse.ArgumentParser(description=ScriptDescript)
    Parser.add_argument('-m', '--maleFile', type=str, metavar='M',
                        required=True)
    Parser.add_argument('-f', '--femaleFile', type=str, metavar='F',
                        required=True)
    Parser.add_argument('-n', '--name', type=str, metavar='N',
                        required=True)
    Parser.add_argument('-i', '--increment', type=float, metavar='I',
                        required=True)
    args = vars(Parser.parse_args())

    # Set args to variables
    maleFile = args['maleFile']
    femaleFile = args['femaleFile']
    incr = int(args['increment'])
    name = args['name']
    del args
    slideWindow(maleFile, femaleFile, incr, name)
