from src.tools.chipdiff import *
from src.tools.macs2 import *
from src.tools.zinbra import *


def run_macs2(rep1, rep2, input_rep1, input_rep2, output_folder, prefix):
    macs2 = MACS2(path="/home/denovo/miniconda/bin")
    macs2.configure_run_params(outdir=output_folder, maxgap=60)
    macs2.configure_data(cond1=rep1, control1=input_rep1,
                         cond2=rep2, control2=input_rep2)
    macs2.run(prefix=prefix)
    return output_folder + prefix + "_c3.0_common.bed"


def run_chipdiff(rep1, rep2, tool_path, outdir, chr_description_fname, prefix):
    chipdiff = ChipDiff(tool_path)
    chipdiff.configure_run_params(chr_description_file=chr_description_fname)
    chipdiff.configure_data(rep1, rep2)
    chipdiff.run(prefix)

    run_in_shell("mv {0}.bin {1}".format(prefix, outdir))
    run_in_shell("mv {0}.hmm {1}".format(prefix, outdir))
    run_in_shell("mv {0}.region {1}".format(prefix, outdir))
    run_in_shell("mv config.txt {1}".format(prefix, outdir))
    return outdir + prefix + ".region"


def run_zinbra_analyze(ref, rep1, rep2, outfilename, zibra_path, only=None, fdr=0.001):
    zinbra = Zinbra(zibra_path)
    zinbra.configure_run_params(fdr=fdr, only=only)
    zinbra.configure_data(reference=ref, condition1_rep1=rep1, condition1_rep2=rep2)
    zinbra.run(bed=outfilename)


def run_zinbra_compare(ref, rep1_1, rep1_2, rep2_1, rep2_2, outfname, path, only=None, fdr=0.001):
    zinbra = Zinbra(path)
    zinbra.configure_run_params(fdr=fdr, only=only)
    zinbra.configure_data(reference=ref, condition1_rep1=rep1_1, condition1_rep2=rep1_2,
                          condition2_rep1=rep2_1, condition2_rep2=rep2_2)
    zinbra.run(bed=outfname, compare=True)
