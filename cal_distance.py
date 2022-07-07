# author: delta1037
# Date: 2022/05/01
# mail:geniusrabbit@qq.com
# 打包代码 pyinstaller -F -c cal_distance.py
import pandas as pd
from geopy import distance

INPUT_FILE = 'stationinfo.csv'
OUTPUT_FILE = 'host_tdf_distance.csv'

HOST_ID = 'hostid'
REQUIRE_COL_LIST = ['stationname', 'jingdu', 'weidu']  # 顺序不要动
OUTPUT_LIST = ['from_key', 'to_key', 'distance', 'light_speed_time']  # 顺序不要动

PI = 3.1415926
LIGHT_SPEED = 299792458


def cal_distance_batch():
    # 打开文件，检测是否包含需要的列
    input_df = pd.read_csv(INPUT_FILE, encoding='utf8')
    columns = input_df.columns
    for col in REQUIRE_COL_LIST:
        if col not in columns:
            print("[ERROR] 列 " + col + "不存在，请重试")
            return

    # 如果 不包含hostid列，就添加一列，值默认为“1”
    if HOST_ID not in columns:
        print("[WARN] 列 " + HOST_ID + " 不存在, 设置默认值1")
        input_df[HOST_ID] = "1"

    input_df[REQUIRE_COL_LIST[1]] = input_df[REQUIRE_COL_LIST[1]].astype(float) * 180 / PI
    input_df[REQUIRE_COL_LIST[2]] = input_df[REQUIRE_COL_LIST[2]].astype(float) * 180 / PI

    print(input_df)
    print(input_df.info())

    output_df = None
    # 计算任意两个站点之间的距离
    for idx_from, row_from in input_df.iterrows():
        for idx_to, row_to in input_df.iterrows():
            if idx_from == idx_to:
                continue
            # 计算距离和时间
            t_distance = distance.distance(
                    (row_from[REQUIRE_COL_LIST[2]], row_from[REQUIRE_COL_LIST[1]]),
                    (row_to[REQUIRE_COL_LIST[2]], row_to[REQUIRE_COL_LIST[1]])
                ).kilometers
            df = pd.DataFrame(
                    [[
                        row_from[HOST_ID] + '-' + row_from[REQUIRE_COL_LIST[0]],
                        row_to[HOST_ID] + '-'  + row_to[REQUIRE_COL_LIST[0]],
                        t_distance,
                        t_distance * 1000 / LIGHT_SPEED
                    ]],
                    columns=OUTPUT_LIST
                )
            if output_df is None:
                output_df = df
            else:
                output_df = pd.concat([output_df, df])

    # 输出结果文件
    if output_df is not None:
        output_df.to_csv(OUTPUT_FILE, index=False)


if __name__ == '__main__':
    cal_distance_batch()