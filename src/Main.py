import pandas
import numpy as np
from Zinbra import *
import seaborn as sns
import matplotlib.pyplot as plt


def main():
    basepath = "~/AU/Research/"
    datafolder = basepath + "Data/"
    toolsfolder = basepath + "Tools/"
    tools_output_folder = datafolder + "tools_output/"
    bedfolder = datafolder + "/bed/"

    # Data settings
    reference = datafolder + "hg19.2bit"

    rep1_vehicle = bedfolder + "FOXA1/GSM1534736_FOXA1_ChIP-seq_Vehicle_rep1.bed.gz"
    rep2_vehicle = bedfolder + "FOXA1/GSM1534737_FOXA1_ChIP-seq_Vehicle_rep2.bed.gz"

    rep1_e2 = bedfolder + "FOXA1/GSM1534738_FOXA1_ChIP-seq_E2_rep1.bed.gz"
    rep2_e2 = bedfolder + "FOXA1/GSM1534739_FOXA1_ChIP-seq_E2_rep2.bed.gz"
    #


    ###
    ### Analysis of Vehicle and E2 data
    ###
    zinbra = Zinbra(toolsfolder + "zinbra/")
    zinbra.set_reference(reference)

    out_vehicle = tools_output_folder + "zinbra/" + "result_vehicle.bed"
    out_e2 = tools_output_folder + "zinbra/" + "result_e2.bed"

    zinbra.add_replicates([rep1_vehicle, rep2_vehicle])
    zinbra.run_analyze(fdr=0.0001, only="chr1", bed=out_vehicle)

    zinbra.add_replicates([rep1_e2, rep2_e2])
    zinbra.run_analyze(fdr=0.0001, only="chr1", bed=out_e2)

    # load peaks
    header = ['chr', 'start', 'end', 'strand']
    df_vh = pandas.read_table(out_vehicle)
    df_e2 = pandas.read_table(out_e2)
    df_vh.columns = header
    df_e2.columns = header

    # peak length
    df_vh['peak_len'] = df_vh['end'].astype(np.int) - df_vh['start'].astype(np.int)
    df_e2['peak_len'] = df_e2['end'].astype(np.int) - df_e2['start'].astype(np.int)

    # number of differential peaks
    number_dr_vh = len(df_vh)
    number_dr_e2 = len(df_e2)

    # Plotting
    f, (ax1, ax2, ax3) = plt.subplots(3, 1)
    sns.barplot(["Vehicle", "E2"], [number_dr_vh, number_dr_e2], palette="pastel", ax=ax1)
    ax1.set_ylabel("Number of differential peaks")
    sns.violinplot(data=[df_e2['peak_len'], df_vh['peak_len']], ax=ax2, palette="pastel")
    ax2.set_ylabel("Peak length")
    sns.kdeplot(df_vh['peak_len'], ax=ax3)
    sns.kdeplot(df_e2['peak_len'], ax=ax3)
    ax3.set_ylabel("Density")
    plt.show()


if __name__ == '__main__':
    main()
