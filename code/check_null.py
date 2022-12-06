### null値の有無を確認する 

import pandas as pd

def check_null(filename):
    data = pd.read_csv(filename)
    print(f'ncol_hasnull - {data.isnull().any().sum()} ({filename})')

check_null('../out/reformed_dummy.csv')
check_null('../out/reformed_notdummy.csv')
check_null('../data/BCCWJ_frequencylist_suw_ver1_0_30.csv')
