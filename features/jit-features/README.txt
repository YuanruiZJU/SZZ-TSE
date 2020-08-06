Step1: 安装mysql，创建JIT数据库

Step2：Python安装python-mysql-connector, sqlalchemy, simplejson等安装包

Step3： 配置文件config.json

data_root_path: 设置数据放置的根目录
projects：设置研究项目存储目录，在data_root_path 下
git_log_path: 生成git日志的目录，在data_root_path 下
csv_path： 生成特征向量CSV的目录，在data_root_path下
label_csv_store_path: tests文件夹所在目录，tests文件夹下的csv目前存储了相关commit的标签，不要随便改动。

sql: mysql相关设置，填写username， password, dbname为JIT
local_time_zone: 东八时区


Step4：clone git仓库
clone研究项目到data_root_path下


Step5 依次运行下列文件
- log_generation.py，生成git日志
- features_db_store.py 存储特征到数据库
- csv_result.py, 生成含有特征向量的CSV


