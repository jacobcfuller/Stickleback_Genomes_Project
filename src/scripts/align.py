
import os
from subprocess import call

for f in os.listdir('.'):
    if os.path.isfile(f):
        popTxt = open(f)
        popName = str(f[:len(f)-4])
        line = popTxt.readline()
        while line:
            call(["../sub_scripts/stick_alignment_submission.sh",
                 ("-s %s" % str(line[:len(line)-1])),
                 ("-d %s" % "feulner/"+str(popName))])
            line = popTxt.readline()
