import os

import pandas as pd

TARGET_NAMES = ["R_naught", "Infectious_period", 'sampling_proba', 'tree_size']

PREDICTED_NAMES = ["R_naught", "Infectious_period"]


PREFIX = os.path.abspath(os.path.dirname(__file__))


def get_ci_tables(tree_size, encoding):
    """
    Loads the tables required for CI computation (for approximated parametric bootstrap)

    :param encoding: str, 'FFNN_SUMSTATS' or 'CNN_FULL_TREE'

    :param tree_size: str, 'LARGE' or 'SMALL', corresponding to the size of the tree
        ('SMALL', if 49<#tips<200; 'LARGE', if 199<#tips<501)

    :return: two pd.DataFrame, containing values for CI computation: predicted and target tables
    """
    predicted_path, target_path = get_ci_table_paths(tree_size, encoding)
    return (pd.read_csv(predicted_path, compression='xz', header=None, names=PREDICTED_NAMES),
            pd.read_csv(target_path, compression='xz', header=None, names=TARGET_NAMES))


def get_ci_table_paths(tree_size, encoding):
    """
    Returns the paths to the tables required for CI computation (for approximated parametric bootstrap)

    :param encoding: str, 'FFNN_SUMSTATS' or 'CNN_FULL_TREE'

    :param tree_size: str, 'LARGE' or 'SMALL', corresponding to the size of the tree
        ('SMALL', if 49<#tips<200; 'LARGE', if 199<#tips<501)

    :return: tuple containing the paths to the tables containing values for CI computation: predicted and target
    """
    return (os.path.join(PREFIX, tree_size.lower(), '{}.csv.xz'.format(encoding)),
            os.path.join(PREFIX, tree_size.lower(), 'target.csv.xz'))


def main():
    """
    Entry point, calling :py:func:`phylodeep_data_bd.get_ci_table_paths`  with command-line arguments.
    :return: void
    """
    import argparse

    parser = argparse.ArgumentParser(description="Constructs the paths to the tables required for CI computation"
                                                 " (for approximated parametric bootstrap).",
                                     prog='bd_ci_paths')

    parser.add_argument('-s', '--tree_size',
                        help="input tree size, can be 'LARGE' (200-500 tips) or 'SMALL' (50-199 tips).",
                        type=str, required=True, choices=('LARGE', 'SMALL'), default='LARGE')

    parser.add_argument('-e', '--encoding', help="'FFNN_SUMSTATS' or 'CNN_FULL_TREE'",
                        type=str, required=True, choices=('FFNN_SUMSTATS', 'CNN_FULL_TREE'),
                        default='CNN_FULL_TREE')

    params = parser.parse_args()

    print(get_ci_table_paths(**vars(params)))


if '__main__' == __name__:
    main()
