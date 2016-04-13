from src.tools.chipdiff import *
from src.tools.macs2 import *
from src.tools.sicer import SICER
from src.tools.zinbra import *


def run_macs2(rep1, rep2, input_rep1, input_rep2, macs2_path, output_folder, prefix):
    macs2 = MACS2(macs2_path)
    macs2.configure_run_params(output_folder)
    macs2.configure_data(rep1, input_rep1, rep2, input_rep2)
    macs2.run(prefix)
    file_cond1 = output_folder + prefix + "_c3.0_cond1.bed"
    file_cond2 = output_folder + prefix + "_c3.0_cond2.bed"
    file_commn = output_folder + prefix + "_c3.0_common.bed"
    return file_cond1, file_cond2, file_commn


def run_chipdiff(rep1, rep2, tool_path, outdir, chr_description_fname, prefix):
    chipdiff = ChipDiff(tool_path)
    chipdiff.configure_run_params(chr_description_fname)
    chipdiff.configure_data(rep1, rep2)
    chipdiff.run(prefix)

    sh("mv {0}.bin {1}".format(prefix, outdir))
    sh("mv {0}.hmm {1}".format(prefix, outdir))
    sh("mv {0}.region {1}".format(prefix, outdir))
    sh("mv config.txt {1}".format(prefix, outdir))
    return outdir + prefix + ".region"


def run_zinbra_analyze(ref, rep1, rep2, outfilename, zibra_path, only=None, fdr=0.001):
    zinbra = Zinbra(zibra_path)
    zinbra.configure_run_params(fdr, only=only)
    zinbra.configure_data(ref, rep1, rep2)
    zinbra.run(bed=outfilename)


def run_zinbra_compare(ref, rep1_1, rep1_2, rep2_1, rep2_2, outfname, path, only=None, fdr=0.01):
    zinbra = Zinbra(path)
    zinbra.configure_run_params(fdr, only=only)
    zinbra.configure_data(ref, rep1_1, rep1_2, rep2_1, rep2_2)
    zinbra.run(True, outfname)


# TODO Make MAnorm works
# def run_manorm(cond1_rep1, cond1_rep2,
#                cond2_rep1, cond2_rep2,
#                ctrl1_rep1, ctrl1_rep2,
#                ctrl2_rep1, ctrl2_rep2,
#                manorm_path, macs2_path, outdir):
#     # pooling
#     rep_condition1 = outdir + "/pooled_replicates_vehicle.bed"
#     inp_condition1 = outdir + "/pooled_input_vehicle.bed"
#     make_pooling(cond1_rep1, cond1_rep2, rep_condition1)
#     make_pooling(ctrl1_rep1, ctrl1_rep2, inp_condition1)
#
#     rep_condition2 = outdir + "/pooled_replicates_e2.bed"
#     inp_condition2 = outdir + "/pooled_input_e2.bed"
#     make_pooling(cond2_rep1, cond2_rep2, rep_condition2)
#     make_pooling(ctrl2_rep1, ctrl2_rep2, inp_condition2)
#
#     macs2 = MACS2(macs2_path)
#     summits1, d1 = macs2.callpeaks(rep_condition1, inp_condition1, "manorm_cond1", 120, outdir, needB=False)
#     summits2, d2 = macs2.callpeaks(rep_condition2, inp_condition2, "manorm_cond2", 120, outdir, needB=False)
#
#     # extension = "manorm"
#     # cond_cols = [4, 5, 6]
#     # ctrl_cols = [4, 5]
#     # cond1 = rmcols_reformat(cond1, extension, cond_cols)
#     # cond2 = rmcols_reformat(cond2, extension, cond_cols)
#     # control1 = rmcols_reformat(control1, extension, ctrl_cols)
#     # control2 = rmcols_reformat(control2, extension, ctrl_cols)
#
#     manorm = MAnorm(manorm_path)
#     manorm.configure_run_params(outdir, d1, d2)
#     # manorm.configure_run_params(outdir, 13869843, 14406753)
#     manorm.configure_data(summits1, summits2,
#                           cond1_rep1, cond1_rep2,
#                           cond2_rep1, cond2_rep2)
#     manorm.run()


def run_sicer(cond1, control1, cond2, control2, sicer_path, outdir, windowsize=200, gap=200,
              fdr1=0.01, fdr2=0.01):
    sicer = SICER(sicer_path)
    sicer.configure_data(cond1, control1, cond2, control2)
    sicer.configure_run_params(outdir, windowsize, gap, fdr1, fdr2)
    sicer.run()
