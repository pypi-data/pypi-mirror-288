#========================================================================================================================================
# CyborgAI CC BY-NC-ND 4.0 Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 Internation    https://github.com/cyborg-ai-git # 
#========================================================================================================================================

from evo_framework import *
from evo_package_assistant.entity import *
import importlib.util
from pathlib import Path
from evo_package_assistant.control.CAssistantCallback import CAssistantCallback
# ---------------------------------------------------------------------------------------------------------------------------------------
# UAssistant
# ---------------------------------------------------------------------------------------------------------------------------------------
""" UAssistant
"""
class UAssistantApi:  
    __instance = None

    def __init__(self):
        if UAssistantApi.__instance != None:
            raise Exception("ERROR_SINGLETON")
        else:
            UAssistantApi.__instance = self  
            self.pathAssistant:str|Any = None
            self.eAssistantMap:EAssistantMap = EAssistantMap()
# -----------------------------------------------------------------------------
    @staticmethod
    def getInstance():
        if UAssistantApi.__instance == None:
            uObject = UAssistantApi()
           # uObject.doInit()
            
        return UAssistantApi.__instance
# -----------------------------------------------------------------------------
    def doInit(self, isSkipLoad=False):
        try:   
           
            pathAssistantTmp = CSetting.getInstance().doGet("CYBORGAI_PATH_ASSETS_ASSISTANT")
        
            if pathAssistantTmp is None:
                IuLog.doError(__name__, f"ERROR_REQUIRED_ENV|CYBORGAI_PATH_ASSETS_ASSISTANT")
                pathAssistantTmp= "~/cyborgai/peer/peer-python/assistant"
                pathAssistantTmp = os.path.expanduser(pathAssistantTmp)
                IuLog.doWarning(__name__, f"WARNING_ENV_CYBORGAI_PATH_ASSETS_ASSISTANT_NONE_USE_{pathAssistantTmp}")
              
            self.pathAssistant = pathAssistantTmp  
            IuLog.doVerbose(__name__, f"pathAssistant:{self.pathAssistant}")
            
           
            self.eAssistantMap.doGenerateID()
            
            if not isSkipLoad:
                self.__doLoadDirEAssistant()
            
            
        except Exception as exception:
            IuLog.doException(__name__,exception)
            raise

# -----------------------------------------------------------------------------   
    async def doOnSet(self, eAction:EAction) -> EAction:
        try:
           raise Exception("ERROR_NOT_IMPLEMENTED")
        except Exception as exception:
            IuLog.doException(__name__,exception)
            raise
        

# -----------------------------------------------------------------------------   
    async def doOnGet(self, eAction:EAction) -> EAction:
        try:
           raise Exception("ERROR_NOT_IMPLEMENTED")
        except Exception as exception:
            IuLog.doException(__name__,exception)
            raise
        
# -----------------------------------------------------------------------------   
    async def doOnDel(self, eAction:EAction) -> EAction:
        try:
           raise Exception("ERROR_NOT_IMPLEMENTED")
        except Exception as exception:
            IuLog.doException(__name__,exception)
            raise
# -----------------------------------------------------------------------------   
    def doOnQuery(self, eAction:EAction) -> EAction:
        try:
           raise Exception("ERROR_NOT_IMPLEMENTED")
        except Exception as exception:
            IuLog.doException(__name__,exception)
            raise
              
# -----------------------------------------------------------------------------   
    def doSetEAssistant(self, eAssistant:EAssistant):
        try:
           self.eAssistantMap.mapEAssistant.doSet(eAssistant)
        except Exception as exception:
            IuLog.doException(__name__,exception)
            raise
        
# -----------------------------------------------------------------------------   
    async def doGetEAssistantQuery(self, eAssistantQuery:EAssistantQuery) -> EAssistant :
        try:
            if eAssistantQuery is None:
                raise Exception("ERROR_eAssistantQuery_NONE")
            
            if eAssistantQuery.query is None:
                raise Exception("ERROR_eAssistantQuery.query_NONE")
            
            arrayQuery = eAssistantQuery.query.split("=")
            
            if len(arrayQuery) != 2 and arrayQuery[0].lower() != "id":
                raise Exception("ERROR_eAssistantQuery.query_id_NONE")
                
            eAssistantID= arrayQuery[-1]
            
            return await self.doGetEAssistant(eAssistantID)
            
        except Exception as exception:
            IuLog.doException(__name__,exception)
            raise
# -----------------------------------------------------------------------------   
    async def doGetEAssistant(self, id:bytes) -> EAssistant:
        try:
            #id = bytes.fromhex(idIn)
            idStr = IuKey.toString(id).lower().replace(" ","_")
            if id in self.eAssistantMap.mapEAssistant.keys():
                return self.eAssistantMap.mapEAssistant.doGet(id)
            else:
                pathAssistant = f"{self.pathAssistant}/assistant_{idStr}.yaml"
                self.doLoadEAssistant(pathAssistant)
                
                IuLog.doVerbose(__name__, self.eAssistantMap)
                
                if id in self.eAssistantMap.mapEAssistant.keys():
                    return self.eAssistantMap.mapEAssistant.doGet(id)
                
                IuLog.doError(__name__,f"ERROR_NOT_FOUD_ASSISTANT|{pathAssistant}")
                
                raise Exception(f"ERROR_NOT_FOUD_ASSISTANT|{idStr}")
            
        except Exception as exception:
            IuLog.doException(__name__,exception)
            raise
