from tools.AIMengTools import AIMEngTools
from tools.ProspectiveStudentsTool import ProspectiveStudentsTool
from tools.EventTools import EventTools

class Executor:

    AVAILABLE_TOOLS = {
        **AIMEngTools.get_tool_map(),
        **ProspectiveStudentsTool.get_tool_map(),
        **EventTools.get_tool_map()
    }

    @classmethod
    def execute_tool(cls, name, args):
        print("Args : ", args)
        return cls.AVAILABLE_TOOLS.get(name)(**args)