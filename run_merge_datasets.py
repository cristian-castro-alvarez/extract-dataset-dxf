from typing import Dict

import pandas as pd

from utils.loader import load_yaml

CONFIG_FILE = 'config.yaml'


def run_merge_datasets(config: Dict) -> pd.DataFrame:

    cells = pd.read_csv(config['dataset']['bbdd_celdas'])
    cells.columns = cells.columns.str.replace(' ', '')

    points_domains_start = pd.read_csv(config['dataset']['points_and_domains_start'])
    points_domains_start.columns = points_domains_start.columns.str.replace(' ', '')

    points_domains_end = pd.read_csv(config['dataset']['points_and_domains_end'])
    points_domains_end.columns = points_domains_end.columns.str.replace(' ', '')

    start_merge = pd.merge(cells, points_domains_start, how='left', left_on=['x_i', 'y_i', 'z_i'], right_on=['x', 'y', 'z'])
    start_merge = start_merge.drop(columns=['x', 'y', 'z'])
    start_merge = start_merge.rename(columns={'domain': 'start_domain'})
    start_merge = start_merge.drop_duplicates()

    end_merge = pd.merge(cells, points_domains_end, how='left', left_on=['x_f', 'y_f', 'z_f'], right_on=['x', 'y', 'z'])
    end_merge = end_merge.drop(columns=['x', 'y', 'z'])
    end_merge = end_merge.rename(columns={'domain': 'end_domain'})
    end_merge = end_merge.drop_duplicates()

    return pd.merge(start_merge, end_merge, how='left', on=cells.columns.values.tolist())


if __name__ == '__main__':
    """
    Creates and process a dataset from a .dxf file
    """
    # Load Config
    config = load_yaml(CONFIG_FILE)
    # Merge
    data = run_merge_datasets(config=config)
    data.to_csv('final_dataset.csv', index=False)