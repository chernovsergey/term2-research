from abstracttool import AbstractTool
from src.dataprocessing.preprocessing import *


class MAnorm(AbstractTool):
    def __init__(self, path):
        self.where_manorm = path

    def preprocess_if_necessary(self):
        ex = "mnr"
        cond_cols = [4, 5, 6]
        ctrl_cols = [4, 5]
        self.conditions[0] = drop_columns_and_save(self.conditions[0], ex, cond_cols)
        self.conditions[1] = drop_columns_and_save(self.conditions[1], ex, cond_cols)
        self.controls[0] = drop_columns_and_save(self.controls[0], ex, ctrl_cols)
        self.controls[1] = drop_columns_and_save(self.controls[1], ex, ctrl_cols)

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

        self.preprocess_if_necessary()

        runstring = "cp {0}/MAnorm.sh {1}" \
                    "cp {0}/MAnorm.r {1} " \
                    "cd {1}; ./MAnorm.sh" \
                    " {2}" \
                    " {3}" \
                    " {4}" \
                    " {5}" \
                    " {6} {7}".format(self.where_manorm, self.outdir,
                                      self.conditions[0], self.conditions[1],
                                      self.controls[0], self.controls[1],
                                      self.d1, self.d2)

        run_in_shell(runstring)
