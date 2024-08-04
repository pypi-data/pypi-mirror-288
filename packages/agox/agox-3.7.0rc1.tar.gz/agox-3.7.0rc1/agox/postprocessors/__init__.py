"""
While generators generate candidates, postprocessors are used to apply common 
postprocessing steps to all generated candidates. For example, the centering postprocessor
will center all candidates in the cell. 

The most common postprocessors is the relax postprocessor, which performs a local
optimization on all candidates. Parallel implementations of this postprocessor are
also available and are recommended for searches that generated multiple candidates 
pr. iteration. 
"""
from .ABC_postprocess import PostprocessBaseClass
from .minimum_dist import MinimumDistPostProcess
from .wrap import WrapperPostprocess
from .centering import CenteringPostProcess
from .relax import RelaxPostprocess
from .disjoint_filtering import DisjointFilteringPostprocess
from .ray_relax import ParallelRelaxPostprocess

__all__ = [
    'PostprocessBaseClass',
    'WrapperPostprocess',
    'CenteringPostProcess',
    'RelaxPostprocess',
    'DisjointFilteringPostprocess',
    'ParallelRelaxPostprocess', 
    'MinimumDistPostProcess']