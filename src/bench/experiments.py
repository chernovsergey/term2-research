import seaborn as sns
import matplotlib.pyplot as plt
import pandas
import numpy as np


def make_plots(out_e2, out_vehicle):
    # load peaks
    header = ['chr', 'start', 'end', 'strand']
    df_vh = pandas.read_table(out_vehicle)
    df_e2 = pandas.read_table(out_e2)
    df_vh.columns = header
    df_e2.columns = header

    # peak length
    df_vh['peak_len'] = df_vh['end'].astype(np.int) - df_vh['start'].astype(np.int)
    df_e2['peak_len'] = df_e2['end'].astype(np.int) - df_e2['start'].astype(np.int)

    print df_vh['peak_len'].values
    print df_e2['peak_len'].values

    # number of differential peaks
    number_dr_vh = len(df_vh)
    number_dr_e2 = len(df_e2)

    # Plotting
    f, (ax1, ax2, ax3) = plt.subplots(3, 1)
    sns.barplot(["Vehicle", "E2"], [number_dr_vh, number_dr_e2], palette="pastel", ax=ax1)
    ax1.set_ylabel("Number of differential peaks")
    sns.violinplot(data=[df_e2['peak_len'], df_vh['peak_len']], ax=ax2, palette="pastel")
    ax2.set_ylabel("Peak length")
    sns.kdeplot(df_vh['peak_len'].values, ax=ax3)
    sns.kdeplot(df_e2['peak_len'].values, ax=ax3)
    ax3.set_ylabel("Density")
    plt.show()
