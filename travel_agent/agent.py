"""
Tourism Planning Agent - Google ADK Implementation

This agent is refactored from an AutoGen-based tourism planning agent to use
the Google Agent Development Kit (ADK) framework with Mistral AI (via LiteLLM).

The agent team consists of:
1. Planner Agent - Creates initial travel plans based on user requests
2. Local Agent - Suggests authentic local activities and places to visit
3. Language Agent - Provides language/communication tips for the destination
4. Travel Summary Agent - Consolidates all suggestions into a final comprehensive plan

Architecture:
- Uses SequentialAgent to orchestrate the workflow (equivalent to AutoGen's RoundRobinGroupChat)
- Each sub-agent processes the request in sequence, passing context via session state
- Powered by Mistral Large 3 model via LiteLLM integration
"""

from google.adk.agents import LlmAgent, SequentialAgent
from google.adk.models.lite_llm import LiteLlm

# Define the Mistral Large 3 model via LiteLLM
# The model string format for Mistral via LiteLLM is: "mistral/{model_name}"
MISTRAL_MODEL = LiteLlm(model="mistral/mistral-large-latest")

# --- 1. Define the Planner Agent ---
# Responsible for creating the initial travel plan based on user request
planner_agent = LlmAgent(
    name="planner_agent",
    model=MISTRAL_MODEL,
    description="A helpful assistant that can plan trips.",
    instruction="""You are a helpful travel planning assistant. Your task is to suggest a comprehensive travel plan for the user based on their request.

When creating a travel plan, include:
- Suggested itinerary with day-by-day activities
- Recommended places to stay
- Key attractions and must-see destinations
- Best time to visit and weather considerations
- General travel tips for the destination

Be specific and practical in your suggestions. Consider the user's time constraints and provide a realistic schedule.

After providing your suggestions, clearly indicate that you are passing the plan to the local expert for authentic recommendations.""",
    output_key="planner_suggestions"  # Store output in session state
)

# --- 2. Define the Local Agent ---
# Provides authentic local activities and hidden gems
local_agent = LlmAgent(
    name="local_agent",
    model=MISTRAL_MODEL,
    description="A local assistant that can suggest authentic local activities or places to visit.",
    instruction="""You are a local expert assistant. Your task is to enhance the travel plan with authentic and interesting local activities, hidden gems, and places that tourists might miss.

Review the initial travel plan suggestions:
{planner_suggestions}

Based on this plan, add:
- Authentic local experiences and cultural activities
- Off-the-beaten-path destinations and hidden gems
- Local food recommendations and where to find authentic cuisine
- Local customs and etiquette tips
- Best times to visit specific attractions to avoid crowds
- Local transportation tips

Build upon the existing plan suggestions and provide additional local insights that will make the trip more memorable and authentic.

After providing your suggestions, indicate that you are passing the enhanced plan to the language specialist.""",
    output_key="local_suggestions"  # Store output in session state
)

# --- 3. Define the Language Agent ---
# Provides language and communication tips for the destination
language_agent = LlmAgent(
    name="language_agent",
    model=MISTRAL_MODEL,
    description="A helpful assistant that can provide language tips for a given destination.",
    instruction="""You are a language and communication specialist. Your task is to review the travel plan and provide essential language and communication tips for the destination.

Review the travel plan and local suggestions:
{planner_suggestions}

{local_suggestions}

Provide helpful information about:
- The primary language(s) spoken at the destination
- Essential phrases travelers should know (greetings, thank you, help, numbers, directions, etc.)
- Common communication challenges and how to overcome them
- Whether English is widely spoken
- Useful apps or tools for translation
- Cultural nuances in communication (body language, formal vs informal speech, etc.)
- Tips for interacting with locals who may not speak your language

If the existing plan already includes good language tips, acknowledge that and add any additional helpful information.

After your suggestions, indicate that you are passing everything to the summary agent for the final comprehensive plan.""",
    output_key="language_suggestions"  # Store output in session state
)

# --- 4. Define the Travel Summary Agent ---
# Consolidates all suggestions into a final comprehensive travel plan
travel_summary_agent = LlmAgent(
    name="travel_summary_agent",
    model=MISTRAL_MODEL,
    description="A helpful assistant that summarizes the complete travel plan.",
    instruction="""You are a travel plan consolidation specialist. Your task is to take all suggestions and advice from the previous agents and create a detailed, well-organized final travel plan.

Review all the information gathered:

**Planner Suggestions:**
{planner_suggestions}

**Local Expert Insights:**
{local_suggestions}

**Language & Communication Tips:**
{language_suggestions}

Create a comprehensive, integrated final travel plan that includes:

1. **Trip Overview**
   - Destination summary
   - Best time to visit
   - Duration and key highlights

2. **Day-by-Day Itinerary**
   - Detailed daily schedule
   - Mix of popular attractions and hidden gems
   - Recommended timings and logistics

3. **Accommodation Recommendations**
   - Where to stay
   - Areas/neighborhoods to consider

4. **Local Experiences & Food**
   - Authentic activities
   - Must-try local dishes and where to find them
   - Cultural experiences

5. **Practical Information**
   - Language tips and essential phrases
   - Local customs and etiquette
   - Transportation advice
   - Safety tips

6. **Budget Considerations**
   - Estimated costs where applicable
   - Money-saving tips

Ensure the final plan is:
- Well-organized and easy to follow
- Practical and actionable
- Complete with all perspectives integrated

End your response with "TERMINATE" to indicate the plan is complete.""",
    output_key="final_travel_plan"  # Store the final plan
)

# --- 5. Create the Sequential Agent (Travel Planning Pipeline) ---
# This orchestrates the agents in sequence, similar to AutoGen's RoundRobinGroupChat
travel_pipeline = SequentialAgent(
    name="travel_planning_pipeline",
    description="Executes a comprehensive travel planning workflow through a team of specialized agents.",
    sub_agents=[
        planner_agent,
        local_agent,
        language_agent,
        travel_summary_agent
    ]
    # Agents run in order: Planner -> Local -> Language -> Summary
)

# For ADK compatibility, the root agent must be named `root_agent`
root_agent = travel_pipeline
