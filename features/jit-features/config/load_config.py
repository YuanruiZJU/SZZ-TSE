import simplejson
import os

PARENT_PATH = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
CONFIG_PATH = os.path.join(PARENT_PATH, "config.json")

class Config:
    def __init__(self):
        with open(CONFIG_PATH, 'r') as conf:
            conf_str = conf.read()
            conf_json = simplejson.loads(conf_str)
            self.data_path = conf_json['data_root_path']
            self.git_log_path = os.path.join(self.data_path, conf_json['git_log_path'])
            self.projects = conf_json['projects']
            self.sql_config = SQLConfig(conf_json['sql'])
            self.consider_extensions = set(conf_json['extensions'])
            self.csv_store_path = conf_json['label_csv_store_path']
            self.feature_csv_path = os.path.join(self.data_path, conf_json['csv_path'])

    def project_log_path(self, project_name, log_filename=None):
        assert(project_name in self.projects)
        path = os.path.join(self.git_log_path, project_name)
        if not os.path.exists(path):
            os.makedirs(path)
        if log_filename is None:
            return path
        else:
            return os.path.join(path, log_filename + '.log')

    def project_path(self, project_name):
        assert(project_name in self.projects)
        return os.path.join(self.data_path, project_name)

    def project_label_csv_path(self, project_name):
        return os.path.join(self.csv_store_path, project_name+".csv")

    def project_feature_csv_path(self, project_name):
        return os.path.join(self.feature_csv_path, project_name+".csv")


class SQLConfig:
    def __init__(self, sql_json):
        self.vendor = sql_json['vendor']
        self.dbname = sql_json['dbname']
        self.username = sql_json['username']
        self.password = sql_json['password']

