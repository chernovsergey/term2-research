from abstracttool import AbstractTool
from src.auxilary.utility import *


class SICER(AbstractTool):
    def __init__(self, path):
        self.where_sicer = path

    def configure_data(self, cond1=None, control1=None, cond2=None, control2=None):
        if cond1 is not None and cond2 is not None:
            self.conditions = [cond1, cond2]
        else:
            raise Error("Wrong condition files")

        if control1 is not None and control2 is not None:
            self.controls = [control1, control2]
        else:
            raise Error("Wrong control files")

    def configure_run_params(self, outdir, windowsize=200, gap=200, fdr1=0.01, fdr2=0.01):
        if outdir is not None:
            self.outdir = outdir
        else:
            raise Error("Wrong outdir path")

        self.windowsize = windowsize
        self.gap = gap
        self.fdr1 = fdr1
        self.fdr2 = fdr2

    def run(self):

        get_base = lambda x: os.path.basename(x)
        self.datadir = os.path.split(self.controls[0])[0]

        runstring = "export SICER=\"{2}\"; " \
                    "export DATADIR=\"{0}\"; " \
                    "export OUTPUTDIR=\"{1}\"; " \
                    "cd {2}; " \
                    "./SICER-df.sh {3} {4} {5} {6} {7} {8} {9} {10}".format(
            self.datadir, self.outdir, self.where_sicer,
            get_base(self.conditions[0]), get_base(self.controls[0]),
            get_base(self.conditions[1]), get_base(self.controls[1]),
            self.windowsize, self.gap, self.fdr1, self.fdr2)

        sh(runstring)
