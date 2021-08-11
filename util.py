import pandas as pd
import numpy as np


def fill_empty_month(dict_df):
    months = ["%.2d" % i for i in range(1, 13)]
    empty = ['empty', 'empty']

    for key, value in dict_df.items():
        if len(dict_df[key]) < 12:
            for x in range(12):
                try:
                    if dict_df[key][x][0][3:5] != months[x]:
                        dict_df[key].insert(x, empty)
                except:
                    dict_df[key].insert(x, empty)
    return dict_df


def get_min_temperature_per_month(df):
    used_only = df[['nama_stasiun', 'wmoid', 'tanggal', 'suhu_minimum']]
    used_only = used_only.dropna()
    replaced_to_nan = used_only.replace([9999, 8888], np.nan)
    replaced_to_nan.suhu_minimum.fillna(replaced_to_nan.suhu_minimum.mean(), inplace=True)

    daftar_wmoid_stasiun = replaced_to_nan.wmoid.unique()

    suhu_per_stasiun = []
    for x in daftar_wmoid_stasiun:
        suhu_per_stasiun.append(replaced_to_nan[replaced_to_nan.wmoid == x])

    months = ["%.2d" % i for i in range(1, 13)]
    suhu_min_per_stasiun = {}
    for x in range(len(daftar_wmoid_stasiun)):
        tanggal_suhu = suhu_per_stasiun[x][['tanggal', 'suhu_minimum']]
        suhu_per_bulan = [tanggal_suhu[tanggal_suhu.tanggal.str[3:5] == x] for x in months]
        suhu_min_per_stasiun[daftar_wmoid_stasiun[x]] = suhu_per_bulan

    final = {}
    temp = []
    for stasiun in daftar_wmoid_stasiun:
        try:
            final[replaced_to_nan[replaced_to_nan.wmoid == stasiun].iloc[0].nama_stasiun] = []
            for bulan in suhu_min_per_stasiun[stasiun]:
                try:
                    temp.append([bulan[bulan.suhu_minimum == bulan.suhu_minimum.min()].iloc[0].tanggal,
                                 bulan[bulan.suhu_minimum == bulan.suhu_minimum.min()].iloc[0].suhu_minimum])
                except:
                    pass
        except:
            pass
        try:
            final[replaced_to_nan[replaced_to_nan.wmoid == stasiun].iloc[0].nama_stasiun] = temp
            temp = []
        except:
            pass

    return fill_empty_month(final)


def get_max_temperature_per_month(df):
    used_only = df[['nama_stasiun', 'wmoid', 'tanggal', 'suhu_maksimum']]
    used_only = used_only.dropna()
    replaced_to_nan = used_only.replace([9999, 8888], np.nan)
    replaced_to_nan.suhu_maksimum.fillna(replaced_to_nan.suhu_maksimum.mean(), inplace=True)

    daftar_wmoid_stasiun = replaced_to_nan.wmoid.unique()

    suhu_per_stasiun = []
    for x in daftar_wmoid_stasiun:
        suhu_per_stasiun.append(replaced_to_nan[replaced_to_nan.wmoid == x])

    months = ["%.2d" % i for i in range(1, 13)]
    suhu_max_per_stasiun = {}
    for x in range(len(daftar_wmoid_stasiun)):
        tanggal_suhu = suhu_per_stasiun[x][['tanggal', 'suhu_maksimum']]
        suhu_per_bulan = [tanggal_suhu[tanggal_suhu.tanggal.str[3:5] == x] for x in months]
        suhu_max_per_stasiun[daftar_wmoid_stasiun[x]] = suhu_per_bulan

    final = {}
    temp = []
    for stasiun in daftar_wmoid_stasiun:
        try:
            final[replaced_to_nan[replaced_to_nan.wmoid == stasiun].iloc[0].nama_stasiun] = []
            for bulan in suhu_max_per_stasiun[stasiun]:
                try:
                    maximum = (bulan.iloc[0:7].suhu_maksimum.sum()) / 7
                    current = bulan.iloc[0]
                    for x in range(0, len(bulan) - 7):
                        if (bulan.iloc[x:x + 7].suhu_maksimum.sum()) / 7 > maximum:
                            maximum = (bulan.iloc[x:x + 7].suhu_maksimum.sum()) / 7
                            current = bulan.iloc[x]
                    temp.append([current.tanggal, current.suhu_maksimum])
                except:
                    pass
            final[replaced_to_nan[replaced_to_nan.wmoid == stasiun].iloc[0].nama_stasiun] = temp
            temp = []
        except:
            pass

    return fill_empty_month(final)


