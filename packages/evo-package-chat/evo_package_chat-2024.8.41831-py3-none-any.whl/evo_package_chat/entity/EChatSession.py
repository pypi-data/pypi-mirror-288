#========================================================================================================================================
# CyborgAI CC BY-NC-ND 4.0 Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International  https://github.com/cyborg-ai-git 
#========================================================================================================================================

from evo_framework.entity.EObject import EObject
from evo_framework.core.evo_core_type.entity.EvoMap import EvoMap

#========================================================================================================================================
"""EChatSession

    EChatSession _DOC_
    
"""
class EChatSession(EObject):

    VERSION:str="4c91f647279e7891cdbc68d31ebdf562041cf2cae8f3c4f0c4e40302a5cac0f8"

    def __init__(self):
        super().__init__()
        
        self.sessionID:bytes = None
        self.sessionApi:str = None
  
    def toStream(self, stream):
        super().toStream(stream)
        
        self._doWriteBytes(self.sessionID, stream)
        self._doWriteStr(self.sessionApi, stream)
        
    def fromStream(self, stream):
        super().fromStream(stream)
        
        self.sessionID = self._doReadBytes(stream)
        self.sessionApi = self._doReadStr(stream)
    
    def __str__(self) -> str:
        strReturn = "\n".join([
                super().__str__(),
                            
                f"\tsessionID length:{len(self.sessionID) if self.sessionID else 'None'}",
                f"\tsessionApi:{self.sessionApi}",
                            ]) 
        return strReturn
    