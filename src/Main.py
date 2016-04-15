from src.bench.benchmark import Benchmark
from src.dataprocessing.dr_extractor import *
from src.dataprocessing.preprocessing import *


def main():
    p = DiffRegionsExtractor("config/dataConfig.yaml", "config/toolConfig.yaml")
    regions = p.extract()

    b = Benchmark(regions)
    b.start()


if __name__ == '__main__':
    logging.basicConfig(filename='runlog.log', format='%(asctime)s %(message)s %(levelname)s',
                        level=logging.INFO)
    logging.getLogger().addHandler(logging.StreamHandler())
    logging.info('Started')
    main()
    logging.info('Finished')
