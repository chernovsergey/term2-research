from Utility import *


class MACS2():
    conditions = list()
    controls = list()
    where_macs2 = ""

    def __init__(self, path):
        self.where_macs2 = path

    def configure(self, outdir, cutoff=3, minlen=200, maxgap=100):
        if outdir is not None:
            self.outdir = outdir
        else:
            raise Error("Wrong outdir path")

        self.cutoff = cutoff
        self.minlen = minlen
        self.maxgap = maxgap

    def set_prefix(self, prefix):
        if prefix is not None:
            if prefix != "":
                self.prefix = prefix
        else:
            raise Error("Could not parse prefix")

    def set_conditions(self, cond1, cond2):
        if cond1 is not None and cond2 is not None:
            self.conditions = [cond1, cond2]
        else:
            raise Error("Wrong condition files")

    def set_controls(self, control1, control2):
        if control1 is not None and control2 is not None:
            self.controls = [control1, control2]
        else:
            raise Error("Wrong control files")

    def unarchive_if_necessary(self):
        self.conditions[0] = self.unarchive_gz(self.conditions[0])
        self.controls[0] = self.unarchive_gz(self.controls[0])

        self.conditions[1] = self.unarchive_gz(self.conditions[1])
        self.controls[1] = self.unarchive_gz(self.controls[1])

    def unarchive_gz(self, filename):
        name = str.split(filename, ".bed.gz")[0]
        if not os.path.exists(name + ".bed"):
            run_in_shell("gunzip -c {0} > {1}".format(filename, name + ".bed"))
        return name + ".bed"

    def run_bdgdiff(self, prefix):

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

        runstring = "{0}/macs2 bdgdiff" \
                    " --t1 {1}" \
                    " --t2 {2}" \
                    " --c1 {3}" \
                    " --c2 {4}" \
                    " --outdir {5}" \
                    " --o-prefix {6}" \
                    " --cutoff {7}" \
                    " --min-len {8}" \
                    " --max-gap {9}".format(self.where_macs2,
                                            self.conditions[0], self.conditions[1],
                                            self.controls[0], self.controls[1],
                                            self.outdir, self.prefix, self.cutoff, self.minlen,
                                            self.maxgap)

        run_in_shell(runstring)
