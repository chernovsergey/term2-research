from src.auxilary.parseconfigs import *
from src.tools.running import *


class DiffRegionsExtractor:
    files_to_benchmark = {}

    def __init__(self, dataconfig, toolconfig):
        self.dataconf = dataconfig
        self.toolconf = toolconfig

        self.ref, \
        self.rep1, self.inp1, \
        self.rep2, self.inp2 = load_data_config(load_yaml(dataconfig))

        for k, v in load_yaml(toolconfig).iteritems():
            setattr(self, k, v)

        # pooling
        dir = get_dirname(self.rep1[0])

        self.pool_condn1 = dir + "/pooled_replicates_cond1.bed"
        self.pool_input1 = dir + "/pooled_input_cond1.bed"
        make_pooling(self.rep1[0], self.rep1[1], self.pool_condn1)
        make_pooling(self.inp1[0], self.inp1[1], self.pool_input1)

        self.pool_condn2 = dir + "/pooled_replicates_cond2.bed"
        self.pool_input2 = dir + "/pooled_input_cond2.bed"
        make_pooling(self.rep2[0], self.rep2[1], self.pool_condn2)
        make_pooling(self.inp2[0], self.inp2[1], self.pool_input2)

        # TODO call peaks here for tools required predefined regions

    def __extract_chipdiff(self):
        outdir = self.chipdiff['outdir']
        chromosomes = self.chipdiff['chromosomes']
        path = self.chipdiff['path']
        projname = self.chipdiff['projname']

        chipdiff_outfiles = run_chipdiff(bed_to_tag(self.pool_condn1),
                                         bed_to_tag(self.pool_condn2),
                                         path,
                                         outdir,
                                         chromosomes,
                                         projname)
        return chipdiff_outfiles

    def __extract_macs2(self):
        outdir = self.macs2['outdir']
        path = self.macs2['path']
        projname = self.macs2['projname']

        outfile = run_macs2(self.pool_condn1, self.pool_condn2,
                            self.pool_input1, self.pool_input2, path, outdir, projname)
        return outfile

    def __extract_zinbra(self):
        output = self.zinbra['outdir']
        path = self.zinbra['path']
        outfile = output + "/{0}.bed".format(self.zinbra['projname'])
        only = self.zinbra['only_chr']

        run_zinbra_compare(ref=self.ref,
                           rep1_1=self.rep1[0], rep1_2=self.rep1[1],
                           rep2_1=self.rep2[0], rep2_2=self.rep2[1],
                           outfname=outfile, path=path, only=only)
        return outfile

    def __extract_sicer(self):
        outdir = self.sicer['outdir']
        path = self.sicer['path']
        outfile = run_sicer(self.pool_condn1, self.pool_input1,
                            self.pool_condn2, self.pool_input2,
                            path, outdir)
        return outfile

    def __extract_manorm(self):
        manorm_outdir = self.manorm['outdir']
        manorm_path = self.manorm['path']

        if hasattr(self, "macs2"):
            macs2_path = self.macs2['path']
            peakcaller = MACS2(macs2_path)
            peaks1, d1 = peakcaller.callpeaks(self.pool_condn1, self.pool_input1, "cond1", 120,
                                              manorm_outdir,
                                              needB=False)
            peaks2, d2 = peakcaller.callpeaks(self.pool_condn2, self.pool_input2, "cond2", 120,
                                              manorm_outdir,
                                              needB=False)
        else:
            raise Error("MACS2 configuration not found")

        extension = "manorm"
        peak_cols = [4, 5, 6]
        read_cols = [4, 5]
        cond1 = rmcols_reformat(self.pool_condn1, extension, peak_cols)
        cond2 = rmcols_reformat(self.pool_condn2, extension, peak_cols)
        peaks1 = rmcols_reformat(peaks1, extension, read_cols)
        peaks2 = rmcols_reformat(peaks2, extension, read_cols)

        outfile = run_manorm(peaks1, peaks2, cond1, cond2, d1, d2, manorm_path, manorm_outdir)
        return outfile

    def get_dr_extractors(self):
        methods = [method for method in dir(self) if callable(getattr(self, method))]
        methods = list(
            filter(lambda x: str.startswith(x, "_DiffRegionsExtractor__extract"), methods))
        return methods

    def extract(self):
        dr_extractors = self.get_dr_extractors()
        for extractor in dr_extractors:
            name = str.split(extractor, "_")[-1]
            method_ref = getattr(self, extractor)
            if hasattr(self, name):
                output = method_ref()
                self.files_to_benchmark[name] = output

        return self.files_to_benchmark
