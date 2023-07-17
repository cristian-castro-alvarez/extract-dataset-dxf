from pathlib import Path
from typing import Dict

import ezdxf
import numpy as np
import pandas as pd

from utils.loader import load_yaml

CONFIG_FILE = 'config.yaml'


def run_extract_dataset(config: Dict) -> pd.DataFrame:
    """
    Creates a dataset from layers in a dxf file
    """

    input_file = Path.cwd() / config['input_celdas_dir']

    doc = ezdxf.readfile(input_file)
    model_space = doc.modelspace()

    data = []

    for entity in model_space:
        if entity.dxftype() == 'LINE':
            layer_name = entity.dxf.layer
            layer_rgb = entity.rgb
            x_i = entity.dxf.start[0]
            y_i = entity.dxf.start[1]
            z_i = entity.dxf.start[2]
            x_f = entity.dxf.end[0]
            y_f = entity.dxf.end[1]
            z_f = entity.dxf.end[2]
            data.append([layer_name, layer_rgb, x_i, y_i, z_i, x_f, y_f, z_f])

    columns = ['layer_name', 'layer_rgb', 'x_i', 'y_i', 'z_i', 'x_f', 'y_f', 'z_f']

    return pd.DataFrame(data=data, columns=columns)


def process_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Computes distances and angles
    Assumes that each row of the dataframe has x_i, y_i, z_i, x_f, y_f, z_f
    """
    # Distance
    df['distance'] = np.sqrt((df.x_f-df.x_i)**2+
                             (df.y_f-df.y_i)**2+
                             (df.z_f-df.z_i)**2)
    # Angle w/R to Y-Axis (North)
    df['angle_wr_y'] = np.degrees(np.arctan2((df.x_f-df.x_i),(df.y_f-df.y_i)))

    return df


if __name__ == '__main__':
    """
    Creates and process a dataset from a .dxf file
    """
    # Load Config
    config = load_yaml(CONFIG_FILE)
    # Extract
    data = run_extract_dataset(config=config)
    # Process & Export
    data = process_data(df=data)
    data.to_csv('bbdd_celdas.csv', index=False)