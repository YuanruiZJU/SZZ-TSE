import db.models as models
from config import conf
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class DbAPI:
    def __init__(self):
        self.__db_name = conf.sql_config.dbname
        self.__db_vendor = conf.sql_config.vendor
        self.__username = conf.sql_config.username
        self.__password = conf.sql_config.password
        self.engine = self.create_eng()
        # create tables
        models.Base.metadata.create_all(self.engine)
        self.__session = sessionmaker(bind=self.engine)()

    def create_eng(self):
        if self.__db_vendor == 'mysql':
            return create_engine('mysql+mysqlconnector://%s:%s@localhost:3306/%s?charset=utf8' %
                                 (self.__username, self.__password, self.__db_name))
        else:
            raise NotImplementedError

    def close_session(self):
        self.__session.close()

#######################################################################
#
# General DB APIs
#
#######################################################################

    def insert_objs(self, db_objs):
        for db_obj in db_objs:
            self.__session.add(db_obj)
        self.__session.commit()

    def retrieve_query(self, table_name, project=None, fields=None):
        try:
            db_model = models.table_map[table_name]
        except KeyError:
            return None
        query_fields = []
        if fields is not None:
            for f in fields:
                db_field = getattr(db_model, f, None)
                if db_field is not None:
                    query_fields.append(db_field)
        if len(query_fields) > 0:
            query = self.__session.query(*query_fields)
        else:
            query = self.__session.query(db_model)
        if project is not None:
            return query.filter(db_model.project == project)
        else:
            return query.filter()







