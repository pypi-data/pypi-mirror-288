"""
 Descriptors derived from a molecule's 3D structure

"""
from __future__ import annotations
from rdkit.Chem.Descriptors import _isCallable
from rdkit.Chem import rdMolDescriptors
__all__ = ['CalcMolDescriptors3D', 'descList', 'rdMolDescriptors']
def CalcMolDescriptors3D(mol, confId = None):
    """
    
        Compute all 3D descriptors of a molecule
        
        Arguments:
        - mol: the molecule to work with
        - confId: conformer ID to work with. If not specified the default (-1) is used
        
        Return:
        
        dict
            A dictionary with decriptor names as keys and the descriptor values as values
    
        raises a ValueError 
            If the molecule does not have conformers
        
    """
def _setupDescriptors(namespace):
    ...
descList: list  # value = [('PMI1', <function <lambda> at 0x7f07a8a934c0>), ('PMI2', <function <lambda> at 0x7f0799bbd260>), ('PMI3', <function <lambda> at 0x7f0799bbd3a0>), ('NPR1', <function <lambda> at 0x7f0799bbd440>), ('NPR2', <function <lambda> at 0x7f0799bbd4e0>), ('RadiusOfGyration', <function <lambda> at 0x7f0799bbd580>), ('InertialShapeFactor', <function <lambda> at 0x7f0799bbd620>), ('Eccentricity', <function <lambda> at 0x7f0799bbd6c0>), ('Asphericity', <function <lambda> at 0x7f0799bbd760>), ('SpherocityIndex', <function <lambda> at 0x7f0799bbd800>), ('PBF', <function <lambda> at 0x7f0799bbd8a0>)]
