import matplotlib.pyplot as plt
import pandas
import seaborn as sns


# TODO
class Benchmark:
    palette = "pastel"
    toolnames = []

    # TODO make input files as map with all required meta-information about tools
    def __init__(self, inputfiles):
        assert inputfiles != None
        self.input = inputfiles

        for i in xrange(len(inputfiles)):
            self.toolnames.append("tool{}".format(i))

    def start(self):
        self.show_number_of_DRs()
        self.show_length_distribution()

    def show_length_distribution(self):
        peak_lens = []
        for file in self.input:
            df = pandas.read_table(file, skiprows=[0])

            peaks = df.ix[:, 2] - df.ix[:, 1]
            peak_lens.append(peaks.values)

        ax = sns.violinplot(data=peak_lens, palette=self.palette)
        ax.set_ylabel("Peak length")
        plt.show()

        ax2 = sns.kdeplot(peak_lens[0], shade=True)
        for i in xrange(1, len(peak_lens)):
            sns.kdeplot(peak_lens[i], ax=ax2, shade=True)
        ax2.set_ylabel("Density")
        plt.show()

    def show_number_of_DRs(self):
        number_drs = []
        for file in self.input:
            df = pandas.read_table(file, skiprows=[0])
            number_drs.append(len(df))

        ax1 = sns.barplot(self.toolnames, number_drs, palette=self.palette)
        ax1.set_ylabel("Number of differential peaks")
        plt.show()
