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
descList: list  # value = [('PMI1', <function <lambda> at 0x10d45ab90>), ('PMI2', <function <lambda> at 0x116d867a0>), ('PMI3', <function <lambda> at 0x116d86830>), ('NPR1', <function <lambda> at 0x116d868c0>), ('NPR2', <function <lambda> at 0x116d86950>), ('RadiusOfGyration', <function <lambda> at 0x116d869e0>), ('InertialShapeFactor', <function <lambda> at 0x116d86a70>), ('Eccentricity', <function <lambda> at 0x116d86b00>), ('Asphericity', <function <lambda> at 0x116d86b90>), ('SpherocityIndex', <function <lambda> at 0x116d86c20>), ('PBF', <function <lambda> at 0x116d86cb0>)]
