from src.dataprocessing.pipeline import Pipeline
from src.dataprocessing.preprocessing import *


def main():
    p = Pipeline("config/dataConfig.yaml", "config/toolConfig.yaml")
    p.start()

    # base_path = "/home/denovo/AU/Research/"
    # data_path = base_path + "Data/"
    # tools_path = base_path + "Tools/"
    # bedfiles = data_path + "bed/"
    # tools_output_path = data_path + "tools_output/"
    #
    # # Data settings
    # reference = data_path + "hg19.2bit"
    # foxa1 = bedfiles + "FOXA1/chr22/"
    #
    # rep1_vh = foxa1 + "GSM1534736_FOXA1_ChIP-seq_Vehicle_rep1_chr22.bed"
    # rep2_vh = foxa1 + "GSM1534737_FOXA1_ChIP-seq_Vehicle_rep2_chr22.bed"
    # input_vh_rep1 = foxa1 + "GSM1534712_Input_ChIP-seq_Vehicle_rep1_chr22.bed"
    # input_vh_rep2 = foxa1 + "GSM1534713_Input_ChIP-seq_Vehicle_rep2_chr22.bed"
    #
    # rep1_e2 = foxa1 + "GSM1534738_FOXA1_ChIP-seq_E2_rep1_chr22.bed"
    # rep2_e2 = foxa1 + "GSM1534739_FOXA1_ChIP-seq_E2_rep2_chr22.bed"
    # input_e2_rep1 = foxa1 + "GSM1534714_Input_ChIP-seq_E2_rep1_chr22.bed"
    # input_e2_rep2 = foxa1 + "GSM1534715_Input_ChIP-seq_E2_rep2_chr22.bed"
    #
    # # # pooling
    # rep_vh = foxa1 + "pooled_replicates_cond1.bed"
    # inp_vh = foxa1 + "pooled_input_cond1.bed"
    # make_pooling(rep1_vh, rep2_vh, rep_vh)
    # make_pooling(input_vh_rep1, input_vh_rep2, inp_vh)
    #
    # rep_e2 = foxa1 + "pooled_replicates_cond2.bed"
    # inp_e2 = foxa1 + "pooled_input_cond2.bed"
    # make_pooling(rep1_e2, rep2_e2, rep_e2)
    # make_pooling(input_e2_rep1, input_e2_rep2, inp_e2)
    #
    # chipdif_outdir = tools_output_path + "chipdiff/"
    # chromosomes = bedfiles + "chrom_descr.txt"
    # chipdiff_path = tools_path + "chipdiff"
    # chipdiff_outfiles = run_chipdiff(bed_to_tag(rep_e2), bed_to_tag(rep_vh),
    #                                  chipdiff_path, chipdif_outdir, chromosomes, "diff_e2_vh")
    # print chipdiff_outfiles
    #
    # macs2_outdir = tools_output_path + "macs2/"
    # macs2_path = "/home/denovo/miniconda/bin"
    # macs2_outfiles = run_macs2(rep_e2, rep_vh, inp_e2, inp_vh, macs2_path, macs2_outdir,
    #                            "diff_e2_vh")
    # print macs2_outfiles
    #
    # zinbra_output = tools_output_path + "zinbra"
    # zinbra_path = tools_path + "zinbra/"
    # zinbra_outfiles = zinbra_output + "cmp_vh_e2.bed"
    # run_zinbra_compare(ref=reference,
    #                    rep1_1=rep1_vh, rep2_1=rep1_e2, rep1_2=rep2_vh, rep2_2=rep2_e2,
    #                    outfname=zinbra_outfiles, path=zinbra_path, only="chr22")
    # print zinbra_outfiles


if __name__ == '__main__':
    logging.basicConfig(filename='runlog.log', format='%(asctime)s %(message)s %(levelname)s',
                        level=logging.INFO)
    logging.getLogger().addHandler(logging.StreamHandler())
    logging.info('Started')
    main()
    logging.info('Finished')
