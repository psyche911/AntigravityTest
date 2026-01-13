# Tourism Planning Agent - Google ADK with Mistral AI

A multi-agent tourism planning system built with **Google Agent Development Kit (ADK)** and powered by **Mistral Large 3** model.

## Overview

This project is a refactored version of an AutoGen-based tourism planning agent, redesigned to use the Google ADK framework. The agent team works collaboratively to create comprehensive travel plans.

### Agent Team

The system consists of 4 specialized agents working in sequence:

| Agent | Role | Description |
|-------|------|-------------|
| **Planner Agent** | Trip Planning | Creates initial travel plans with itineraries, attractions, and logistics |
| **Local Agent** | Local Expert | Adds authentic local experiences, hidden gems, and cultural tips |
| **Language Agent** | Communication | Provides language tips, essential phrases, and cultural communication advice |
| **Travel Summary Agent** | Consolidation | Integrates all suggestions into a comprehensive final travel plan |

### Architecture

- **Framework**: Google Agent Development Kit (ADK)
- **LLM**: Mistral Large 3 (via LiteLLM)
- **Orchestration**: SequentialAgent (equivalent to AutoGen's RoundRobinGroupChat)
- **UI**: Official Google ADK Web Interface

## Prerequisites

- Python 3.11 or higher
- Mistral AI API key ([Get one here](https://console.mistral.ai/))

## Installation

### 1. Clone/Navigate to the project directory

```bash
cd /path/to/AntigravityTest
```

### 2. Create and activate a virtual environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate on macOS/Linux
source venv/bin/activate

# Activate on Windows
# venv\Scripts\activate
```

### 3. Install dependencies

```bash
python3 -m pip install -r requirements.txt
```

### 4. Configure your API key

Edit the `.env` file in the `travel_agent/` directory:

```bash
# travel_agent/.env
MISTRAL_API_KEY="your_actual_mistral_api_key_here"
```

## Usage

### Option 1: Run with ADK Web Interface (Recommended)

The ADK provides a web-based UI for interacting with agents:

```bash
# Run from the project root (parent of travel_agent/)
adk web --port 8000
```

Then open your browser and navigate to: **http://localhost:8000**

Select `travel_agent` from the agent dropdown and start chatting!

### Option 2: Run with Command Line Interface

```bash
# Run from the project root
adk run travel_agent
```

### Example Prompts

Try these prompts to test the agent:

- "Plan a 3 day trip to Nepal."
- "I want to visit Tokyo for 5 days on a budget."
- "Create a romantic 7-day itinerary for Paris and the French Riviera."
- "Plan a 4-day adventure trip to Costa Rica with hiking and wildlife."

## Project Structure

```
AntigravityTest/
├── travel_agent/
│   ├── __init__.py      # Package initialization
│   ├── agent.py         # Main agent definitions (root_agent)
│   └── .env             # Mistral API key configuration
├── requirements.txt     # Python dependencies
├── README.md           # This file
└── venv/               # Virtual environment (after setup)
```

## How It Works

1. **User Input**: You provide a travel planning request (e.g., "Plan a 3 day trip to Nepal")

2. **Sequential Processing**: The SequentialAgent orchestrates the workflow:
   - **Step 1**: Planner Agent creates an initial travel plan
   - **Step 2**: Local Agent enhances with authentic experiences
   - **Step 3**: Language Agent adds communication tips
   - **Step 4**: Summary Agent consolidates everything

3. **State Sharing**: Each agent stores its output in the session state using `output_key`, allowing subsequent agents to access previous suggestions.

4. **Final Output**: The Travel Summary Agent produces a comprehensive, well-organized travel plan and signals completion with "TERMINATE".

## Comparison with Original AutoGen Code

| Feature | AutoGen (Original) | Google ADK (Refactored) |
|---------|-------------------|------------------------|
| Framework | AutoGen AgentChat | Google ADK |
| Orchestration | RoundRobinGroupChat | SequentialAgent |
| Termination | TextMentionTermination("TERMINATE") | Agent instruction includes "TERMINATE" |
| State Passing | Via conversation history | Via session state (output_key) |
| LLM | OpenAI GPT-4o | Mistral Large 3 |
| UI | Console | ADK Web Interface |

## Troubleshooting

### "MISTRAL_API_KEY not found"
Make sure your `.env` file in `travel_agent/` contains the correct API key.

### "Module not found" errors
Ensure you've activated the virtual environment and installed dependencies:
```bash
source venv/bin/activate
python3 -m pip install -r requirements.txt
```

### ADK Web not loading agents
Run `adk web` from the project root directory (the parent of `travel_agent/`), not from inside the agent folder.

## Resources

- [Google ADK Documentation](https://google.github.io/adk-docs/)
- [Mistral AI API Docs](https://docs.mistral.ai/)
- [LiteLLM Mistral Provider](https://docs.litellm.ai/docs/providers/mistral)

## License

MIT License
