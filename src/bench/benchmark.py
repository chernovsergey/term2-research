from itertools import *

import matplotlib.pyplot as plt
import numpy as np
import pandas
import seaborn as sns
from intervaltree.intervaltree import IntervalTree

from src.auxilary.venn import *


class Benchmark:
    palette = "pastel"
    toolnames = []
    input = []

    def __init__(self, inputfiles):
        assert inputfiles != None
        assert type(inputfiles) == type(dict())

        for name, outfile in inputfiles.iteritems():
            self.toolnames.append(name)
            self.input.append(outfile)

    def __show_diff_scatter(self):
        intervaltrees_dict = dict()
        min_coord = 1e10
        max_coord = -1

        for idx in xrange(len(self.input)):
            data = pandas.read_table(self.input[idx], skiprows=[0]).ix[:, 1:3]
            itree = IntervalTree()

            curmin = min(data.ix[:, 0])
            if curmin < min_coord:
                min_coord = curmin

            curmax = max(data.ix[:, 1])
            if curmax > max_coord:
                max_coord = curmax

            for line in xrange(len(data)):
                start = data.ix[line, 0]
                end = data.ix[line, 1] + 1
                itree[start:end] = (start, end)
            intervaltrees_dict[self.toolnames[idx]] = itree

        print min_coord, max_coord

        for out1, out2 in combinations(self.toolnames, 2):
            if out1 != out2:
                simm_diff = intervaltrees_dict[out1] ^ intervaltrees_dict[out2]
                tree_size = len(simm_diff)
                x = np.zeros(tree_size)
                s = np.zeros(tree_size)
                items = list(simm_diff.items())
                for i in xrange(tree_size):
                    it = items[i]
                    x[i] = it.begin + (it.end - it.begin) / float(2)
                    s[i] = x[i] ** 0.27

                plt.scatter(x, x, s=s, c='r', alpha=0.3, edgecolors='none')
                plt.ylabel('Genome coordinates')
                plt.xlabel('Genome coordinates')
                plt.title("Coverage difference for tools: " + out1 + " vs " + out2)
                plt.savefig("peaks_covdif_%s_%s" % (out1, out2))

    def __show_venn_diagram(self):

        subsets = list()
        for file_idx in xrange(len(self.input)):
            curset = list()
            df = pandas.read_table(self.input[file_idx], skiprows=[0])
            size = len(df)
            x = df.ix[:, 1:3]
            del df
            for line in xrange(size):
                intervals = xrange(x.ix[line, 0], x.ix[line, 1] + 1)
                for pos in intervals:
                    curset.append(pos)
            subsets.append(set(curset))

        venn4(subsets, self.toolnames)
        plt.show()

    def __show_length_distribution(self):
        peak_lens = []
        for file in self.input:
            df = pandas.read_table(file, skiprows=[0])
            peaks = df.ix[:, 2].values - df.ix[:, 1].values
            peak_lens.append(peaks)

        f, axarr = plt.subplots(len(self.toolnames), sharex=False)
        for i in xrange(len(self.toolnames)):
            sns.violinplot(data=peak_lens[i], palette=self.palette, orient="h", ax=axarr[i])
            axarr[i].set_ylabel(self.toolnames[i])

        f.tight_layout()
        plt.show()

        ax2 = sns.kdeplot(peak_lens[0], label=self.toolnames[0], shade=True)
        for i in xrange(1, len(peak_lens)):
            sns.kdeplot(peak_lens[i], ax=ax2, label=self.toolnames[i], shade=True) \
                .set(xlim=(0, 3000))
        ax2.set_ylabel("Density")
        plt.show()

    def __show_number_of_DRs(self):
        number_drs = []
        for file in self.input:
            df = pandas.read_table(file, skiprows=[0])
            number_drs.append(len(df))

        ax1 = sns.barplot(self.toolnames, number_drs, palette=self.palette)
        ax1.set_ylabel("Number of differential peaks")
        ax1.set(yscale="log")
        plt.savefig("out/peaks_covdiff_venn")

    def get_benchmark_tests(self):
        methods = [method for method in dir(self) if callable(getattr(self, method))]
        methods = list(filter(lambda x: str.startswith(x, "_Benchmark__show"), methods))
        return methods

    def start(self):
        test_methods = self.get_benchmark_tests()
        for test in test_methods:
            method_ref = getattr(self, test)
            method_ref()
