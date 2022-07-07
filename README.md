# cal_distance
批量计算两个经纬度之间的距离

## 准备文件
源代码或者exe下需要有一个`stationinfo.csv`的文件，文件中必须包含`stationname`, `jingdu`, `weidu`列

注意：主机名字段`hostid`是可选的，如果没有，将设置默认值为“1”

## 源代码运行
使用源代码需要使用如下命令安装需要的包

```bash
pip install geopy pandas
```

运行：

```bash
python3 cal_distance.py
```

## 打包文件运行

将`stationinfo.csv`放到可执行文件同级目录下，双击可执行文件即可。