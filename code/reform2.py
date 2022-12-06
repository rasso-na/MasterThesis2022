# データ整形用２
# カタカナをローマ字に変換
# 音節数やモーラ数などの列を挿入

import pandas as pd
from typing import List, Any
from pykakasi import kakasi
import warnings
import re

warnings.simplefilter('ignore')

# =================================================

kakasi_ = kakasi()
kakasi_.setMode('K', 'a') # K(Katakana) to a(roman)
conv = kakasi_.getConverter()

# =================================================

#「((ウ段＋「ァ/ィ/ェ/ォ」)|(イ段（「イ」を除く）＋「ャ/ュ/ェ/ョ」)|( 「テ/デ」＋「ィ/ュ」)|(大文字カナ))(「ー/ッ/ン」の連続文字列（０文字含む）)」の正規表現
ls = [
    # 二重母音
    '[アカサタナハマヤラワガザダバパ][イウエオ]',
    '[エケセテネヘメレゲゼデベぺ][イウ]',
    '[オコソトノホモヨロヲゴゾドボポ][イウ]',
    # 長音
    '[アカサタナハマヤラワガザダバパ][ア]',
    '[イキシシニヒミリギジヂビピ][イ]',
    '[イキシシニヒミリギジヂビピ][イ]',
    '[ウクスツヌフムユルグズヅブプヴ][ウ]',
    '[エケセテネヘメレゲゼデベぺ][エ]',
    '[オコソトノホモヨロヲゴゾドボポ][オ]',
    # 拗音
    '[ウクスツヌフムユルグズヅブプヴ][ァィェォ]',
    '[イキシチニヒミリギジヂビピ][ャュェョ]',
    '[イキシチニヒミリギジヂビピ][ャュェョ][ウオ]',
    '[テデ][ィュ]',
    '[アイウエオカ-ヂツ-モヤユヨ-ヲヴ]',
]

f = '[ーッン]*'

# ローマ字ver.
# 二重母音: ai，au，ae，ao，ei，eu，oi，ou
# なぜかnauだけできないのでボツ
# ls = [
#     '[kstnhmyrwgzjdbp][a][iueo]',
#     '[kstnhmyrwgzjdbp][e][iu]',
#     '[kstnhmyrwgzjdbp][o][iu]',
#     '[s][h][a][iueo]',
#     '[s][h][e][iu]',
#     '[s][h][o][iu]',
#     '[s][h][a][a]',
#     '[s][h][i][i]',
#     '[s][h][u][u]',
#     '[s][h][e][e]',
#     '[s][h][o][o]',
#     '[s][h][aiueo]',
#     '[c][h][a][iueo]',
#     '[c][h][e][iu]',
#     '[c][h][o][iu]',
#     '[c][h][a][a]',
#     '[c][h][i][i]',
#     '[c][h][u][u]',
#     '[c][h][e][e]',
#     '[c][h][o][o]',
#     '[c][h][aiueo]',
#     '[t][s][a][iueo]',
#     '[t][s][e][iu]',
#     '[t][s][o][iu]',
#     '[t][s][a][a]',
#     '[t][s][i][i]',
#     '[t][s][u][u]',
#     '[t][s][e][e]',
#     '[t][s][o][o]',
#     '[t][s][aiueo]',
#     '[kstnhmyrwgzjdbp][a][a]',
#     '[kstnhmyrwgzjdbp][i][i]',
#     '[kstnhmyrwgzjdbp][u][u]',
#     '[kstnhmyrwgzjdbp][e][e]',
#     '[kstnhmyrwgzjdbp][o][o]',
#     '[kstnhmrgzjdbp][aiueo]',
#     '[yw][auo]',
#     '[kstnhmrgzdbp][y][auo]',
#     '[aiueo]',
# ]

# f = '[n]*'

cond_s = '(?:'
for l in ls:
    if ls.index(l) != len(ls)-1:
        cond_s = cond_s + l + '|'
    else:
        cond_s += l

# cond_s += ')'
cond_s += ')' + f
cond_s = '(' + cond_s + ')'
# print(cond_s)
# cond_s = '(?:'+c1+'|'+c1_1+'|'+c1_2+'|'+c1_3+')'+c5 #(?:)はサブパターンの参照を避けるカッコ
# cond_s = '('+cond_s+')'
re_syllable = re.compile(cond_s)

def syllableWakachi(kana_text):
    return re_syllable.findall(kana_text)

# =================================================

ls = [
    '[ウクスツヌフムユルグズヅブプヴ][ァィェォ]',
    '[イキシチニヒミリギジヂビピ][ャュェョ]',
    '[テデ][ィュ]',
    '[ァ-ヴー]',
]

cond_m = '('
for l in ls:
    if ls.index(l) != len(ls)-1:
        cond_m = cond_m + l + '|'
    else:
        cond_m += l

cond_m += ')'
# print(cond_m)
re_mora = re.compile(cond_m)

def moraWakachi(kana_text):
    return re_mora.findall(kana_text)

# =================================================


class DataFrame:

    def __init__(self, data) -> None:
        self.df = data # データフレーム

    # get

    def getDf(self) -> Any:
        return self.df

    # set

    def setDf(self, df) -> None:
        self.df = df

    # other

    def dropna(self):
        pass


    def reform2(self):
        s_lForm = self.getDf()['lForm']

        roma = []

        syll = []
        mora = []
        len_syll = []
        len_mora = []

        for l in s_lForm:
            roma += [conv.do(l)]
            syll += [syllableWakachi(l)]
            len_syll += [len(syllableWakachi(l))]
            mora += [moraWakachi(l)]
            len_mora += [len(moraWakachi(l))]

        # for l in roma:

        return pd.DataFrame(
            data={'len_syll': len_syll, 'len_mora': len_mora, 'roma': roma, 'syll': syll, 'mora': mora},
            columns=['len_syll', 'len_mora', 'roma', 'syll', 'mora']
        )

def main() -> None:
    data = DataFrame()
    df: Any = pd.read_csv('BCCWJ_frequencylist_suw_ver1_0_30.csv')
    data.setDf(df)
    for col in ['lemma', 'subLemma']:
        data.getDf().pop(col)
    data.setDf(data.getDf().dropna())
    reformed2 = data.reform2()
    reformed2.to_csv('./reformed_.csv')

if __name__ == '__main__':
    main()