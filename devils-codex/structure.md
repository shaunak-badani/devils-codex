# Devils Codex Project Structure

```
agent/
├── .env                      # Environment variables
├── .gitignore                # Git ignore file
├── README.md                 # Project documentation
├── requirements.txt          # Dependencies
├── app/
│   ├── __init__.py
│   ├── main.py               # FastAPI entry point
│   ├── config.py             # Configuration settings
│   ├── agent/
│   │   ├── __init__.py
│   │   ├── agent.py          # Main agent implementation with LangGraph
│   │   ├── memory.py         # Conversation memory
│   │   └── prompts.py        # System prompts for the agent
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── base.py           # Base tool interface
│   │   ├── ai_meng_tool.py   # AI MEng program information tool
│   │   ├── events_tool.py    # Campus events tool
│   │   ├── prospective_tool.py # Prospective student info tool
│   │   └── web_search_tool.py  # Web search fallback tool
│   ├── data/
│   │   ├── __init__.py
│   │   ├── loader.py         # Data loaders for different sources
│   │   ├── vectorstore.py    # Vector database implementation
│   │   └── scrapers/         # Web scrapers for Duke sites
│   │       ├── __init__.py
│   │       ├── ai_meng.py    # Scraper for AI MEng program
│   │       ├── events.py     # Scraper for events
│   │       └── prospective.py # Scraper for prospective students
│   ├── eval/
│   │   ├── __init__.py
│   │   ├── evaluator.py      # Evaluation framework
│   │   └── test_cases.py     # Test cases for evaluation
│   ├── ui/
│   │   ├── __init__.py
│   │   ├── pages/            # Streamlit pages
│   │   │   ├── __init__.py
│   │   │   ├── main.py       # Main chat interface
│   │   │   └── about.py      # About page
│   │   └── components/       # UI components
│   │       ├── __init__.py
│   │       ├── chat.py       # Chat component
│   │       └── sidebar.py    # Sidebar component
│   └── utils/
│       ├── __init__.py
│       └── helpers.py        # Utility functions
├── data/
│   ├── raw/                  # Raw data storage
│   ├── processed/            # Processed data
│   └── embeddings/           # Vector embeddings
└── tests/
    ├── __init__.py
    ├── test_agent.py         # Tests for agent
    ├── test_tools.py         # Tests for tools
    └── test_evaluation.py    # Tests for evaluation
```
