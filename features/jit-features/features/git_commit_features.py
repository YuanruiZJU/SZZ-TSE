from git_analysis.analyze_git_logs import retrieve_git_logs
from git_analysis.analyze_git_namestat import retrieve_git_namestats
from git_analysis.analyze_git_numstat import get_numstats
from git_analysis.git_stats.git_commit_meta import RawGitCommitMeta
from utils.extensions import in_our_extensions
from copy import deepcopy


class GitCommitFeatures(object):
    project_numstat = None
    project_logs = None
    project_namestat = None
    project_merge_numstat = None
    project_merge_namestat = None
    candidate_commit = set()
    committer_time = dict()
    developer_stats = dict()
    parent_file_stats = dict()
    rgcm_dict = dict()
    current_root = set()
    calculated_commit = set()

    def __init__(self, rgcm):
        assert(isinstance(rgcm, RawGitCommitMeta))
        self.project = rgcm.project
        self.commit_id = rgcm.commit_id
        self.parents = rgcm.parent
        self.stats = GitCommitFeatures.project_numstat[self.commit_id]
        self.namestat = GitCommitFeatures.project_namestat[self.commit_id]
        self.committer_email = rgcm.committer_email
        self.time_stamp = rgcm.time_stamp
        self.author_email = rgcm.author_email
        self.sons = rgcm.sons
        self.msg = rgcm.commit_message

    def in_required_extensions(self, file_path):
        if len(self.parents) > 1:
            return False
        if in_our_extensions(file_path):
            return True
        files, rename_files = self.stats.modified_files
        if self.namestat.file_modify_type[file_path] == 'rename':
            cur_path = rename_files[file_path]
            if in_our_extensions(cur_path):
                return True
        return False

    @staticmethod
    def light_initialize():
        GitCommitFeatures.committer_time = dict()
        GitCommitFeatures.file_stats = dict()
        GitCommitFeatures.developer_stats = dict()
        GitCommitFeatures.parent_file_stats = dict()
        GitCommitFeatures.candidate_commit = set()
        GitCommitFeatures.rgcm_dict = dict()
        GitCommitFeatures.current_root = set()
        GitCommitFeatures.calculated_commit = set()

    @staticmethod
    def initialize(project, merge_all_log=False):
        gcf = GitCommitFeatures
        gcf.project_logs = retrieve_git_logs(project)
        gcf.project_numstat = get_numstats(project)
        gcf.project_namestat = retrieve_git_namestats(project)
        gcf.project_merge_namestat = retrieve_git_namestats(project, True, merge_all_log)
        gcf.project_merge_numstat = get_numstats(project, True, merge_all_log)

        gcf.committer_time = dict()
        gcf.file_stats = dict()
        gcf.developer_stats = dict()
        gcf.parent_file_stats = dict()
        gcf.candidate_commit = set()
        gcf.rgcm_dict = dict()
        gcf.current_root = set()
        gcf.calculated_commit = set()

    @staticmethod
    def calculate_features_for_root(feature_class):
        gcf = GitCommitFeatures
        extracted_results = list()
        if len(gcf.current_root) == 0:
            return
        for r in gcf.current_root:
            fc_obj = feature_class(gcf.rgcm_dict[r])
            extracted_results.append(fc_obj.extract())
            gcf.calculated_commit.add(r)
        original_root = deepcopy(gcf.current_root)
        gcf.current_root = set()
        for s in gcf.candidate_commit:
            parent_not_cal = False
            for p in gcf.rgcm_dict[s].parent:
                if p not in gcf.calculated_commit:
                    parent_not_cal = True
                    break
            if not parent_not_cal:
                gcf.current_root.add(s)

        for r in original_root:
            for s in gcf.rgcm_dict[r].sons:
                if s in gcf.current_root:
                    continue
                if len(gcf.rgcm_dict[s].parent) == 1:
                    gcf.current_root.add(s)
                else:
                    all_parent_calculated = True
                    for p in gcf.rgcm_dict[s].parent:
                        if p not in gcf.calculated_commit:
                            all_parent_calculated = False
                    if all_parent_calculated:
                        gcf.current_root.add(s)
                    else:
                        gcf.candidate_commit.add(s)
        tmp = deepcopy(gcf.candidate_commit)
        for s in tmp:
            if s in gcf.current_root:
                gcf.candidate_commit.remove(s)
        return extracted_results

    def check_identical_commit(self):
        try:
            GitCommitFeatures.committer_time[self.committer_email]
        except KeyError:
            GitCommitFeatures.committer_time[self.committer_email] = set()
        if self.time_stamp not in GitCommitFeatures.committer_time[self.committer_email]:
            GitCommitFeatures.committer_time[self.committer_email].add(self.time_stamp)
            return False
        else:
            return True
