from features.git_commit_features import GitCommitFeatures
from copy import deepcopy
from git_analysis.analyze_git_logs import retrieve_git_logs
from object.features import HistoryFeatures as HistoryFeaturesObj


class HistoryFeatures(GitCommitFeatures):
    def __init__(self, rgcm):
        super(HistoryFeatures, self).__init__(rgcm)

    def create_file_record(self, path, identical):
        gcf = GitCommitFeatures
        gcf.parent_file_stats[self.commit_id]['files'][path] = dict()
        gcf.parent_file_stats[self.commit_id]['files'][path]['developers'] = set()
        gcf.parent_file_stats[self.commit_id]['files'][path]['developers'].add(self.author_email)
        gcf.parent_file_stats[self.commit_id]['files'][path]['changes'] = set()
        if not identical:
            gcf.parent_file_stats[self.commit_id]['files'][path]['changes'].add(self.commit_id)
        gcf.parent_file_stats[self.commit_id]['files'][path]['last_age'] = self.time_stamp

    def evolve_non_merge(self, identical):
        assert(len(self.parents) <= 1)
        gcf = GitCommitFeatures
        stats = self.stats
        namestats = self.namestat
        dev_set = set()
        age = 0
        change_set = set()
        files, rename_files = stats.modified_files
        p = None
        p_file_stats = None
        nf = 0
        if len(self.parents) == 1:
            p = self.parents[0]
            p_file_stats = gcf.parent_file_stats[p]['files']
            if gcf.parent_file_stats[p]['son_num'] == 1:
                gcf.parent_file_stats[self.commit_id]['files'] = p_file_stats
            else:
                gcf.parent_file_stats[self.commit_id]['files'] = deepcopy(p_file_stats)
        for f, added, deleted in files:
            if f.endswith("/"):
                continue
            nf += 1
            if namestats.file_modify_type[f] == 'add':
                assert (deleted == 0)
                self.create_file_record(f, identical)
            elif namestats.file_modify_type[f] == 'delete':
                assert (p is not None)
                dev_set |= p_file_stats[f]['developers']
                change_set |= p_file_stats[f]['changes']
                age += 1.0 * (self.time_stamp - p_file_stats[f]['last_age']) / 86400.0
                del gcf.parent_file_stats[self.commit_id]['files'][f]
            elif namestats.file_modify_type[f] == 'rename':
                assert (p is not None)
                cur_file = rename_files[f]
                dev_set |= p_file_stats[f]['developers']
                change_set |= p_file_stats[f]['changes']
                age += 1.0 * (self.time_stamp - p_file_stats[f]['last_age']) / 86400.0
                gcf.parent_file_stats[self.commit_id]['files'][cur_file] = deepcopy(p_file_stats[f])
                gcf.parent_file_stats[self.commit_id]['files'][cur_file]['developers'].add(self.author_email)
                if not identical:
                    gcf.parent_file_stats[self.commit_id]['files'][cur_file]['changes'].add(self.commit_id)
                gcf.parent_file_stats[self.commit_id]['files'][cur_file]['last_age'] = self.time_stamp
                del gcf.parent_file_stats[self.commit_id]['files'][f]
            else:
                assert (namestats.file_modify_type[f] == 'modify')
                assert (p is not None)
                try:
                    dev_set |= p_file_stats[f]['developers']
                    change_set |= p_file_stats[f]['changes']
                    age += 1.0 * (self.time_stamp - p_file_stats[f]['last_age']) / 86400.0
                except KeyError:
                    gcf.parent_file_stats[self.commit_id]['files'][f] = dict()
                    gcf.parent_file_stats[self.commit_id]['files'][f]['developers'] = set()
                    gcf.parent_file_stats[self.commit_id]['files'][f]['changes'] = set()
                gcf.parent_file_stats[self.commit_id]['files'][f]['developers'].add(self.author_email)
                if not identical:
                    gcf.parent_file_stats[self.commit_id]['files'][f]['changes'].add(self.commit_id)
                gcf.parent_file_stats[self.commit_id]['files'][f]['last_age'] = self.time_stamp
        ndev = len(dev_set)
        nuc = len(change_set)
        if nf > 0:
            nuc = 1.0 * nuc / nf
            age = age / nf

        if len(self.parents) == 1:
            if gcf.parent_file_stats[p]['son_num'] <= 1:
                del gcf.parent_file_stats[p]
            else:
                gcf.parent_file_stats[p]['son_num'] -= 1

        return {
            'project': self.project,
            'commit_id': self.commit_id,
            'ndev': ndev,
            'age': age,
            'nuc': nuc
        }

    def evolve_merge(self, identical):
        gcf = GitCommitFeatures
        assert(len(self.parents) > 1)
        for p in self.parents:
            p_file_stats = gcf.parent_file_stats[p]['files']
            file_paths = p_file_stats.keys()
            for f in file_paths:
                try:
                    gcf.parent_file_stats[self.commit_id]['files'][f]
                except KeyError:
                    gcf.parent_file_stats[self.commit_id]['files'][f] = dict()
                    gcf.parent_file_stats[self.commit_id]['files'][f]['developers'] = set()
                    gcf.parent_file_stats[self.commit_id]['files'][f]['changes'] = set()
                    gcf.parent_file_stats[self.commit_id]['files'][f]['last_age'] = \
                        p_file_stats[f]['last_age']
                gcf.parent_file_stats[self.commit_id]['files'][f]['developers'] |= \
                    p_file_stats[f]['developers']
                gcf.parent_file_stats[self.commit_id]['files'][f]['changes'] |= p_file_stats[f]['changes']
                if gcf.parent_file_stats[self.commit_id]['files'][f]['last_age'] < \
                    p_file_stats[f]['last_age']:
                    gcf.parent_file_stats[self.commit_id]['files'][f]['last_age'] = \
                        p_file_stats[f]['last_age']

        added_files = set()
        renamed_cur_files = set()
        for p in self.parents:
            try:
                namestats = gcf.project_merge_namestat[self.commit_id+'_'+p]
                stats = gcf.project_merge_numstat[self.commit_id+'_'+p]
            except KeyError:
                continue
            files, rename_files = stats.modified_files
            for f, added, deleted in files:
                if f not in namestats.file_modify_type.keys():
                    continue
                try:
                    p_file_stats = gcf.parent_file_stats[self.commit_id]['files'][f]
                except KeyError:
                    if namestats.file_modify_type[f] in ['delete', 'rename']:
                        continue
                    elif namestats.file_modify_type[f] == 'add':
                        added_files.add(f)
                if namestats.file_modify_type[f] == 'delete':
                    assert (added == 0 and p is not None)
                    del gcf.parent_file_stats[self.commit_id]['files'][f]
                elif namestats.file_modify_type[f] == 'rename':
                    assert (p is not None)
                    cur_file = rename_files[f]
                    renamed_cur_files.add(cur_file)
                    try:
                        gcf.parent_file_stats[self.commit_id]['files'][cur_file]
                    except KeyError:
                        gcf.parent_file_stats[self.commit_id]['files'][cur_file] = dict()
                        gcf.parent_file_stats[self.commit_id]['files'][cur_file]['developers'] = set()
                        gcf.parent_file_stats[self.commit_id]['files'][cur_file]['changes'] = set()
                        gcf.parent_file_stats[self.commit_id]['files'][cur_file]['last_age'] = \
                            p_file_stats['last_age']
                    gcf.parent_file_stats[self.commit_id]['files'][cur_file]['developers'] |= \
                        p_file_stats['developers']
                    gcf.parent_file_stats[self.commit_id]['files'][cur_file]['changes'] |= \
                        p_file_stats['changes']
                    if gcf.parent_file_stats[self.commit_id]['files'][cur_file]['last_age'] < \
                        p_file_stats['last_age']:
                        gcf.parent_file_stats[self.commit_id]['files'][cur_file]['last_age'] = \
                            p_file_stats['last_age']
                    del gcf.parent_file_stats[self.commit_id]['files'][f]
        for added_f in added_files:
            if added_f not in renamed_cur_files:
                self.create_file_record(added_f, identical=identical)
        for p in self.parents:
            if gcf.parent_file_stats[p]['son_num'] <= 1:
                del gcf.parent_file_stats[p]
            else:
                gcf.parent_file_stats[p]['son_num'] -= 1
        return {'project': self.project,
                'commit_id': self.commit_id,
                'ndev': 0, 'age': 0, 'nuc': 0}

    def extract(self):
        check_identical = self.check_identical_commit()
        gcf = GitCommitFeatures
        gcf.parent_file_stats[self.commit_id] = dict()
        gcf.parent_file_stats[self.commit_id]['files'] = dict()
        gcf.parent_file_stats[self.commit_id]['son_num'] = len(self.sons)
        if len(self.parents) <= 1:
            return self.evolve_non_merge(check_identical)
        else:
            return self.evolve_merge(check_identical)


def extract_to_db_obj(project):
    gcf = GitCommitFeatures
    gcf.initialize(project, True)
    rgcms = retrieve_git_logs(project)
    db_objs = list()
    root = set()
    rgcm_dict = dict()
    for rgcm in rgcms:
        rgcm_dict[rgcm.commit_id] = rgcm
        if len(rgcm.parent) == 0:
            root.add(rgcm.commit_id)
    gcf.current_root = root
    gcf.calculated_commit = set()
    gcf.candidate_commit = set()
    gcf.rgcm_dict = rgcm_dict
    number = 0
    while len(gcf.current_root) > 0:
        number += len(gcf.current_root)
        extract_results = gcf.calculate_features_for_root(HistoryFeatures)
        assert(isinstance(extract_results, list))
        for er in extract_results:
            sf_obj = HistoryFeaturesObj(er)
            sf_obj.print_attributes()
            db_objs.append(sf_obj.to_db_obj())
    return db_objs


if __name__ == '__main__':
    project = 'activemq'
    extract_to_db_obj(project)

