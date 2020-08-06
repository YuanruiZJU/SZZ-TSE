from object import commit_meta
from git_analysis.analyze_git_logs import retrieve_git_logs
from db.api import DbAPI
from features import diffusion
from features import experience
from features import history
from features import purpose
from features import size


def store_meta(project):
    gls = retrieve_git_logs(project)
    db_objs = list()
    for gl in gls:
        cm = commit_meta.CommitMeta()
        cm.from_git_log(gl)
        db_objs.append(cm.to_db_obj())
    db_api = DbAPI()
    db_api.insert_objs(db_objs)
    db_api.close_session()


def store_features(project, feature_type):
    if feature_type == 'diffusion':
        db_objs = diffusion.extract_to_db_obj(project)
    elif feature_type == 'experience':
        db_objs = experience.extract_to_db_obj(project)
    elif feature_type == 'history':
        db_objs = history.extract_to_db_obj(project)
    elif feature_type == 'purpose':
        db_objs = purpose.extract_to_db_obj(project)
    else:
        assert(feature_type == 'size')
        db_objs = size.extract_to_db_obj(project)
    db_api = DbAPI()
    db_api.insert_objs(db_objs)
    db_api.close_session()

if __name__ == '__main__':
    project = 'activemq'
    store_meta(project)
    store_features(project, 'diffusion')
    store_features(project, 'experience')
    store_features(project, 'history')
    store_features(project, 'purpose')
    store_features(project, 'size')
