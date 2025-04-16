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
            "name": "get_tuition_fee",
            "description": "Get's details about the ESTIMATED tuition fee for the AI Meng Program.",
            "parameters": {}
        },
        {
            "type": "function",
            "name": "get_application_requirements",
            "description": "Get details about the documents and exams required for applying to Master of Engineering programs.",
            "parameters": {}
        }
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
    
    tuition_url = "https://masters.pratt.duke.edu/admissions/tuition-financial-aid/"
    @classmethod
    def get_tuition_fee(cls):
        context = ssl._create_unverified_context()
        page = urlopen(cls.tuition_url, context = context).read()
        
        soup = BeautifulSoup(page, 'lxml')
        table = soup.find("h3", string="Artificial Intelligence Master of Engineering").find_next("table")
        return table

    
    @classmethod
    def get_tool_map(cls):
        TOOLS_MAP = {
            "get_tuition_fee": cls.get_tuition_fee,
            "get_application_requirements": cls.get_application_requirements
        }
        return TOOLS_MAP
    
    application_requirements_url = "https://masters.pratt.duke.edu/apply/instructions/"
    @classmethod
    def get_application_requirements(cls):
        context = ssl._create_unverified_context()
        page = urlopen(cls.application_requirements_url, context = context).read()
        
        soup = BeautifulSoup(page, 'lxml')
        information = soup.find("h2", string="Master of Engineering Programs").find_parent("section").text
        return information.strip()
    
    



if __name__ == "__main__":
    # response = ProspectiveStudentsTool.get_list_faq(program = "ms")
    # response = ProspectiveStudentsTool.get_faq_answer(program = "phd", faq_number = 7)
    # response = ProspectiveStudentsTool.get_tuition_fee()
    response = ProspectiveStudentsTool.get_application_requirements()
    print(response)
        


