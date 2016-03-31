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

    # unpack data
    rep1_vh = unpack_gz(foxa1 + "GSM1534736_FOXA1_ChIP-seq_Vehicle_rep1.bed.gz")
    rep2_vh = unpack_gz(foxa1 + "GSM1534737_FOXA1_ChIP-seq_Vehicle_rep2.bed.gz")
    input_vh_rep1 = unpack_gz(foxa1 + "GSM1534712_Input_ChIP-seq_Vehicle_rep1.bed.gz")
    input_vh_rep2 = unpack_gz(foxa1 + "GSM1534713_Input_ChIP-seq_Vehicle_rep2.bed.gz")

    rep1_e2 = unpack_gz(foxa1 + "GSM1534738_FOXA1_ChIP-seq_E2_rep1.bed.gz")
    rep2_e2 = unpack_gz(foxa1 + "GSM1534739_FOXA1_ChIP-seq_E2_rep2.bed.gz")
    input_e2_rep1 = unpack_gz(foxa1 + "GSM1534714_Input_ChIP-seq_E2_rep1.bed.gz")
    input_e2_rep2 = unpack_gz(foxa1 + "GSM1534715_Input_ChIP-seq_E2_rep2.bed.gz")

    # # pooling
    rep_vh = foxa1 + "pooled_replicates_vehicle.bed"
    inp_vh = foxa1 + "pooled_input_vehicle.bed"
    make_pooling(rep1_vh, rep2_vh, rep_vh)
    make_pooling(input_vh_rep1, input_vh_rep2, inp_vh)

    rep_e2 = foxa1 + "pooled_replicates_e2.bed"
    inp_e2 = foxa1 + "pooled_input_e2.bed"
    make_pooling(rep1_e2, rep2_e2, rep_e2)
    make_pooling(input_e2_rep1, input_e2_rep2, inp_e2)

    chipdif_outdir = tools_output_path + "chipdiff/"
    chromosomes = bedfiles + "chrom_descr.txt"
    chipdiff_path = tools_path + "chipdiff"
    chdiff_e2 = run_chipdiff(bed_to_tag(rep_e2), bed_to_tag(rep_vh), chipdiff_path, chipdif_outdir,
                             chromosomes, "e2_vs_vh")

    macs2_outdir = tools_output_path + "macs2/"
    macs2_path = "/home/denovo/miniconda/bin"
    macs2_1 = run_macs2(rep1_e2, rep1_vh, input_e2_rep1, input_vh_rep1, macs2_path, macs2_outdir,
                        "p1_e2_vh")
    macs2_2 = run_macs2(rep2_e2, rep2_vh, input_e2_rep2, input_vh_rep2, macs2_path, macs2_outdir,
                        "p2_e2_vh")
    macs2_e2_vh_cond1 = macs2_outdir + "diff_E2_VH_cond1.bed"
    macs2_e2_vh_cond2 = macs2_outdir + "diff_E2_VH_cond2.bed"
    macs2_e2_vh_commn = macs2_outdir + "diff_E2_VH_common.bed"
    make_pooling(macs2_1[0], macs2_2[0], macs2_e2_vh_cond1)
    make_pooling(macs2_1[1], macs2_2[1], macs2_e2_vh_cond2)
    make_pooling(macs2_1[2], macs2_2[2], macs2_e2_vh_commn)

    zinbra_output = tools_output_path + "zinbra/"
    zinbra_path = tools_path + "zinbra/"
    zinbra_cmp = zinbra_output + "cmp_vh_e2.bed"
    run_zinbra_compare(reference, rep1_1=rep1_vh, rep2_1=rep1_e2, rep1_2=rep2_vh, rep2_2=rep2_e2,
                       outfname=zinbra_cmp, path=zinbra_path, only="chrX")

    outdir = tools_output_path + "manorm"
    manorm_path = tools_path + "manorm"
    outfiles = run_manorm(rep1_vh, rep1_e2, input_vh_rep1, input_e2_rep1, manorm_path, macs2_path,
                          outdir)
    print outfiles


if __name__ == '__main__':
    logging.basicConfig(filename='runlog.log', format='%(asctime)s %(message)s %(levelname)s',
                        level=logging.INFO)
    logging.getLogger().addHandler(logging.StreamHandler())
    logging.info('Started')
    main()
    logging.info('Finished')
