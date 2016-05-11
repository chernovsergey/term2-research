def main():
    import argparse
    parser = argparse.ArgumentParser()

    parser.add_argument("-t", "--toolconfig",
                        help="YAML file with tool config. See example at github.com/chernovsergey/term2-research")
    parser.add_argument("-d", "--dataconfig",
                        help="YAML file with data config. See example at github.com/chernovsergey/term2-research")

    args = parser.parse_args()

    if args.toolconfig and args.dataconfig:
        print "Configuration file %s will be used as tool config" % args.toolconfig
        print "Configuration file %s will be used as data source" % args.dataconfig

        from src.dataprocessing.dr_extractor import DiffRegionsExtractor
        p = DiffRegionsExtractor(args.dataconfig, args.toolconfig)
        regions = p.extract()

        from src.bench.benchmark import Benchmark
        b = Benchmark(regions)
        b.start()


if __name__ == '__main__':
    import sys
    import os.path

    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

    from src.dataprocessing.preprocessing import *

    logging.basicConfig(filename='runlog.log', format='%(asctime)s %(message)s %(levelname)s',
                        level=logging.INFO)
    logging.getLogger().addHandler(logging.StreamHandler())
    logging.info('Started')
    main()
    logging.info('Finished')
