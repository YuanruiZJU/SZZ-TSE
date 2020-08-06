from query.base import BaseQuery


class CommitMetaQuery(BaseQuery):
    table_name = 'commit_meta'


class DiffusionFeaturesQuery(BaseQuery):
    table_name = 'diffusion_features'


class SizeFeaturesQuery(BaseQuery):
    table_name = 'size_features'


class PurposeFeaturesQuery(BaseQuery):
    table_name = 'purpose_features'


class HistoryFeaturesQuery(BaseQuery):
    table_name = 'history_features'


class ExperienceFeaturesQuery(BaseQuery):
    table_name = 'experience_features'


class ProjectQuery:
    def __init__(self, project):
        self.project = project
        self.cms = CommitMetaQuery(project).do_query()
        self.diffusion_features = DiffusionFeaturesQuery(project).do_query()
        self.size_features = SizeFeaturesQuery(project).do_query()
        self.purpose_features = PurposeFeaturesQuery(project).do_query()
        self.history_features = HistoryFeaturesQuery(project).do_query()
        self.exp_features = ExperienceFeaturesQuery(project).do_query()
        self.__cache_end_commit_id = None

    @property
    def end_commit_id(self):
        if self.__cache_end_commit_id is not None:
            return self.__cache_end_commit_id
        commit_id = None
        for pf in self.purpose_features:
            if pf.fix:
                commit_id = pf.commit_id
        self.__cache_end_commit_id = commit_id
        return self.__cache_end_commit_id

    def combine(self):
        features_dict = dict()
        for sf in self.size_features:
            features_dict[sf.commit_id] = dict()
            features_dict[sf.commit_id]['la'] = sf.la
            features_dict[sf.commit_id]['ld'] = sf.ld
            features_dict[sf.commit_id]['lt'] = sf.lt
        for df in self.diffusion_features:
            features_dict[df.commit_id]['ns'] = df.ns
            features_dict[df.commit_id]['nd'] = df.nd
            features_dict[df.commit_id]['nf'] = df.nf
            features_dict[df.commit_id]['entropy'] = df.entropy
        for pf in self.purpose_features:
            features_dict[pf.commit_id]['fix'] = pf.fix
        for hf in self.history_features:
            features_dict[hf.commit_id]['ndev'] = hf.ndev
            features_dict[hf.commit_id]['age'] = hf.age
            features_dict[hf.commit_id]['nuc'] = hf.nuc
        for ef in self.exp_features:
            features_dict[ef.commit_id]['exp'] = ef.exp
            features_dict[ef.commit_id]['rexp'] = ef.rexp
            features_dict[ef.commit_id]['sexp'] = ef.sexp
        ret_list = list()
        for cm in self.cms:
            cm_dict = features_dict[cm.commit_id]
            if len(cm_dict) == 14:
                cm_dict['commit_id'] = cm.commit_id
                ret_list.append(cm_dict)
            if cm.commit_id == self.end_commit_id:
                break
        return ret_list

