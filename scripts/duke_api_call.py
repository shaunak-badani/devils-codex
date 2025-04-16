import requests
from dotenv import load_dotenv
import urllib.parse
import requests
import os
load_dotenv()

class AIMEngTools:
    __course_name = "AIPI - AI for Product Innovation"
    __encoded_course_name = urllib.parse.quote(__course_name)
    __params = {"access_token": os.environ.get("DUKE_API_KEY")}
    base_url = f"https://streamer.oit.duke.edu/curriculum/courses/subject/{__encoded_course_name}"

    TOOLS_SCHEMA = [{
        "type": "function",
        "name": "get_courses_list",
        "description": "Gets the list of courses for the AI MEng program",
        "parameters": {}
    }]

    @classmethod
    def get_courses_list(cls):
        response = requests.get(cls.base_url, params = cls.__params)
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


        imp_keys = {"crse_id", "course_title_long"}

        filtered_dicts = filter_keys(course_summary, imp_keys)
        return filtered_dicts



if __name__ == "__main__":
    response = AIMEngTools.get_courses_list()
    print(response)