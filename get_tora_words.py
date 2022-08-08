import re
import glob

import pandas as pd

tora_path = r"tanach/all_tora.txt"
nach_path = r"tanach/nach.txt"
tanach_path = r"tanach/all_tanach.txt"
PUNCT = "\u05B0-\u05BD\u05C1-\u05C7"
ACCENTS = "\u0591-\u05AF\u05BD\u05BF-\u05C0\u05C3"
HEBREW_LETTERS = "\u05D0-\u05EA\u05BE"
SPECIAL = "\u05C4-\u05C6"
MAQAF = "\u05BE"
lf = "\u000A"
cr = "\u0020"
hiphen = "\u002D"
ALL = "[" + HEBREW_LETTERS + PUNCT + ACCENTS + "]+"
VERSES_PAT = "(\d+)\s*\u05C3\s*(\d+)"


def get_tora_words():
    fnames = glob.glob(r"tanach\*.txt")
    dfs = []
    for path in fnames:
        txt = open(path, encoding="utf8").read()
        new_txt = re.sub(VERSES_PAT, r"\1_\2", txt)

        full_ts = pd.Series(re.split("[\s\u05BE]+", new_txt))
        words_mask = full_ts.str.match(ALL + "$")
        verses_mask = full_ts.str.match('\d+_\d+$')
        full_ts = full_ts[words_mask | verses_mask].reset_index(drop=True)
        words_without_accents_ts = full_ts.str.replace("[" + ACCENTS + "]", "", regex=True)
        only_words_ts = full_ts.str.replace("[" + ACCENTS + PUNCT + "]", "", regex=True)
        only_accents_ts = full_ts.str.replace("[" + PUNCT + HEBREW_LETTERS + "\d" + "_" + "]", "", regex=True)
        verses_df = full_ts.str.extract("(\d+)_(\d+)")
        #verses_ts = verses_ts.apply(lambda x: x.split("_")[0].zfill(3)+"_"+x.split("_")[1].zfill(3))
        mask = verses_df.isnull().all(axis=1)


        df = pd.concat([full_ts, words_without_accents_ts, only_words_ts, only_accents_ts, verses_df.ffill().astype(int)], axis=1)
        df.columns = ["full", "without_accents", "only_words", "only_accents", "pasuk","perek"]
        df["book"] = path[7:-4]
        dfs.append(df.loc[mask, :].reset_index(drop=True))
    return pd.concat(dfs, axis=0)

    #
    # mask = words_mask & verses_mask
    # full_ts = full_ts[mask]
    # without_accents_ts =
    # m = ''.join(f.readlines())
    # m = re.sub(MAQAF, " ", m)
    # m = re.sub(VERSES_PAT, " ", m)
    #
    # pat_punct_accents = "[" + HEBREW_LETTERS + PUNCT \
    #                     + ACCENTS + "]+"
    #
    # q = re.findall(pat_punct_accents, m, re.UNICODE)
    # # br = ''.join(q)
    # # br = re.sub(r'\u0020[\u05D0-\u05EA]\u0020', ' ', br)
    # # br = re.sub(r'[\u000A\u0020\u002D]+', ' ', br).rstrip().lstrip()
    # return pd.Series(q)


def find_seq(path):
    f = open(path)
    m = ''.join(f.readlines())
    q = re.findall(r'[\u05D0-\u05EA]', m, re.UNICODE)
    br = ''.join(q)
    br = br.replace(r'\u05DD', r'\u05DE')
    br = br.replace(r'\u05DA', r'\u05DB')
    br = br.replace(r'\u05DF', r'\u05E0')
    br = br.replace(r'\u05E3', r'\u05E4')
    br = br.replace(r'\u05E5', r'\u05E6')
    matcher = re.compile(r'(.{1,100}?)\1\1\1', re.UNICODE)

    end = 0
    q = matcher.search(br, end)
    while q != None:
        q.group(0)
        end = q.end()
        start = q.start()

        print(br[start - 5:end + 50])
        q = matcher.search(br, start + 1)


if __name__ == "__main__":
    get_tora_words()
