from src.auxilary.utility import *


def drop_columns_and_save(filaneme, format, dropcols=None):
    if dropcols is not None:
        name = str.split(filaneme, ".bed")[0]
        if not os.path.exists(name + ".mnr"):
            cols = ",".join(map(str, dropcols))
            run_in_shell(
                "cat  {0}.bed | cut -f{3} --complement > {1}.{2}".format(name, name, format, cols))
        return name + ".mnr"
    else:
        raise Error("wrong column numbers list to be dropped")


def make_pooling(file1, file2, result):
    name1 = str.split(file1, ".bed.gz")[0]
    if str.endswith(file1, ".gz"):
        if not os.path.exists(name1 + ".bed"):
            run_in_shell("gunzip -c {0} > {1}".format(file1, name1 + ".bed"))

    name2 = str.split(file2, ".bed.gz")[0]
    if str.endswith(file2, ".gz"):
        if not os.path.exists(name2 + ".bed"):
            run_in_shell("gunzip -c {0} > {1}".format(file1, name2 + ".bed"))

    if not os.path.exists(result):
        run_in_shell("cat {0} {1} > {2}".format(name1 + ".bed", name2 + ".bed", result))
