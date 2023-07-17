import glob
import os

import itasca as it
import pandas as pd

DIR_DOMINIOS = os.path.join(os.path.join(os.getcwd(), 'input'), 'DOMINIOS')
DIR_CELDAS = 'bbdd_celdas.csv'


def run_cross_datasets() -> None:
    # Delete previous states
    it.command("""
    model new
    model large-strain off
    model precision 9
    """)
    
    df = pd.read_csv(DIR_CELDAS)
    
    geom_dict = {}
    for file in glob.glob(os.path.join(DIR_DOMINIOS, "*.dxf")):
        name = os.path.basename(file.split('.dxf')[0])
        it.command(f"geometry import '{file}' set '{name}'")
        geom_dict[name] = name
    
    for index, row in df.iterrows():
        it.command(f"data scalar create {row.x_i} {row.y_i} {row.z_i} group 'start'")
        it.command(f"data scalar create {row.x_f} {row.y_f} {row.z_f} group 'end'")
    
    for key, value in geom_dict.items():
        it.command(f"""
        data scalar group '{value}' slot 'domain' ... 
        range geometry-space '{value}' count odd direction 0 0 1
        """)
    
    it.command("program call 'run_get_scalar_groups.dat'")
    



if __name__ == '__main__':
    # Delete all previous states
    it.command("""
    python-reset-state false
    """)
    
    run_cross_datasets()