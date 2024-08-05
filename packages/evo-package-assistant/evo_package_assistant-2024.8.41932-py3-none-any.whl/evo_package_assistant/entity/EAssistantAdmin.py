#========================================================================================================================================
# CyborgAI CC BY-NC-ND 4.0 Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International  https://github.com/cyborg-ai-git 
#========================================================================================================================================

from evo_framework.entity.EObject import EObject
from evo_framework.core.evo_core_type.entity.EvoMap import EvoMap

from evo_framework.core.evo_core_api.entity.EApiAdmin import EApiAdmin
from evo_package_assistant.entity.EAssistantQuery import EAssistantQuery
#========================================================================================================================================
"""EAssistantAdmin

    EAssistantAdmin _DOC_
    
"""
class EAssistantAdmin(EObject):

    VERSION:str="8c46a1e6100f393cc46ea5742fe0d559c79177f60ac90463bb765587b62b7f84"

    def __init__(self):
        super().__init__()
        
        self.eApiAdmin:EApiAdmin = None
        self.eAssistantQuery:EAssistantQuery = None
  
    def toStream(self, stream):
        super().toStream(stream)
        
        self._doWriteEObject(self.eApiAdmin, stream)
        self._doWriteEObject(self.eAssistantQuery, stream)
        
    def fromStream(self, stream):
        super().fromStream(stream)
        
        self.eApiAdmin = self._doReadEObject(EApiAdmin, stream)
        self.eAssistantQuery = self._doReadEObject(EAssistantQuery, stream)
    
    def __str__(self) -> str:
        strReturn = "\n".join([
                super().__str__(),
                            
                f"\teApiAdmin:{self.eApiAdmin}",
                f"\teAssistantQuery:{self.eAssistantQuery}",
                            ]) 
        return strReturn
    