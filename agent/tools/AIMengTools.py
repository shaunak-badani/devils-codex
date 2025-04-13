import requests
from dotenv import load_dotenv
import urllib.parse
import requests
import os
from bs4 import BeautifulSoup

load_dotenv()
class AIMEngTools:
    __course_name = "AIPI - AI for Product Innovation"
    __encoded_course_name = urllib.parse.quote(__course_name)
    __params = {"access_token": os.environ.get("DUKE_API_KEY")}
    courses_url = f"https://streamer.oit.duke.edu/curriculum/courses/subject/{__encoded_course_name}"
    course_details_url = f"https://streamer.oit.duke.edu/curriculum/classes/strm"

    ALLOWED_STRM_VALUES = ["1940 - 2025 Fall Term", "1930 - 2025 Summer Term 2", "1925 - 2025 Summer Term 1", "1910 - 2025 Spring Term"]
    ALLOWED_COURSE_VALUES = []

    TOOLS_SCHEMA = [
        {
            "type": "function",
            "name": "get_courses_list",
            "description": "Gets the list of courses and details in the format \{ 'crse_id', 'crse_offer_nbr', 'course_title_long', 'fall_and_or_spring' \} for the AI MEng program",
            "parameters": {}
        }, 
        {
            "type": "function",
            "name": "get_course_details",
            "description": "Retrieves course details and instructor(s) for a given course.",
            "parameters": {
                "type": "object",
                "properties": {
                    "strm": {
                        "type": "string",
                        "enum": ALLOWED_STRM_VALUES,
                        "description": f"The term in question : Fall, Spring, Summer 1 or Summer 2"
                    },
                    "crse_id": {
                        "type": "string",
                        "description": "Units the temperature will be returned in."
                    },
                    "crse_offer_nbr": {
                        "type": "string",
                        "description": "Course offering nbr of the course"
                    }
                },
                "required": [
                    "strm",
                    "crse_id",
                    "crse_offer_nbr"
                ],
                "additionalProperties": False
            },
            "strict": True
        },
        {
            "type": "function",
            "name": "get_courses_list_alternate",
            "description": "Alternate API to get the list of courses for the AI MEng program. Only returns headers",
            "parameters": {}
        },
        {
            "type": "function",
            "name": "get_course_details_alternate",
            "description": "Fallback fn to get course details. get_courses_list_alternate must be called first",
            "parameters": {
                "type": "object",
                "properties": {
                    "course_name": {
                        "type": "string",
                        "enum": ALLOWED_COURSE_VALUES,
                        "description": f"Course name obtained. Must be one from course_list_alternate function"
                    }
                },
                "required": [
                    "course_name"
                ],
                "additionalProperties": False
            },
            "strict": True
        },
        {
            "type": "function",
            "name": "get_degree_details",
            "description": "Gets degree details for the AI MEng program. Includes details about 12, 16 month plans, 4+1 BSE, and MD + MEng dual degree",
            "parameters": {}
        },
        ]

    @classmethod
    def get_courses_list(cls):
        response = requests.get(cls.courses_url, params = cls.__params)
        json_output = response.json()

        course_summary = json_output \
            .get("ssr_get_courses_resp", {}) \
            .get("course_search_result", {}) \
            .get("subjects", {}) \
            .get("subject", {}) \
            .get("course_summaries", {}) \
            .get("course_summary", {})

        """
        course summary is an array = [
        {
            "crse_id": "027568",
            "crse_id_lov_descr": null,
            "effdt": "2021-08-15",
            "crse_offer_nbr": "1",
            "institution": "DUKEU",
            "institution_lov_descr": "Duke University",
            "subject": "AIPI",
            "subject_lov_descr": "AI for Product Innovation",
            "catalog_nbr": " 501",
            "course_title_long": "AIPI Seminar",
            "ssr_crse_typoff_cd": "FALL-SPRNG",
            "ssr_crse_typoff_cd_lov_descr": "Fall and/or Spring",
            "msg_text": null,
            "multi_off": "N",
            "crs_topic_id": "0",
            "course_off_summaries": null
        }]
        """

        def filter_keys(dicts, keys_to_keep):
            filtered_dicts = [
                {k: d.get(k) for k in keys_to_keep}
                for d in dicts
            ]
            return filtered_dicts


        imp_keys = {"crse_id", "course_title_long", "crse_offer_nbr", "ssr_crse_typoff_cd_lov_descr"}

        filtered_dicts = filter_keys(course_summary, imp_keys)
        return filtered_dicts
    
    @classmethod
    def get_course_details(cls, *, strm, crse_id, crse_offer_nbr):
        if strm not in cls.ALLOWED_STRM_VALUES:
            print(f"Strm : {strm} is not supported!")
            return []
        encoded_strm = urllib.parse.quote(strm)
        base_url = cls.course_details_url + f"/{encoded_strm}/crse_id/{crse_id}"
        total_params = {**cls.__params, "crse_offer_nbr": crse_offer_nbr}
        response = requests.get(base_url, params = total_params)
        json_output = response.json()
        class_description = json_output \
            .get("ssr_get_classes_resp", {}) \
            .get("search_result", {}) \
            .get("subjects", {}) \
            .get("subject", {}) \
            .get("classes_summary", {}) \
            .get("class_summary", {})
        
        if isinstance(class_description, dict):
            class_description = class_description.get("ssr_descrlong", " ")
        elif isinstance(class_description, list):
            descriptions = set()
            for cls_descr in class_description:
                descriptions.add(cls_descr.get("ssr_descrlong", " "))
            class_description = " ".join(descriptions)
        else:
            raise TypeError("Unknown type of class description!")

        course_instructors = json_output \
            .get("ssr_get_classes_resp", {}) \
            .get("search_result", {}) \
            .get("subjects", {}) \
            .get("subject", {}) \
            .get("classes_summary", {}) \
            .get("class_summary", {}) 
        if isinstance(course_instructors, dict):
            course_instructors = course_instructors \
                .get("classes_meeting_patterns", {}) \
                .get("class_meeting_pattern", {}) \
                .get("class_instructors", {})
            
            instructors = []
            for v in course_instructors.values():
                instructors.append(v.get("name_display"))
        elif isinstance(course_instructors, list):
            instructors = set()
            for instr in course_instructors:
                cls_instructors = instr \
                            .get("classes_meeting_patterns", {}) \
                            .get("class_meeting_pattern", {}) \
                            .get("class_instructors", {})
                for v in cls_instructors.values():
                    instructors.add(v.get("name_display"))
                    
            instructors = list(instructors)
        else:
            raise TypeError("Unknown type of class description!")
        return {"Class description": class_description, "Instructors": instructors}

    degree_details_url = "https://masters.pratt.duke.edu/ai/degree"

    @classmethod
    def get_degree_details(cls):
        response = requests.get(cls.degree_details_url)
        soup = BeautifulSoup(response.text, 'lxml')
        subpage = soup.find("h2", id="h-flexibility-and-options").find_parent("section")
        subpage_text = subpage.text.strip()
        return subpage_text
    
    course_list_alternate_url = "https://masters.pratt.duke.edu/ai/courses/"
    
    
    @classmethod
    def get_courses_list_alternate(cls):
        """
        Fallback fn to get list of courses if not available in previous list of events
        """
        response = requests.get(cls.course_list_alternate_url)
        soup = BeautifulSoup(response.text, 'lxml')
        headers = soup.find_all('h3', class_ ="title--small")
        courses = [header.text for header in headers]
        cls.ALLOWED_COURSE_VALUES = courses
        return courses
    
    @classmethod
    def get_course_details_alternate(cls, course_name):
        """
        Fallback fn to get course details. get_courses_list_alternate must be called first
        """
        if course_name not in cls.ALLOWED_COURSE_VALUES:
            print(f"Course {course_name} not allowed!")
            return " "
        response = requests.get(cls.course_list_alternate_url)
        soup = BeautifulSoup(response.text, 'lxml')
        target = soup.find('h3', string = course_name)
        return target.find_parent("li").text.strip()

    @classmethod
    def get_tool_map(cls):
        TOOLS_MAP = {
            "get_courses_list": cls.get_courses_list,
            "get_course_details": cls.get_course_details,
            "get_degree_details": cls.get_degree_details,
            "get_courses_list_alternate": cls.get_courses_list_alternate,
            "get_course_details_alternate": cls.get_course_details_alternate
        }
        return TOOLS_MAP

if __name__ == "__main__":
    response = AIMEngTools.get_courses_list()
    args = {
        "strm":"1940 - 2025 Fall Term",
        "crse_id":"027038",
        "crse_offer_nbr":"1"
    }
    # response = AIMEngTools.get_course_details(**args)
    # response = AIMEngTools.get_courses_list_alternate()
    # response = AIMEngTools.get_course_details_alternate("AIPI 520: Modeling Process & Algorithms")
    print("Response obtained :", response)