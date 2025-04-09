import requests
import xml.etree.ElementTree as ET
from datetime import datetime

class EventsTool:
    def __init__(self):
        self.feed_url = "https://calendar.duke.edu/events/index.xml?&future_days=45&feed_type=simple"

    def run(self, query: str) -> str:
        try:
            response = requests.get(self.feed_url)
            response.raise_for_status()

            root = ET.fromstring(response.content)

            events = []
            for item in root.findall(".//item"):
                title = item.find("title").text
                pub_date = item.find("pubDate").text

                # Convert pubDate to readable format
                try:
                    date_obj = datetime.strptime(pub_date, "%a, %d %b %Y %H:%M:%S %Z")
                    formatted_date = date_obj.strftime("%B %d, %Y %I:%M %p")
                except Exception:
                    formatted_date = pub_date

                events.append(f"{formatted_date} — {title}")

            if not events:
                return "No upcoming events found in the next 45 days."

            # Limit the output to 5–10 events for brevity
            top_events = "\n".join(events[:10])
            return f"Here are some upcoming events on campus:\n\n{top_events}"

        except Exception as e:
            return f"Error retrieving events: {str(e)}"
