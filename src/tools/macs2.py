from abstracttool import AbstractTool
from src.auxilary.utility import *


class MACS2(AbstractTool):
    def __init__(self, path):
        self.where_macs2 = path

    def unarchive_if_necessary(self):
        self.conditions[0] = self.unarchive_gz(self.conditions[0])
        self.controls[0] = self.unarchive_gz(self.controls[0])
        self.conditions[1] = self.unarchive_gz(self.conditions[1])
        self.controls[1] = self.unarchive_gz(self.controls[1])

    def unarchive_gz(self, filename):
        name = filename

        if str.endswith(filename, ".bed.gz"):
            name = str.split(filename, ".bed.gz")[0]
            if not os.path.exists(name + ".bed"):
                run_in_shell("gunzip -c {0} > {1}".format(filename, name + ".bed"))
                return name + ".bed"
        else:
            return name

    def configure_data(self, cond1=None, control1=None, cond2=None, control2=None):
        if cond1 is not None and cond2 is not None:
            self.conditions = [cond1, cond2]
        else:
            raise Error("Wrong condition files")

        if control1 is not None and control2 is not None:
            self.controls = [control1, control2]
        else:
            raise Error("Wrong control files")

    def configure_run_params(self, outdir, cutoff=3, minlen=200, maxgap=100):
        if outdir is not None:
            self.outdir = outdir
        else:
            raise Error("Wrong outdir path")

        self.cutoff = cutoff
        self.minlen = minlen
        self.maxgap = maxgap

    # TODO add parameters in accordance with macs2 callpeak --help
    def callpeaks(self, condition, control, name, extsize, outdir):
        """
        macs2 callpeak -B -t cond1_ChIP.bam -c cond1_Control.bam -n cond1 --nomodel --extsize 120
        """
        runstring = "cd {5}; echo {0}/macs2 callpeak -B" \
                    " -t {1}" \
                    " -c {2}" \
                    " -n {3}" \
                    " --nomodel " \
                    " --extsize {4}".format(self.where_macs2, condition, control, name, extsize,
                                            outdir)
        run_in_shell(runstring)

        t = outdir + name + "_treat_pileup.bdg"
        c = outdir + name + "_control_lambda.bdg"
        d = parse_d(outdir + name + "_peaks.xls")
        return t, c, d

    def run(self, prefix):
        if len(self.conditions) != 2 and len(self.controls) != 2:
            raise Error("Controls and conditions has not been set")

        if prefix is not None:
            if prefix != "":
                self.prefix = prefix
            else:
                raise Error("Passed empty prefix")
        else:
            raise Error("Passed wrong prefix")

        self.unarchive_if_necessary()

        # TODO it's may be useless step
        # self.conditions[0], self.controls[0], d1 = self.callpeaks(self.conditions[0],
        #                                                           self.controls[0], "cond1", 120,
        #                                                           self.outdir)
        # self.conditions[1], self.controls[1], d2 = self.callpeaks(self.conditions[1],
        #                                                           self.controls[1], "cond2", 120,
        #                                                           self.outdir)

        runstring = "{0}/macs2 bdgdiff" \
                    " --t1 {1}" \
                    " --c1 {2}" \
                    " --t2 {3}" \
                    " --c2 {4}" \
                    " --outdir {5}" \
                    " --o-prefix {6}" \
                    " -l {8}" \
                    " -g {9}".format(self.where_macs2,
                                     self.conditions[0], self.controls[0],
                                     self.conditions[1], self.controls[1],
                                     self.outdir, self.prefix, self.cutoff, self.minlen,
                                     self.maxgap)

        run_in_shell(runstring)
