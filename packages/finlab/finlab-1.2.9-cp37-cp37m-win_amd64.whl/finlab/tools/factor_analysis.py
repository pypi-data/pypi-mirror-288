import pandas as pd
from finlab import data
from finlab.tools.event_study import create_factor_data
from tqdm import tqdm
from finlab.dataframe import FinlabDataFrame


def ic(factor, adj_close, rank=False, days=[10, 20, 60, 120]):

    if isinstance(factor, pd.DataFrame):
        factor = {'factor': factor}

    for fname, f in factor.items():
        factor[fname] = FinlabDataFrame(f).index_str_to_date()

    ics = {}

    total = len(days) * len(factor)
    with tqdm(total=total, desc="Processing") as pbar:
        for d in days:
            ret = adj_close.shift(-d-1) / adj_close.shift(-1) - 1

            for fname, f in factor.items():
                inter_col = f.columns.intersection(adj_close.columns)
                ret_resahped = ret.reindex(f.index, method='ffill')
                if not rank:
                    ic = f[inter_col].apply(lambda s: s.corr(ret_resahped.loc[s.name]), axis=1)
                else:
                    ic = f[inter_col].rank(axis=1, pct=True).apply(lambda s: s.corr(ret_resahped.loc[s.name]), axis=1)
                ics[f"{fname}_{d}"] = ic
                pbar.update(1)

    return pd.concat(ics, axis=1)
