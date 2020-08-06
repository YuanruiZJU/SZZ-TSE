from db.api import DbAPI
from object.commit_meta import CommitMeta
from object.features import DiffusionFeatures
from object.features import SizeFeatures
from object.features import PurposeFeatures
from object.features import HistoryFeatures
from object.features import ExperienceFeatures

table_obj_map = {
    'commit_meta': CommitMeta,
    'diffusion_features': DiffusionFeatures,
    'size_features': SizeFeatures,
    'purpose_features': PurposeFeatures,
    'history_features': HistoryFeatures,
    'experience_features': ExperienceFeatures
}


class BaseQuery(object):
    table_name = ''

    def __init__(self, project=None):
        self.db_api = DbAPI()
        self.fields = None
        self.query_results = None
        self.project = project

    def initialize_fields(self, fields):
        self.fields = set()
        for f in fields:
            self.fields.add(f)

    def do_query(self):
        self.query_results = self.db_api.retrieve_query(self.table_name,
                                                        self.project,
                                                        self.fields)
        if self.query_results is None:
            return None
        obj_class = table_obj_map[self.table_name]
        if self.query_results is not None:
            ret_list = list()
            for q in self.query_results:
                ret_obj = obj_class()
                ret_obj.from_db_obj(q)
                ret_list.append(ret_obj)
            return ret_list

    def __del__(self):
        self.db_api.close_session()