def bmkg_to_final(df):
    df.dropna(inplace=True)
    df_min = get_min_temperature_per_month(df)
    df_max = get_max_temperature_per_month(df)
    months = ["%.2d" % i for i in range(1, 13)]
    table = pd.DataFrame(columns=['stasiun', 'tipe'].extend(months))
    daftar_stasiun = df.nama_stasiun.unique()
    for x in daftar_stasiun:
        table = table.append({
            'stasiun': x,
            'tipe': 'min',
            't01': df_min[x][0][0],
            's01': df_min[x][0][1],
            't02': df_min[x][1][0],
            's02': df_min[x][1][1],
            't03': df_min[x][2][0],
            's03': df_min[x][2][1],
            't04': df_min[x][3][0],
            's04': df_min[x][3][1],
            't05': df_min[x][4][0],
            's05': df_min[x][4][1],
            't06': df_min[x][5][0],
            's06': df_min[x][5][1],
            't07': df_min[x][6][0],
            's07': df_min[x][6][1],
            't08': df_min[x][7][0],
            's08': df_min[x][7][1],
            't09': df_min[x][8][0],
            's09': df_min[x][8][1],
            't10': df_min[x][9][0],
            's10': df_min[x][9][1],
            't11': df_min[x][10][0],
            's11': df_min[x][10][1],
            't12': df_min[x][11][0],
            's12': df_min[x][11][1],
        }, ignore_index=True)
        table = table.append({
            'stasiun': x,
            'tipe': 'max',
            't01': df_max[x][0][0],
            's01': df_max[x][0][1],
            't02': df_max[x][1][0],
            's02': df_max[x][1][1],
            't03': df_max[x][2][0],
            's03': df_max[x][2][1],
            't04': df_max[x][3][0],
            's04': df_max[x][3][1],
            't05': df_max[x][4][0],
            's05': df_max[x][4][1],
            't06': df_max[x][5][0],
            's06': df_max[x][5][1],
            't07': df_max[x][6][0],
            's07': df_max[x][6][1],
            't08': df_max[x][7][0],
            's08': df_max[x][7][1],
            't09': df_max[x][8][0],
            's09': df_max[x][8][1],
            't10': df_max[x][9][0],
            's10': df_max[x][9][1],
            't11': df_max[x][10][0],
            's11': df_max[x][10][1],
            't12': df_max[x][11][0],
            's12': df_max[x][11][1],
        }, ignore_index=True)
    return table


def extract_insight(df, year):
    table = bmkg_to_final(df)
    table.to_csv(f'hasil_{year}.csv', sep=';')


def extract_insight_excel(raw, year):
    df = bmkg_to_final(raw)
    start_cells = [1]
    for row in range(2, len(df) + 1):
        if df.loc[row - 1, 'stasiun'] != df.loc[row - 2, 'stasiun']:
            start_cells.append(row)

    writer = pd.ExcelWriter(f"hasil_{year}.xlsx", engine='xlsxwriter')
    df.to_excel(writer, sheet_name=str(year), index=False)
    workbook = writer.book
    worksheet = writer.sheets[str(year)]
    merge_format = workbook.add_format({'align': 'center', 'valign': 'vcenter', 'border': 2})

    last_row = len(df)

    for row in start_cells:
        try:
            end_row = start_cells[start_cells.index(row) + 1] - 1
            if row == end_row:
                worksheet.write(row, 0, df.loc[row - 1, 'stasiun'], merge_format)
            else:
                worksheet.merge_range(row, 0, end_row, 0, df.loc[row - 1, 'stasiun'], merge_format)
        except IndexError:
            if row == last_row:
                worksheet.write(row, 0, df.loc[row - 1, 'stasiun'], merge_format)
            else:
                worksheet.merge_range(row, 0, last_row, 0, df.loc[row - 1, 'stasiun'], merge_format)

    writer.save()
