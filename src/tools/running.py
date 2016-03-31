from src.tools.chipdiff import *
from src.tools.macs2 import *
from src.tools.manorm import *
from src.tools.zinbra import *


def run_macs2(rep1, rep2, input_rep1, input_rep2, macs2_path, output_folder, prefix):
    macs2 = MACS2(path=macs2_path)
    macs2.configure_run_params(outdir=output_folder, maxgap=60)
    macs2.configure_data(cond1=rep1, control1=input_rep1,
                         cond2=rep2, control2=input_rep2)
    macs2.run(prefix=prefix)
    file_cond1 = output_folder + prefix + "_c3.0_cond1.bed"
    file_cond2 = output_folder + prefix + "_c3.0_cond2.bed"
    file_commn = output_folder + prefix + "_c3.0_common.bed"
    return file_cond1, file_cond2, file_commn


def run_chipdiff(rep1, rep2, tool_path, outdir, chr_description_fname, prefix):
    chipdiff = ChipDiff(tool_path)
    chipdiff.configure_run_params(chr_description_file=chr_description_fname)
    chipdiff.configure_data(rep1, rep2)
    chipdiff.run(prefix)

    sh("mv {0}.bin {1}".format(prefix, outdir))
    sh("mv {0}.hmm {1}".format(prefix, outdir))
    sh("mv {0}.region {1}".format(prefix, outdir))
    sh("mv config.txt {1}".format(prefix, outdir))
    return outdir + prefix + ".region"


def run_zinbra_analyze(ref, rep1, rep2, outfilename, zibra_path, only=None, fdr=0.001):
    zinbra = Zinbra(zibra_path)
    zinbra.configure_run_params(fdr=fdr, only=only)
    zinbra.configure_data(reference=ref, condition1_rep1=rep1, condition1_rep2=rep2)
    zinbra.run(bed=outfilename)


def run_zinbra_compare(ref, rep1_1, rep1_2, rep2_1, rep2_2, outfname, path, only=None, fdr=0.01):
    zinbra = Zinbra(path)
    zinbra.configure_run_params(fdr=fdr, only=only)
    zinbra.configure_data(reference=ref, condition1_rep1=rep1_1, condition1_rep2=rep1_2,
                          condition2_rep1=rep2_1, condition2_rep2=rep2_2)
    zinbra.run(bed=outfname, compare=True)


def run_manorm(cond1, cond2, control1, control2, manorm_path, macs2_path, outdir):
    macs2 = MACS2(macs2_path)
    t1, c1, d1 = macs2.callpeaks(cond1, control1, "manorm_cond1", 120, outdir)
    t2, c2, d2 = macs2.callpeaks(cond2, control2, "manorm_cond2", 120, outdir)

    ex = "manorm"
    cond_cols = [4, 5, 6]
    ctrl_cols = [4, 5]
    cond1 = rmcols_reformat(cond1, ex, cond_cols)
    cond2 = rmcols_reformat(cond2, ex, cond_cols)
    control1 = rmcols_reformat(control1, ex, ctrl_cols)
    control2 = rmcols_reformat(control2, ex, ctrl_cols)

    manorm = MAnorm(manorm_path)
    manorm.configure_run_params(outdir, d1, d2)
    manorm.configure_data(cond1, control1, cond2, control2)
    manorm.run()
