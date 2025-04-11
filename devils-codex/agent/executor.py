from tools.AIMengTools import AIMEngTools

class Executor:

    AVAILABLE_TOOLS = {
        **AIMEngTools.get_tool_map()
    }

    @classmethod
    def execute_tool(cls, name, args):
        print("Args : ", args)
        return cls.AVAILABLE_TOOLS.get(name)(**args)