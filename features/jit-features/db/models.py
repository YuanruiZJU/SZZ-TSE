from sqlalchemy import Column, String, Integer, Boolean, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

###################################################################
#
# Models defining the Mysql tables used to store information
#
##################################################################


class CommitMeta(Base):
    """
    Currently, we only have the ground-truth labels of revisions
    in SVN repositories. A problem hindering the our study is that when
    using SVN commands, you must connect to network and interact
    with servers managing the repositories. It really slows down the
    progress of our study.

    Luckily, SVN revisions are corresponding to the git commits in the git
    repository, which gives us an opportunity to directly deal with
    git commits.
    """
    __tablename__ = 'commit_meta'

    id = Column(Integer, primary_key=True, autoincrement=True)
    project = Column(String(63), nullable=False)
    commit_id = Column(String(40), nullable=False)
    is_merge = Column(Boolean, nullable=False)
    time_stamp = Column(Integer, nullable=False)
    creation_time = Column(DateTime, nullable=False)


class DiffusionFeatures(Base):
    __tablename__ = 'diffusion_features'
    id = Column(Integer, primary_key=True, autoincrement=True)
    project = Column(String(63), nullable=False)
    commit_id = Column(String(63), nullable=False)
    ns = Column(Integer, nullable=False)
    nd = Column(Integer, nullable=False)
    nf = Column(Integer, nullable=False)
    entropy = Column(Float, nullable=False)


class SizeFeatures(Base):
    __tablename__ = 'size_features'
    id = Column(Integer, primary_key=True, autoincrement=True)
    project = Column(String(63), nullable=False)
    commit_id = Column(String(63), nullable=False)
    la = Column(Integer, nullable=False)
    ld = Column(Integer, nullable=False)
    lt = Column(Float, nullable=False)


class PurposeFeatures(Base):
    __tablename__ = 'purpose_features'
    id = Column(Integer, primary_key=True, autoincrement=True)
    project = Column(String(63), nullable=False)
    commit_id = Column(String(63), nullable=False)
    fix = Column(Integer, nullable=False)


class HistoryFeatures(Base):
    __tablename__ = 'history_features'
    id = Column(Integer, primary_key=True, autoincrement=True)
    project = Column(String(63), nullable=False)
    commit_id = Column(String(63), nullable=False)
    ndev = Column(Float, nullable=False)
    age = Column(Float, nullable=False)
    nuc = Column(Float, nullable=False)


class ExperienceFeatures(Base):
    __tablename__ = 'experience_features'

    id = Column(Integer, primary_key=True, autoincrement=True)
    project = Column(String(63), nullable=False)
    commit_id = Column(String(63), nullable=False)
    exp = Column(Integer, nullable=False)
    rexp = Column(Float, nullable=False)
    sexp = Column(Integer, nullable=False)



table_map = {
    'commit_meta': CommitMeta,
    'diffusion_features': DiffusionFeatures,
    'size_features': SizeFeatures,
    'purpose_features': PurposeFeatures,
    'history_features': HistoryFeatures,
    'experience_features': ExperienceFeatures
}