# -----------------------------------------------------------------------------   
    async def doQuery(self, eAssistantQuery:EAssistantQuery) -> EAssistantMap:
        try:
            #TODO:query
            self.__doLoadDirEAssistant()
            yield self.eAssistantMap
        except Exception as exception:
            IuLog.doException(__name__,exception)
            raise
# -----------------------------------------------------------------------------   
    async def doDelEAssistant(self, id):
        try:
            self.eAssistantMap.mapEAssistant.doDel(id)
        except Exception as exception:
            IuLog.doException(__name__,exception)
            raise
#-------------------------------------------------------------------------------
    def __doLoadDirEAssistant(self):
        try:
            if self.pathAssistant is None:
                IuLog.doError(__name__, f"ERROR_REQUIRED_ENV|CYBORGAI_PATH_ASSETS_ASSISTANT")
            else:
                IuLog.doVerbose(__name__, f"self.pathAssistant {self.pathAssistant}")
                
                directory = Path(self.pathAssistant)
                
                arrayFileAssistant = [str(file) for file in directory.rglob('assistant_*.yaml')]
                
                if len(arrayFileAssistant) == 0:
                    IuLog.doWarning(__name__, f"WARNING:pathAssistant empty download assistant in {self.pathAssistant}")
                
                IuLog.doVerbose(__name__,f"arrayFileAssistant:\n{arrayFileAssistant}")

                for pathAssistant in arrayFileAssistant:
                    self.doLoadEAssistant(pathAssistant)
                
        except Exception as exception:
            IuLog.doException(__name__,exception)
            raise
        
#-------------------------------------------------------------------------------
    def doLoadEAssistant(self, pathAssistant):
        try:
            IuLog.doVerbose(__name__,f"pathAssistant: {pathAssistant}")
            
            mapAssistantFull = IuYAml.doLoad(pathAssistant)
            
            IuLog.doVerbose(__name__, f"{mapAssistantFull}")
        
            eAssistant = EAssistant()
            
            mapAssistant = mapAssistantFull["assistant"]
            
            name = str(mapAssistant["name"])
            systemMessage = str(mapAssistant["SYSTEM"])
            description = str(mapAssistant["description"])
            logo = str(mapAssistant["logo"])
            
            if "messages" in  mapAssistant: 
                arrayMessage = mapAssistant["messages"]
                for mapMessage in arrayMessage:
                    for messageRole, message in mapMessage.items():
                        role = str(messageRole).upper()
                        
                        enumAssistantRole = EnumAssistantRole.ASSISTANT
                        if role == "USER":
                            enumAssistantRole =  EnumAssistantRole.USER
                            
                        eAssistant.addMessage(enumAssistantRole, str(message))
                
           
            if "action" in  mapAssistantFull:    
                actionStr = ""   
                mapAction = mapAssistantFull["action"]
                for key, value in mapAction.items():
                    eAssistantAction = EAssistantAction()
                    eAssistantAction.doGenerateID(str(key))
                    eAssistantAction.doGenerateTime()
                    eAssistantAction.message = str(value)
                    actionStr = "\n".join([actionStr, f"{key}: {value}"])
                    eAssistant.mapAction.doSet(eAssistantAction)
                systemMessage = systemMessage.format(action_list = actionStr )
             
            idStr = name.replace(" ", "_").lower()               
            eAssistant.doGenerateID(f"{idStr}", isHash=False)
            eAssistant.name = f"{name}"
            eAssistant.systemMessage = systemMessage
            eAssistant.logo = logo
            eAssistant.description = description
            
            eAssistant.callback = CAssistantCallback(mapAssistantFull)
            
            if eAssistant.callback is None:
                raise Exception("ERROR_NOT_VALID|eAssistant.callback")
            
            self.eAssistantMap.mapEAssistant.doSet(eAssistant)
            
            IuLog.doVerbose(__name__, eAssistant)
            
            return eAssistant
                     
        except Exception as exception:
            IuLog.doException(__name__,exception)
            raise
'''      
#-------------------------------------------------------------------------------
    def doLoadEAssistantOld(self, pathAssistant):
        try:
            IuLog.doInfo(__name__,f"pathAssistant: {pathAssistant}")
            
            # Expand the user's home directory if ~ is used
            path = os.path.expanduser(pathAssistant)

            # Create a module spec from the file location
            spec = importlib.util.spec_from_file_location("loaded_assistant", path)

            # Create a new module based on the spec
            module = importlib.util.module_from_spec(spec)

            # Execute the module in its own namespace
            spec.loader.exec_module(module)

            # Optionally, add the module to sys.modules so it can be accessed as a normal import
            #sys.modules["loaded_assistant"] = module
            module.doAddEAssistant()
                
        except Exception as exception:
            IuLog.doException(__name__,exception)
            raise
'''