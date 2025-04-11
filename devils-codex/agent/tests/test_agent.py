from ..agent import DukeAgent

agent = DukeAgent()
def test_get_courses_list():
    query = "Get me a list of courses offered for the AIPI program"
    response = agent.run(query)
    print(response)

    EXPECTED_COURSES = ["AIPI Seminar", "AIPI Workshops", "Python Bootcamp", "Introductory Residency", \
        "Mid-Program Residency", "Concluding Residency", "Sourcing Data for Analytics", \
        "Modeling Process and Algorithms", "Optimization in Practice", "Deep Reinforcement Learning Applications", \
        "Deep Reinforcement Learning Applications", "Deep Learning Applications", "Capstone Practicum 1",\
        "Legal, Societal, and Ethical Implications of AI", "Operationalizing AI", "Advanced Topics in AI for Product Innovation", \
        "Advanced Topics in AI for Products Innovation (with Lab)", "Special Readings in AI for Product Innovation"]

    for COURSE in EXPECTED_COURSES:
        assert COURSE in response


def test_course_information():
    query = "Who is the instructor for Modeling Processes and Algorithms"
    response = agent.run(query)

    EXPECTED_INSTRUCTOR = "Jon J Reifschneider"

    assert EXPECTED_INSTRUCTOR in response