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

    def configure_data(self, cond1=None, control1=None, cond2=None, control2=None):
        if cond1 is not None and cond2 is not None:
            self.conditions = [cond1, cond2]
        else:
            raise Error("Wrong condition files")

        if control1 is not None and control2 is not None:
            self.controls = [control1, control2]
        else:
            raise Error("Wrong control files")

    def run(self):
        if len(self.conditions) != 2 and len(self.controls) != 2:
            raise Error("Controls and conditions has not been set")

        runstring = "cp {0}/MAnorm.sh {1}; " \
                    "cp {0}/MAnorm.r {1}; " \
                    "cd {1}; ./MAnorm.sh" \
                    " {2}" \
                    " {3}" \
                    " {4}" \
                    " {5}" \
                    " {6} {7}".format(self.where_manorm, self.outdir,
                                      self.conditions[0], self.conditions[1],
                                      self.controls[0], self.controls[1],
                                      self.d1, self.d2)

        sh(runstring)
