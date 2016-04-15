from abstracttool import AbstractTool
from src.dataprocessing.preprocessing import *


class MAnorm(AbstractTool):
    def __init__(self, path):
        self.where_manorm = path

    def configure_run_params(self, outdir, d1, d2, projname="diff_cond1_cond2"):
        if outdir is not None:
            self.outdir = outdir
        else:
            raise Error("Wrong outdir path")

        if None not in [d1, d2]:
            self.d1 = d1
            self.d2 = d2

        self.projname = projname

    def configure_data(self, summits1=None, summits2=None, cond1=None, cond2=None):

        if None in [summits1, summits2, cond1, cond2]:
            raise Error("Wrong input files")
        else:
            self.conditions = [cond1, cond2]
            self.peaks = [summits1, summits2]

    def run(self):
        if len(self.conditions) != 4 and len(self.peaks) != 2:
            raise Error("Controls and conditions has not been set")

        runstring = "cp {0}/MAnorm.sh {1}; " \
                    "cp {0}/MAnorm.R {1}; " \
                    "cd {1}; ./MAnorm.sh" \
                    " {2}" \
                    " {3}" \
                    " {4}" \
                    " {5}" \
                    " {6} {7}" \
            .format(self.where_manorm, self.outdir,
                    self.peaks[0], self.peaks[1],
                    self.conditions[0], self.conditions[1],
                    self.d1, self.d2)

        sh(runstring)
