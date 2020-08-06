from query.query import ProjectQuery
from utils.csv_ops import write_csv
from config import conf
from labels_from_csv import read_labels_from_csv


HEADERS = ['commit_id', 'la', 'ld', 'lt', 'ns', 'nd', 'nf', 'entropy', 'fix', 'ndev', 'age', 'nuc', 'exp', 'rexp', 'sexp']


def combine_label_with_features(change_list, bug_introducing_set):
    new_change_list = list()
    for c in change_list:
        tmp_data = c
        assert isinstance(tmp_data, dict)
        tmp_data['label'] = False
        if c['commit_id'] in bug_introducing_set:
            tmp_data['label'] = True
        new_change_list.append(tmp_data)
    return new_change_list


def csv_to_disk(project):
    assert isinstance(project, str)
    q = ProjectQuery(project)
    change_list = q.combine()
    assert isinstance(change_list, list)

    label_csv_path = conf.project_label_csv_path(project)
    bug_introducing_set = read_labels_from_csv(label_csv_path)

    new_change_list = combine_label_with_features(change_list, bug_introducing_set)
    project_csv_path = conf.project_feature_csv_path(project)
    write_csv(project_csv_path, new_change_list, HEADERS)


if __name__ == '__main__':
    for p in conf.projects:
        csv_to_disk(p)
