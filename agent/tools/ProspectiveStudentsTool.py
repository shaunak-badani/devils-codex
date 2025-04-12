from dotenv import load_dotenv
from urllib.request import urlopen
from bs4 import BeautifulSoup
import ssl


load_dotenv()
class ProspectiveStudentsTool:

    FAQ_PAGE="https://stat.duke.edu/{program}/frequently-asked-questions"
    ALLOWED_PROGRAM_VALUES = ["ms", "phd"]

    TOOLS_SCHEMA = [
        {
            "type": "function",
            "name": "get_list_faq",
            "description": "Gets the list of frequently asked questions for prospective MS or PHD Duke Students",
            "parameters": {
                "type": "object",
                "properties": {
                    "program": {
                        "type": "string",
                        "enum": ALLOWED_PROGRAM_VALUES,
                        "description": f"The program the prospective student is in : ms or phd"
                    }
                },
            }
        },
        {
            "type": "function",
            "name": "get_faq_answer",
            "description": "Gets the answer to the nth FAQ for prospective MS or PHD Duke Students",
            "parameters": {
                "type": "object",
                "properties": {
                    "program": {
                        "type": "string",
                        "enum": ALLOWED_PROGRAM_VALUES,
                        "description": f"The program the prospective student is in : ms or phd"
                    },
                    "faq_number": {
                        "type": "integer",
                        "description": f"The number of the faq program in the list."
                    }
                },
            }
        },
    ]

    @classmethod
    def get_list_faq(cls, *, program):
        if program not in cls.ALLOWED_PROGRAM_VALUES:
            print(f"Program {program} is not supported!")
            return []
        program_url = cls.FAQ_PAGE.format(program = program)

        context = ssl._create_unverified_context()
        page = urlopen(program_url, context = context).read()
        soup = BeautifulSoup(page, 'lxml')
        div_block = soup.find(id="block-tts-sub-content")
        all_questions = div_block.find("ul").find_all("li")
        questions = []
        for decorated_question in all_questions:
            questions.extend(list(decorated_question.stripped_strings))
        return questions
    
    @classmethod
    def get_faq_answer(cls, *, program, faq_number):
        """
        Get answer to nth faq for program
        """
        if program not in cls.ALLOWED_PROGRAM_VALUES:
            print(f"Program {program} is not supported!")
            return []
        program_url = cls.FAQ_PAGE.format(program = program)

        
        context = ssl._create_unverified_context()
        page = urlopen(program_url, context = context).read()
        
        soup = BeautifulSoup(page, 'lxml')
        div_block = soup.find(id="block-tts-sub-content")
        all_questions = div_block.find("ul").find_all("li")
        if faq_number >= len(all_questions):
            print(f"Cannot find faq number {faq_number}")
            return ""
        question_number = all_questions[faq_number]
        anchor_value = question_number.find("a").get("href").lstrip("#")
        next_sibling = soup.find("a", attrs={"name": anchor_value}).parent.find_next_sibling("p")
        answer = ""
        while next_sibling and next_sibling.name == "p":
            answer += next_sibling.text
            next_sibling = next_sibling.find_next_sibling()
        return answer

    
    @classmethod
    def get_tool_map(cls):
        TOOLS_MAP = {
            "get_list_faq": cls.get_list_faq,
            "get_faq_answer": cls.get_faq_answer
        }
        return TOOLS_MAP

if __name__ == "__main__":
    # response = ProspectiveStudentsTool.get_list_faq(program = "ms")
    response = ProspectiveStudentsTool.get_faq_answer(program = "phd", faq_number = 7)
    print(response)
        


