from abstracttool import AbstractTool
from src.auxilary.etility import *


class Zinbra(AbstractTool):
    def __init__(self, path_to_zinbra):
        self.where_zinbra = path_to_zinbra
        self.replicates_pool = [["", ""], ["", ""]]

    def configure_data(self, reference=None,
                       condition1_rep1=None, condition1_rep2=None,
                       condition2_rep1=None, condition2_rep2=None):

        if reference is not None:
            self.reference = reference

        if condition1_rep1 is not None:
            self.replicates_pool[0][0] = condition1_rep1

        if condition1_rep2 is not None:
            self.replicates_pool[0][1] = condition1_rep2

        if condition2_rep1 is not None:
            self.replicates_pool[1][0] = condition2_rep1

        if condition2_rep2 is not None:
            self.replicates_pool[1][1] = condition2_rep2

    def configure_run_params(self, fdr=None, bed=None, only=None):
        if fdr is not None:
            self.fdr = fdr

        if bed is not None:
            self.bed = bed

        if only is not None:
            self.only = only

    def run_analyze(self):
        repsize = map(len, self.replicates_pool)
        if 0 in repsize:
            raise Error("List of replicates has not been set")

        input = ",".join(map(str, self.replicates_pool[0]))

        runstring = "java -jar {0}/zinbra.jar analyze" \
                    " -r {1}" \
                    " -b 200" \
                    " -i {2}".format(self.where_zinbra, self.reference, input, )

        runstring += " --bed {0}".format(self.bed)

        if self.fdr is not None:
            runstring += " --fdr {0}".format(self.fdr)

        if self.only is not None:
            runstring += " --only {0}".format(self.only)

        run_in_shell(runstring)

    def run_compare(self):
        if list(map(len, self.replicates_pool)) not in [[2, 2], [1, 1]]:
            raise Error("Missing condition files to compare")

        condition1 = ",".join(map(str, self.replicates_pool[0]))
        condition2 = ",".join(map(str, self.replicates_pool[1]))

        runstring = "java -jar {0}/zinbra.jar compare " \
                    " -r {1}" \
                    " -b 200" \
                    " -1 {2}" \
                    " -2 {3}".format(self.where_zinbra, self.reference, condition1, condition2)
        runstring += " --bed {0}".format(self.bed)
        runstring += " --fdr {0}".format(self.fdr)
        runstring += " --only {0}".format(self.only)

        run_in_shell(runstring)

    def run(self, compare=False, bed=None):
        if bed is not None:
            if bed != "":
                self.bed = bed

        if compare:
            self.run_compare()
        else:
            self.run_analyze()
