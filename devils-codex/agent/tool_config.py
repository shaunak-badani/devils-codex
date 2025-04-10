import requests

class Weather:

    @staticmethod
    def get_weather(latitude, longitude):
        response = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m")
        data = response.json()
        return data['current']

class Tools:
    
    _tools = [{
        "type": "function",
        "name": "get_weather",
        "description": "Get current temperature for a given location.",
        "parameters": {
            "type": "object",
            "properties": {
                "latitude": {"type": "number"},
                "longitude": {"type": "number"}
            },
            "required": ["latitude", "longitude"],
            "additionalProperties": False
        }
    }]

    _tool_map = {
        "get_weather": Weather.get_weather
    }

    @staticmethod
    def get_tools():
        return Tools._tools
    
    @staticmethod
    def call_function(name, args):
        return Tools._tool_map[name](*args)
