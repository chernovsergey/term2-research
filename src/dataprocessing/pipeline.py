from src.auxilary.parseconfigs import *
from src.dataprocessing.preprocessing import *
from src.tools.running import *


class Pipeline:
    files_to_benchmark = []

    def __init__(self, dataconfig, toolconfig):
        self.dataconf = dataconfig
        self.toolconf = toolconfig

        self.ref, \
        self.rep1, self.inp1, \
        self.rep2, self.inp2 = load_data_config(load_yaml(dataconfig))

        for k, v in load_yaml(toolconfig).iteritems():
            setattr(self, k, v)

    def start(self):

        # pooling
        dir = get_basepath(self.rep1[0])

        rep_cond1 = dir + "/pooled_replicates_cond1.bed"
        inp_cond1 = dir + "/pooled_input_cond1.bed"
        make_pooling(self.rep1[0], self.rep1[1], rep_cond1)
        make_pooling(self.inp1[0], self.inp1[1], inp_cond1)

        rep_cond2 = dir + "/pooled_replicates_cond2.bed"
        inp_cond2 = dir + "/pooled_input_cond2.bed"
        make_pooling(self.rep2[0], self.rep2[1], rep_cond2)
        make_pooling(self.inp2[0], self.inp2[1], inp_cond2)

        if hasattr(self, "chipdiff"):
            chipdif_outdir = self.chipdiff['outdir']
            chromosomes = self.chipdiff['chromosomes']
            chipdiff_path = self.chipdiff['path']
            chipdiff_projname = self.chipdiff['projname']

            chipdiff_outfiles = run_chipdiff(bed_to_tag(rep_cond1),
                                             bed_to_tag(rep_cond2),
                                             chipdiff_path,
                                             chipdif_outdir,
                                             chromosomes,
                                             chipdiff_projname)

            self.files_to_benchmark.append(chipdiff_outfiles)

        if hasattr(self, "macs2"):
            macs2_outdir = self.macs2['outdir']
            macs2_path = self.macs2['path']
            macs2_projname = self.macs2['projname']

            macs2_outfiles = run_macs2(rep_cond1, rep_cond2,
                                       inp_cond1, inp_cond2,
                                       macs2_path, macs2_outdir, macs2_projname)

            self.files_to_benchmark.append(macs2_outfiles)

        if hasattr(self, "zinbra"):
            zinbra_output = self.zinbra['outdir']
            zinbra_path = self.zinbra['path']
            zinbra_outfiles = zinbra_output + "/{0}.bed".format(self.zinbra['projname'])
            only = self.zinbra['only_chr']

            run_zinbra_compare(ref=self.ref,
                               rep1_1=self.rep1[0], rep1_2=self.rep1[1],
                               rep2_1=self.rep2[0], rep2_2=self.rep2[1],
                               outfname=zinbra_outfiles, path=zinbra_path, only=only)

            self.files_to_benchmark.append(zinbra_outfiles)

        for i in self.files_to_benchmark:
            print i
