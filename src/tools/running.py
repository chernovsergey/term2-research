import re
from os import listdir
from os.path import isfile, join

from src.tools.chipdiff import *
from src.tools.macs2 import *
from src.tools.manorm import *
from src.tools.sicer import *
from src.tools.zinbra import *


def run_macs2(rep1, rep2, input_rep1, input_rep2, macs2_path, output_folder, prefix):
    macs2 = MACS2(macs2_path)
    macs2.configure_run_params(output_folder)
    macs2.configure_data(rep1, input_rep1, rep2, input_rep2)
    macs2.run(prefix)
    output = output_folder + "/" + prefix + "_c3.0_common.bed"
    return output


def run_chipdiff(rep1, rep2, tool_path, outdir, chr_description_fname, prefix):
    chipdiff = ChipDiff(tool_path)
    chipdiff.configure_run_params(chr_description_fname)
    chipdiff.configure_data(rep1, rep2)
    chipdiff.run(prefix)

    sh("mv {0}.bin {1}".format(prefix, outdir))
    sh("mv {0}.hmm {1}".format(prefix, outdir))
    sh("mv {0}.region {1}".format(prefix, outdir))
    sh("mv config.txt {1}".format(prefix, outdir))
    return outdir + "/" + prefix + ".region"


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
def run_manorm(peaksA, peaksB, cond1, cond2, d1, d2, manorm_path, outdir):
    manorm = MAnorm(manorm_path)
    manorm.configure_run_params(outdir, d1, d2)
    manorm.configure_data(peaksA, peaksB, cond1, cond2)
    manorm.run()
    # TODO return file


def run_sicer(cond1, control1, cond2, control2, sicer_path, outdir, windowsize=200, gap=200,
              fdr1=0.01, fdr2=0.01):
    sicer = SICER(sicer_path)
    sicer.configure_data(cond1, control1, cond2, control2)
    sicer.configure_run_params(outdir, windowsize, gap, fdr1, fdr2)
    sicer.run()

    outfile = [f for f in listdir(outdir) if isfile(join(outdir, f)) and f.endswith("summary")]
    r = re.compile('.*-W[0-9]*-G[0-9]*-summary')
    outfile = list(filter(r.match, outfile))
    assert len(outfile) == 1
    return outdir + "/" + outfile[0]
