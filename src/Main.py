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

    rep1_vh = foxa1 + "GSM1534736_FOXA1_ChIP-seq_Vehicle_rep1.bed.gz"
    rep2_vh = foxa1 + "GSM1534737_FOXA1_ChIP-seq_Vehicle_rep2.bed.gz"
    input_vh_rep1 = foxa1 + "GSM1534712_Input_ChIP-seq_Vehicle_rep1.bed.gz"
    input_vh_rep2 = foxa1 + "GSM1534713_Input_ChIP-seq_Vehicle_rep2.bed.gz"

    rep1_e2 = foxa1 + "GSM1534738_FOXA1_ChIP-seq_E2_rep1.bed.gz"
    rep2_e2 = foxa1 + "GSM1534739_FOXA1_ChIP-seq_E2_rep2.bed.gz"
    input_e2_rep1 = foxa1 + "GSM1534714_Input_ChIP-seq_E2_rep1.bed.gz"
    input_e2_rep2 = foxa1 + "GSM1534715_Input_ChIP-seq_E2_rep2.bed.gz"

    # ZINBRA - ANALYZE
    zinbra_output = tools_output_path + "zinbra/"
    zinbra_e2 = zinbra_output + "e2.bed"
    zinbra_vh = zinbra_output + "vh.bed"
    zinbra_path = tools_path + "zinbra/"
    run_zinbra_analyze(reference, rep1_e2, rep2_e2, zinbra_e2, zinbra_path, only="chr1")
    run_zinbra_analyze(reference, rep1_vh, rep2_vh, zinbra_vh, zinbra_path, only="chr1")

    # ZINBRA - COMPARE
    zinbra_cmp = zinbra_output + "cmp_vh_e2.bed"
    run_zinbra_compare(reference, rep1_e2, rep2_e2, rep1_vh, rep2_vh, zinbra_cmp, zinbra_path,
                       only="chr1")

    # # CHIPDIFF
    chipdif_output = tools_output_path + "chipdiff/"
    chromosomes = bedfiles + "chrom_descr.txt"
    chipdiff_path = tools_path + "chipdiff"
    chdiff_e2 = run_chipdiff(rep1_e2, rep2_e2, chipdiff_path, chipdif_output, chromosomes, "e2")
    chdiff_vh = run_chipdiff(rep1_vh, rep2_vh, chipdiff_path, chipdif_output, chromosomes, "vh")
    print chdiff_e2
    print chdiff_vh

    # MACS2
    macs2_output = tools_output_path + "macs2/"
    macs2_e2 = run_macs2(rep1_e2, rep2_e2, input_e2_rep1, input_e2_rep2, macs2_output, "e2")
    macs2_vh = run_macs2(rep1_vh, rep2_vh, input_vh_rep1, input_vh_rep2, macs2_output, "vh")


if __name__ == '__main__':
    main()
