from util import *


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

    def bed_to_bg(self, bedfile, bgfile):
        with open(bgfile, 'w') as outfile:
            with open(bedfile) as infile:
                for line in infile:
                    if line.startswith('track'):
                        outfile.write(line)
                    else:
                        fields = line.strip().split()
                        bedgraph = [fields[0], fields[1], fields[2], fields[4]]
                        print >> outfile, '\t'.join(bedgraph)

    def convert_to_bedGraph(self, file):
        name = str.split(file, ".bed.gz")[0]

        if not os.path.exists(name + ".bedGraph"):

            # unzip if it's necessary
            if not os.path.exists(name + ".bed"):
                run_in_shell("gunzip -c {0} > {1}".format(file, name + ".bed"))

            self.bed_to_bg(name + ".bed", name + ".bedGraph")

        return name + ".bedGraph"

    def run_bdgdiff(self, prefix):

        if len(self.conditions) != 2 and len(self.controls) != 2:
            raise Error("Controls and conditions has not been set")

        cond1 = self.convert_to_bedGraph(self.conditions[0])
        cond2 = self.convert_to_bedGraph(self.conditions[1])
        ctrl1 = self.convert_to_bedGraph(self.controls[0])
        ctrl2 = self.convert_to_bedGraph(self.controls[1])

        runstring = "{0}/macs2 bdgdiff" \
                    " --t1 {1}" \
                    " --t2 {2}" \
                    " --c1 {3}" \
                    " --c2 {4}" \
                    " --outdir {5}" \
                    " --o-prefix {6}".format(self.where_macs2,
                                             cond1, cond2, ctrl1, ctrl2, self.outdir, prefix)

        run_in_shell(runstring)
