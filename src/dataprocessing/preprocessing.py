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
