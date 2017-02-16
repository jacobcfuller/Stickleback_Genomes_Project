
import os
from subprocess import call

for d in os.listdir('.'):
    for f in os.listdir(d):
        txtF = open(d+'/'+f)
        line = txtF.readline()
        while line:
            call(["../sub_scripts/sra_download_submission.sh",
                 ("-a %s" % str(line[:len(line)-1])),
                 ("-i %s" % str(f[:(len(f)-4)])),
                 ("-d %s" % str(d))])
            line = txtF.readline()
