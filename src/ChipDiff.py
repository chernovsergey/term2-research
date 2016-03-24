from Utility import *
import os.path

class ChipDiff():
    libraries = []

    def __init__(self, path):
        self.where_chipdiff = path

    def set_libraries(self, lib1, lib2):
        if lib1 is not None and lib2 is not None:
            self.libraries = [lib1, lib2]

    def configure(self, project_name, chr_description_file, max_iter=500, max_region_dist=1000,
                  min_fold_change=3.0, min_p=0.95, min_training_seq_num=10000):

        self.projname = project_name
        self.chrdescr = chr_description_file

        write_line = lambda arg, val: config_file.write("{0}\t{1}".format(arg, val))

        with open("config.txt", "w+") as config_file:
            write_line("maxIterationNum", max_iter)
            write_line("minRegionDist", max_region_dist)
            write_line("minFoldChange", min_fold_change)
            write_line("minP", min_p)
            write_line("maxTrainingSeqNum", min_training_seq_num)

    def convert_to_tag(self, library):
        name = str.split(library, ".bed.gz")[0]
        if not os.path.exists(name + ".tag"):
            run_in_shell("gunzip -c {0} > {1}".format(library, name + ".bed"))
            run_in_shell("cat  {0}.bed | cut -f3,4,5 --complement > {1}.tag".format(name, name))
            run_in_shell("rm {0}.bed".format(name))
        return name + ".tag"

    def run(self):
        if len(self.libraries) == 0:
            raise Error("Libraries not set!")

        lib1 = self.convert_to_tag(self.libraries[0])
        lib2 = self.convert_to_tag(self.libraries[1])
        input = " ".join([lib1, lib2])

        # Usage: ./ChIPDiff sample_L1.tag sample_L2.tag chrom_descr.txt config.txt sample
        runstring = "{0}/myChIPDiff {1} {2} {3} {4}".format(self.where_chipdiff,
                                                            input, self.chrdescr,
                                                            self.where_chipdiff + "config.txt",
                                                            self.projname)

        run_in_shell(runstring)
