from src.auxilary.utility import *


def rmcols_reformat(filaneme, ext, dropcols=None):
    """
     Removes specified columns and save with given extension
    """
    if dropcols is not None:
        name = str.split(filaneme, ".bed")[0]
        if not os.path.exists(name + "." + ext):
            cols = ",".join(map(str, dropcols))
            INFO("Removing columns {0} from {1}".format(cols, name))
            sh("cat {0}.bed | cut -f{3} --complement > {1}.{2}".format(name, name, ext, cols))
        return name + "." + ext
    else:
        raise Error("wrong column numbers list to be dropped")


def make_pooling(file1, file2, result):
    if not os.path.exists(result):
        INFO("Pooling ...")
        sh("cat {0} {1} > {2}".format(file1, file2, result))


def unpack_gz(filename):
    if not str.endswith(filename, ".bed.gz"):
        raise Error("Non .gz file passed")

    name = str.split(filename, ".gz")[0]
    if not os.path.exists(name):
        INFO("Converting {0}.gz to {0} ...".format(name))
        sh("gunzip -c {0} > {1}".format(filename, name))

    return name


def bed_to_tag(library):
    name = str.split(library, ".bed")[0]
    if not os.path.exists(name + ".tag"):
        INFO("Converting {0}.bed to {0}.tag ...".format(name))
        sh("cat  {0}.bed | cut -f3,4,5 --complement > {1}.tag".format(name, name))
    return name + ".tag"
