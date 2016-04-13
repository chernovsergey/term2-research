from abstracttool import AbstractTool
from src.dataprocessing.preprocessing import *


class MAnorm(AbstractTool):
    def __init__(self, path):
        self.where_manorm = path

    def configure_run_params(self, outdir, d1, d2):
        if outdir is not None:
            self.outdir = outdir
        else:
            raise Error("Wrong outdir path")

        if None not in [d1, d2]:
            self.d1 = d1
            self.d2 = d2

    def configure_data(self, summits1=None, summits2=None,
                       cond1_rep1=None, cond1_rep2=None,
                       cond2_rep1=None, cond2_rep2=None):

        if None in [summits1, summits2, cond1_rep1, cond1_rep2, cond2_rep1, cond2_rep2]:
            raise Error("Wrong input files")
        else:
            self.conditions = [cond1_rep1, cond1_rep2, cond2_rep1, cond2_rep2]
            self.peaks = [summits1, summits2]


    def run(self):
        if len(self.conditions) != 4 and len(self.peaks) != 2:
            raise Error("Controls and conditions has not been set")

        runstring = "cp {0}/MAnorm3.sh {1}; " \
                    "cp {0}/MAnorm3.R {1}; " \
                    "cd {1}; ./MAnorm3.sh" \
                    " project_cond1_cond2" \
                    " {2}" \
                    " {3}" \
                    " {4}" \
                    " {5}" \
                    " {6} {6} {7} {7}".format(self.where_manorm, self.outdir,
                                              self.conditions[0], self.conditions[1],
                                              self.conditions[2], self.conditions[3],
                                              self.d1, self.d2)

        sh(runstring)
