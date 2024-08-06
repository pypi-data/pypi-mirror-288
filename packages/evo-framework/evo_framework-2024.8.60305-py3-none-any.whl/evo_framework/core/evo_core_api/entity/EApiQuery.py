#========================================================================================================================================
# CyborgAI CC BY-NC-ND 4.0 Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International  https://github.com/cyborg-ai-git 
#========================================================================================================================================

from evo_framework.entity.EObject import EObject
from evo_framework.core.evo_core_type.entity.EvoMap import EvoMap

#========================================================================================================================================
"""EApiQuery

    EApiQuery defines the structure for querying within the EVO framework, including collection, eObjectID ID, and query string.
    
"""
class EApiQuery(EObject):

    VERSION:str="ce9f61294905972208af38cd9b2952c960fec67016939deb88e4fd8a2a6f02c6"

    def __init__(self):
        super().__init__()
        
        self.collection:str = None
        self.eObjectID:bytes = None
        self.query:str = None
  
    def toStream(self, stream):
        super().toStream(stream)
        
        self._doWriteStr(self.collection, stream)
        self._doWriteBytes(self.eObjectID, stream)
        self._doWriteStr(self.query, stream)
        
    def fromStream(self, stream):
        super().fromStream(stream)
        
        self.collection = self._doReadStr(stream)
        self.eObjectID = self._doReadBytes(stream)
        self.query = self._doReadStr(stream)
    
    def __str__(self) -> str:
        strReturn = "\n".join([
                super().__str__(),
                            
                f"\tcollection:{self.collection}",
                f"\teObjectID length:{len(self.eObjectID) if self.eObjectID else 'None'}",
                f"\tquery:{self.query}",
                            ]) 
        return strReturn
    