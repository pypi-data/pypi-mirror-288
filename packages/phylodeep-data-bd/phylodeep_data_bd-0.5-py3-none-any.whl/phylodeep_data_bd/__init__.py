import os

import pandas as pd

TARGET_NAMES = ["R_naught", "Infectious_period", 'sampling_proba', 'tree_size']

PREDICTED_NAMES = ["R_naught", "Infectious_period"]


CNN_FULL_TREE = 'CNN_FULL_TREE'
FFNN_SUMSTATS = 'FFNN_SUMSTATS'

LARGE = 'LARGE' # 200 <= #tips <= 500
SMALL = 'SMALL' # 50 <= #tips < 200

ALLOWED_TREE_SIZES = (SMALL, LARGE)
ALLOWED_ENCODINGS = (CNN_FULL_TREE, FFNN_SUMSTATS)



PREFIX = os.path.abspath(os.path.dirname(__file__))


def get_ci_tables(encoding, tree_size, **kwargs):
    """
    Loads the tables required for CI computation (for approximated parametric bootstrap)

    :param encoding: str, one of ALLOWED_ENCODINGS
    :param tree_size: str, the ALLOWED_TREE_SIZES

    :return: two pd.DataFrame, containing values for CI computation: predicted and target tables
    """
    predicted_path, target_path = get_ci_table_paths(tree_size, encoding)
    return (pd.read_csv(predicted_path, compression='xz', header=None, names=PREDICTED_NAMES),
            pd.read_csv(target_path, compression='xz', header=None, names=TARGET_NAMES))


def get_ci_table_paths(encoding, tree_size, **kwargs):
    """
    Returns the paths to the tables required for CI computation (for approximated parametric bootstrap)

    :param encoding: str, one of ALLOWED_ENCODINGS
    :param tree_size: str, the ALLOWED_TREE_SIZES

    :return: tuple containing the paths to the tables containing values for CI computation: predicted and target
    """
    if tree_size not in ALLOWED_TREE_SIZES:
        raise ValueError('Tree size must be one of: {}'.format(', '.join(ALLOWED_TREE_SIZES)))
    if encoding not in ALLOWED_ENCODINGS:
        raise ValueError('Encoding must be one of: {}'.format(', '.join(ALLOWED_ENCODINGS)))
    tree_size = tree_size.lower()
    return (os.path.join(PREFIX, tree_size, '{}.csv.xz'.format(encoding)),
            os.path.join(PREFIX, tree_size, 'target.csv.xz'))


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
                        help="input tree size",
                        type=str, required=True, choices=ALLOWED_TREE_SIZES, default=LARGE)

    parser.add_argument('-e', '--encoding', help="input tree encoding",
                        type=str, required=True, choices=ALLOWED_ENCODINGS,
                        default=CNN_FULL_TREE)

    params = parser.parse_args()

    print(get_ci_table_paths(**vars(params)))


if '__main__' == __name__:
    main()
