import requests

class EventTools:

    base_url = "https://calendar.duke.edu/events/index.json"

    ALLOWED_CATEGORIES = [
        "Academic Calendar Dates",
        "Artificial Intelligence",
        "Brown Bag",
        "Centennial",
        "Charity/Fundraising",
        "Concert/Music"
    ]

    TOOLS_SCHEMA = [
    {
        "type": "function",
        "name": "get_events",
        "description": "Get list of events occuring at Duke.",
        "parameters": {
            "type": "object",
            "properties": {
                "categories": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "enum": ALLOWED_CATEGORIES
                    },
                    "description": "List of categories to filter by"
                },
                "future_days": {
                    "type": "integer",
                    "description": "Number of days in the future to filter events for."
                },
                "local": {
                    "type": "boolean",
                    "description": "Whether to restrict events to local or not."
                }
            }
        }
    }]

    @classmethod
    def get_events(cls, *, categories, future_days, local):
        params = {
            "cfu[]": categories,
            "future_days": future_days,
            "feed_type": "simple"
        }
        if local:
            params["local"] = "true"
        response = requests.get(cls.base_url, params = params)
        json_output = response.json()
        events = []
        for event in json_output.get('events', []):
            events.append({
                "start": event.get("start_timestamp", ""),
                "summary": event.get("summary", ""),
                "location": event.get("location", {}).get("address", "")
            })
        return events
    
    @classmethod
    def get_tool_map(cls):
        TOOLS_MAP = {
            "get_events": cls.get_events
        }
        return TOOLS_MAP


if __name__ == "__main__":
    response = EventTools.get_events(categories=["Brown Bag"], future_days = 33, local = True)
    print(response)