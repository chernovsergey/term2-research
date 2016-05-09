from src.bench.benchmark import Benchmark
from src.dataprocessing.preprocessing import *


def main():
    # p = DiffRegionsExtractor("config/dataConfig.yaml", "config/toolConfig.yaml")
    # regions = p.extract()

    regions = {
        "chipdiff": "/home/denovo/AU/Research/Data/tools_output/chipdiff/diff_e2_vh.region",
        "macs2": "/home/denovo/AU/Research/Data/tools_output/macs2/diff_e2_vh_c3.0_common.bed",
        "zinbra": "/home/denovo/AU/Research/Data/tools_output/zinbra/diff_e2_vh.bed",
        # "sicer":"/home/denovo/AU/Research/Data/tools_output/sicer/pooled_replicates_cond1-and-pooled_replicates_cond2-W200-G200-summary"
    }

    b = Benchmark(regions)
    b.start()


if __name__ == '__main__':
    logging.basicConfig(filename='runlog.log', format='%(asctime)s %(message)s %(levelname)s',
                        level=logging.INFO)
    logging.getLogger().addHandler(logging.StreamHandler())
    logging.info('Started')
    main()
    logging.info('Finished')
