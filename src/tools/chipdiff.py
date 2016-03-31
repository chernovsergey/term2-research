from abstracttool import AbstractTool
from src.auxilary.utility import *


class ChipDiff(AbstractTool):
    libraries = []

    def __init__(self, path):
        self.where_chipdiff = path

    def configure_data(self, lib1, lib2):
        if lib1 is not None and lib2 is not None:
            self.libraries = [lib1, lib2]

    def configure_run_params(self, chr_description_file, max_iter=500,
                             max_region_dist=1000,
                             min_fold_change=3.0, min_p=0.95, min_training_seq_num=10000):

        self.chrdescr = chr_description_file
        write_line = lambda arg, val: config_file.write("{0}\t{1}".format(arg, val))

        with open("config.txt", "w+") as config_file:
            write_line("maxIterationNum", max_iter)
            write_line("minRegionDist", max_region_dist)
            write_line("minFoldChange", min_fold_change)
            write_line("minP", min_p)
            write_line("maxTrainingSeqNum", min_training_seq_num)

    def run(self, prefix):
        if len(self.libraries) == 0:
            raise Error("Libraries not set!")

        if prefix is not None:
            if prefix != "":
                self.projname = prefix
            else:
                raise Error("Passed empty project name")
        else:
            raise Error("Project name hasn't been set")

        input = " ".join(self.libraries)

        # Usage: ./ChIPDiff sample_L1.tag sample_L2.tag chrom_descr.txt config.txt sample
        runstring = "{0}/myChIPDiff {1} {2} {3} {4}".format(self.where_chipdiff,
                                                            input, self.chrdescr,
                                                            self.where_chipdiff + "config.txt",
                                                            self.projname)

        sh(runstring)
