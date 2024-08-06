import re
import time
import hashlib
import pandas as pd
import os
import warnings


def dissect_from_frame(frame, nsample=5):
    def non_alpanumeric(data):
        vals = pd.Series(data).value_counts().sort_values(ascending=True)
        y = dict(zip(vals.index, vals))
        return y

    def val_length(data):
        minl = min(data[data.str.len() > 0].str.len(), default=0)
        maxl = max(data[data.str.len() > 0].str.len(), default=0)
        return {'min': minl, 'max': maxl}

    def not_a_val(data):
        nan = int(data[data.isna()].count())
        # emptystr = int(data[data == ''].count())
        # emptystr = len(data[data == ''])
        emptystr = (data == '').sum()
        return {'nan': nan, 'emptystr': emptystr}

    def top(data, head):
        values = data.value_counts().sort_values(ascending=False)[:head]
        d = dict(zip(values.index, values))
        return d

    strlen = frame.apply(lambda x: val_length(x))
    nnull = frame.apply(lambda x: not_a_val(x))
    nrow = frame.apply(lambda x: len(x))
    nunique = frame.apply(lambda x: len(x[x.str.len() > 0].drop_duplicates().dropna()))
    nvalue = frame.apply(lambda x: len(x[x.str.len() > 0].dropna()))
    freq = frame.apply(lambda x: top(x[x.str.len() > 0], nsample))
    sample = frame.apply(lambda x: str(x[x != ''].value_counts().sort_values(ascending=False)[:nsample].index.tolist()))
    symbols = frame.apply(lambda x: non_alpanumeric(list(re.sub('[a-zA-Z0-9]', '', ''.join(x[x.notna()])))))

    cols = ['strlen', 'nnull', 'nrow', 'nunique', 'nvalue', 'freq', 'symbols']

    result = pd.concat([strlen, nnull, nrow, nunique, nvalue, freq, symbols], axis=1)
    result.columns = cols
    result = result.reset_index().rename(columns={'index': 'column'})
    result['n'] = result.reset_index().index + 1

    return result


def dissect_from_file(file, filetype='csv', sep=';', slicers=[''], nsample=5, skiprows=0, skipfooter=0,
                      encoding='utf-8', names = None):
    if filetype.lower().strip() == 'csv':
        df = pd.read_csv(file, sep=sep, keep_default_na=False, skiprows=skiprows, skipfooter=skipfooter,
                         engine='python', names=names, encoding=encoding, quotechar='"', on_bad_lines='warn', dtype='str')
    filename = os.path.basename(file)

    for slice in slicers:
        df_sliced = df.copy()
        if len(slice) > 0:
            try:
                df_sliced.query(slice, inplace=True)
            except Exception as err:
                msg = f"{type(err).__name__}: Error occurred while slicing. {err}. Skipped slice `{slice}` in file `{filename}`"
                warnings.warn(msg, Warning)
                continue

        print_msg = f"{df_sliced.shape} rows & columns in `{filename}` for slice `{slice}`."
        print(print_msg)

        if df_sliced.shape[0] == 0: continue

        result = dissect_from_frame(df_sliced, nsample)
        result[['filename', 'filetype', 'slice']] = filename, filetype, slice

        file_properties = get_file_property(file)
        result[list(file_properties)] = list(file_properties.values())

        yield result


def get_file_hash(path, hash_type='md5'):
    m = hashlib.new(hash_type)
    with open(path, 'rb') as f:
        m.update(f.read())
        return m.hexdigest()


def get_file_property(path, date_time_format='%Y%m%d'):
    filename = os.path.basename(path)

    timestamp = time.gmtime(os.path.getmtime(path))
    timestamp = time.strftime(date_time_format, timestamp)

    hash = get_file_hash(path)

    size = os.path.getsize(path)

    return {'filename': filename, 'timestamp': timestamp, 'hash': hash, 'size': size}


def concat_dfs(dfs):
    return pd.concat(dfs)
