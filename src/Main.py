from src.tools.running import *


def main():
    base_path = "/home/denovo/AU/Research/"
    data_path = base_path + "Data/"
    tools_path = base_path + "Tools/"
    bedfiles = data_path + "bed/"
    tools_output_path = data_path + "tools_output/"

    # Data settings
    reference = data_path + "hg19.2bit"
    foxa1 = bedfiles + "FOXA1/"

    # archived data
    rep1_vh = foxa1 + "GSM1534736_FOXA1_ChIP-seq_Vehicle_rep1.bed.gz"
    rep2_vh = foxa1 + "GSM1534737_FOXA1_ChIP-seq_Vehicle_rep2.bed.gz"
    input_vh_rep1 = foxa1 + "GSM1534712_Input_ChIP-seq_Vehicle_rep1.bed.gz"
    input_vh_rep2 = foxa1 + "GSM1534713_Input_ChIP-seq_Vehicle_rep2.bed.gz"

    rep1_e2 = foxa1 + "GSM1534738_FOXA1_ChIP-seq_E2_rep1.bed.gz"
    rep2_e2 = foxa1 + "GSM1534739_FOXA1_ChIP-seq_E2_rep2.bed.gz"
    input_e2_rep1 = foxa1 + "GSM1534714_Input_ChIP-seq_E2_rep1.bed.gz"
    input_e2_rep2 = foxa1 + "GSM1534715_Input_ChIP-seq_E2_rep2.bed.gz"

    # pooling
    rep_vh = foxa1 + "pooled_replicates_vehicle.bed"
    inp_vh = foxa1 + "pooled_input_vehicle.bed"
    make_pooling(rep1_vh, rep2_vh, rep_vh)
    make_pooling(input_vh_rep1, input_vh_rep2, inp_vh)

    rep_e2 = foxa1 + "pooled_replicates_e2.bed"
    inp_e2 = foxa1 + "pooled_input_e2.bed"
    make_pooling(rep1_e2, rep2_e2, rep_e2)
    make_pooling(input_e2_rep1, input_e2_rep2, inp_e2)

    macs2_outdir = tools_output_path + "macs2/"
    macs2_e2 = run_macs2(rep_e2, rep_vh, inp_e2, inp_vh, macs2_outdir, "diff_e2_vs_vh")

    chipdif_output = tools_output_path + "chipdiff/"
    chromosomes = bedfiles + "chrom_descr.txt"
    chipdiff_path = tools_path + "chipdiff"
    chdiff_e2 = run_chipdiff(rep_e2, rep_vh, chipdiff_path, chipdif_output, chromosomes, "e2_vs_vh")

    zinbra_output = tools_output_path + "zinbra/"
    zinbra_path = tools_path + "zinbra/"
    zinbra_cmp = zinbra_output + "cmp_vh_e2.bed"
    run_zinbra_compare(reference, rep1_1=rep1_vh, rep2_1=rep1_e2, rep1_2=None, rep2_2=None,
                       outfname=zinbra_cmp, path=zinbra_path)

    outdir = tools_output_path + "manorm/"
    manorm_path = tools_path + "manorm"
    outfiles = run_manorm(rep1_vh, rep1_e2, input_vh_rep1, input_e2_rep1,
                          200, 200,  # this params should be extracted from macs2 callpeak
                          manorm_path, outdir)
    print outfiles


if __name__ == '__main__':
    main()
