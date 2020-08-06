from features.git_commit_features import GitCommitFeatures
from copy import deepcopy
from utils.extensions import in_our_extensions
from git_analysis.analyze_git_logs import retrieve_git_logs
from object.features import SizeFeatures as SizeFeaturesObj


class SizeFeatures(GitCommitFeatures):

    def __init__(self, rgcm):
        super(SizeFeatures, self).__init__(rgcm)

    def evolve_from_prior_commit(self):
        lt = 0
        nf = 0
        gcf = GitCommitFeatures
        stats = self.stats
        namestats = self.namestat
        if len(self.parents) == 0:
            p = None
        elif len(self.parents) == 1:
            p = self.parents[0]
        else:
            if gcf.project_merge_numstat[self.commit_id].base_commit is not None:
                p = gcf.project_merge_numstat[self.commit_id].base_commit
                stats = gcf.project_merge_numstat[self.commit_id]
                namestats = gcf.project_merge_namestat[self.commit_id]
            else:
                p = self.parents[0]
                stats = None
        if stats is not None:
            files, rename_files = stats.modified_files
        else:
            files = []
            rename_files = []

        if p is not None:
            file_stats = gcf.parent_file_stats[p]['files']
            gcf.parent_file_stats[self.commit_id]['files'] = deepcopy(file_stats)
        for f, added, deleted in files:
            if f not in namestats.file_modify_type:
                continue
            if namestats.file_modify_type[f] == 'add':
                assert (deleted == 0)
                gcf.parent_file_stats[self.commit_id]['files'][f] = added
                if in_our_extensions(f):
                    nf += 1
            elif namestats.file_modify_type[f] == 'delete':
                assert (added == 0)
                # assert(deleted == file_stats[f])
                if in_our_extensions(f):
                    try:
                        lt += file_stats[f]
                        nf += 1
                        del gcf.parent_file_stats[self.commit_id]['files'][f]
                    except KeyError:
                        pass
            elif namestats.file_modify_type[f] == 'rename':
                cur_file = rename_files[f]
                tmp = file_stats[f]
                assert (tmp + added - deleted >= 0)
                gcf.parent_file_stats[self.commit_id]['files'][cur_file] = tmp + added - deleted
                if in_our_extensions(f) or in_our_extensions(cur_file):
                    lt += tmp
                    nf += 1
                del gcf.parent_file_stats[self.commit_id]['files'][f]
            else:
                assert (namestats.file_modify_type[f] == 'modify')
                try:
                    tmp = file_stats[f]
                    assert (tmp + added - deleted >= 0)
                    gcf.parent_file_stats[self.commit_id]['files'][f] = tmp + added - deleted
                except KeyError:
                    tmp = 0
                except AssertionError:
                    tmp = 0
                    gcf.parent_file_stats[self.commit_id]['files'][f] = 0

                if in_our_extensions(f):
                    lt += tmp
                    nf += 1
        if len(self.parents) > 1:
            lt = 0
        else:
            nf = len(files)
            if nf > 0:
                lt = 1.0 * lt / nf
        for p in self.parents:
            if gcf.parent_file_stats[p]['son_num'] <= 1:
                del gcf.parent_file_stats[p]
            else:
                gcf.parent_file_stats[p]['son_num'] -= 1
        return lt

    def extract(self):
        gcf = GitCommitFeatures
        if len(self.parents) > 1:
            la = 0
            ld = 0
        else:
            la = self.stats.added_number
            ld = self.stats.deleted_number
        gcf.parent_file_stats[self.commit_id] = dict()
        gcf.parent_file_stats[self.commit_id]['files'] = dict()
        gcf.parent_file_stats[self.commit_id]['son_num'] = len(self.sons)
        lt = self.evolve_from_prior_commit()
        return {'project': self.project,
                'commit_id': self.commit_id,
                'la': la, 'ld': ld, 'lt': lt}


def extract_to_db_obj(project):
    gcf = GitCommitFeatures
    gcf.initialize(project)
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
    while len(SizeFeatures.current_root) > 0:
        extract_results = gcf.calculate_features_for_root(SizeFeatures)
        assert(isinstance(extract_results, list))
        for er in extract_results:
            sf_obj = SizeFeaturesObj(er)
            sf_obj.print_attributes()
            db_objs.append(sf_obj.to_db_obj())
    return db_objs


if __name__ == '__main__':
    project = 'jetty'
    extract_to_db_obj(project)


