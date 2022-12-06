### データ整形用１

import pandas as pd
import os

import reform2

class Data:
    
    def __init__(self, filename) -> None:
        self.data = pd.read_csv(filename)
    
    def make_dummy(self,col_names):
        for col_name in col_names:
            self.data = pd.get_dummies(self.data, columns=[col_name])  # 指定列のダミーを作成

    def replace(self, col_name, regexps, contents):
        cols = self.data.columns.values
        new_df = pd.DataFrame(columns=cols)
        for i, content in enumerate(contents):
            # regexps[i]に一致する行だけを抽出したデータフレーム
            tmp = self.data[self.data[col_name].str.match(regexps[i], na=False)]
            # tmpの指定列の中身を全てcontents[i]に置き換える
            tmp.loc[tmp[col_name].str.match(regexps[i]), col_name] = content
            new_df = pd.concat([new_df, tmp])  # new_dfに対して縦に連結
        self.data = new_df
        return self.data

    def omit_ex(self, col_name, keep):
        i = self.data.query(f'not {col_name} in {keep}').index
        self.data = self.data.drop(i)

    def omit_null(self):
        self.data = self.data.loc[:, ~self.data.isnull().any()]


path = os.path.dirname(os.path.abspath(__file__))
os.chdir(path)
print(f'ｶﾚﾝﾄﾃﾞｨﾚｸﾄﾘ: {os.getcwd()}')
os.makedirs('../out', exist_ok=True)

obj = Data('../data/BCCWJ_frequencylist_suw_ver1_0_30.csv')
print(obj.data.head())
tmp = reform2.DataFrame(obj.data)
obj.data = pd.concat([obj.data, tmp.reform2()], axis=1)
before = len(obj.data)
print(f'処理前データ総数 - {before}')

obj.replace(
                'wType', 
                ['和', '漢', '外'],
                ['和', '漢', '外']
            )
obj.omit_ex(
                'K_acc', 
                ['A', 'B']
            )
obj.replace(
                'pos', 
                ['^名詞.*','^動詞.*', '^形容詞.*', '^副詞.*'], 
                ['名詞', '動詞', '形容詞', '副詞']
            )
obj.omit_null()

obj.data.to_csv('../out/reformed_original.csv')
obj.make_dummy(['K_acc'])
obj.data.to_csv('../out/reformed_notdummy.csv')
obj.make_dummy(['wType', 'pos', 'len_syll', 'len_mora'])
obj.data.to_csv('../out/reformed_dummy.csv')

after = len(obj.data)
print(f'解析可能データ総数 - {after}')
print(f'削除データ数 - {before-after}')
