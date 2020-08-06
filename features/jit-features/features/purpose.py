from features.git_commit_features import GitCommitFeatures
from git_analysis.analyze_git_logs import retrieve_git_logs
from object.features import PurposeFeatures as PurposeFeaturesObj


class PurposeFeatures(GitCommitFeatures):
    def __init__(self, rgcm):
        super(PurposeFeatures, self).__init__(rgcm)

    def extract(self):
        if self.check_identical_commit():
            return None

        fix = 0
        candidate_words=['bug', 'fix', 'wrong', 'error', 'fail', 'problem', 'patch']

        msg_tokens = self.msg.lower().split()
        for w in candidate_words:
            if w in msg_tokens:
                fix = 1

        return {
            'project': self.project,
            'commit_id': self.commit_id,
            'fix': fix
        }


def extract_to_db_obj(project):
    GitCommitFeatures.initialize(project)
    rgcms = retrieve_git_logs(project)
    db_objs = list()
    sorted_rgcms = sorted(rgcms, key=lambda x: x.time_stamp)
    for rgcm in sorted_rgcms:
        pf = PurposeFeatures(rgcm)
        attr_dict = pf.extract()
        if attr_dict is None:
            continue
        pf_obj = PurposeFeaturesObj(attr_dict)
        if getattr(pf_obj, 'fix') == 1:
            pf_obj.print_attributes()
        db_objs.append(pf_obj.to_db_obj())
    return db_objs


if __name__ == '__main__':
    project = 'hadoop-common'

