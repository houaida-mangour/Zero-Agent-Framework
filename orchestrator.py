# orchestrator.py
import json
from config import client, AZURE_DEPLOYMENT_NAME
from prompts import ORCHESTRATOR_SYSTEM_PROMPT

def orchestrator_agent(user_task: str):
    """
    This function takes a task, asks the AI for a plan, and returns the plan.
    """
    print(f"Planning how to: '{user_task}'")

    # Talk to the AI
    response = client.chat.completions.create(
        model=AZURE_DEPLOYMENT_NAME,
        messages=[
            {"role": "system", "content": ORCHESTRATOR_SYSTEM_PROMPT},
            {"role": "user", "content": user_task}
        ],
        temperature=0.1  # Makes the AI more focused and less creative
    )

    # Get the AI's text response
    plan_text = response.choices[0].message.content
    print("Raw AI Response:\n", plan_text)

    # Try to clean the response and find the JSON part
    if "```json" in plan_text:
        plan_text = plan_text.split("```json")[1].split("```")[0].strip()
    elif "```" in plan_text:
        plan_text = plan_text.split("```")[1].split("```")[0].strip()

    # Convert the JSON text into a Python list
    try:
        plan = json.loads(plan_text)
        print(f"Success! Parsed a plan with {len(plan)} steps.")
        return plan
    except json.JSONDecodeError:
        print("Failed to understand the AI's plan. It didn't give valid JSON.")
        return []

# This part only runs if you run this file directly, e.g., `python orchestrator.py`
if __name__ == "__main__":
    test_task = "Find all my screenshots and organize them by month."
    plan = orchestrator_agent(test_task)
    for step in plan:
        print(f"Step {step['step']}: {step['agent']} -> {step['input']}")