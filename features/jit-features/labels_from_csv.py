from utils.csv_ops import parse_csv


def read_labels_from_csv(file_path):
    data_list = parse_csv(file_path)
    bug_introducing_set = set()
    for d in data_list:
        commit_id = d['commit_id']
        commit_label = d['buggy_RA']
        if commit_label.lower() == "buggy":
            bug_introducing_set.add(commit_id)
    return bug_introducing_set
