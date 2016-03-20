from util import *


class Zinbra():
    reference = ""
    where_zinbra = ""
    replicates_pool = list()

    def __init__(self, path_to_zinbra):
        self.where_zinbra = path_to_zinbra

    def set_reference(self, path):
        self.reference = path

    def add_replicates(self, files_list):
        if len(files_list) == 0:
            raise Error("Passed empty list of files")

        self.replicates_pool.append(files_list)

    def clean_replicates(self):
        self.replicates_pool = []

    def run_analyze(self, fdr=None, bed=None, only=None):
        num_replicates = len(self.replicates_pool)

        if num_replicates == 0:
            raise Error("List of replicates has not been set")
        elif num_replicates == 1:
            input = self.replicates_pool[0][1]
        else:
            input = ",".join(self.replicates_pool[0])

        runstring = "java -jar {2}/zinbra.jar analyze" \
                    " -r {0}" \
                    " -b 200" \
                    " -i {1}".format(self.reference, input, self.where_zinbra)

        if bed is not None:
            if bed != "":
                runstring += " --bed {0}".format(bed)

        if fdr is not None:
            runstring += " --fdr {0}".format(fdr)

        if only is not None:
            runstring += " --only {0}".format(only)

        run_in_shell(runstring)

    def run_compare(self):
        if len(self.replicates_pool[0]) < 2:
            raise Error("Not enough files to compare")

        num_replicates = len(self.replicates_pool[0])
        if num_replicates == 1:
            condition1 = self.replicates_pool[0][:1]
            condition2 = self.replicates_pool[1][:1]
        else:
            condition1 = ",".join(self.replicates_pool[0])
            condition2 = ",".join(self.replicates_pool[1])

        run_in_shell("java -jar {2}/zinbra.jar compare "
                     " -r {0}"
                     " -b 200"
                     " -1 {1}"
                     " -2 {2}".format(self.reference,
                                      condition1, condition2,
                                      self.where_zinbra))
