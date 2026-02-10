#!/usr/bin/env python
import sys
import warnings
from datetime import datetime

from market_research_crew.crew import MarketResearchCrew


warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


def run():
    """
    Run the crew locally.
    """
    company_domain = input("Enter company domain (e.g., salesforce.com): ").strip()

    # Inputs must match variables used in YAML, e.g. {company_domain}
    inputs = {
        "company_domain": company_domain,
        # keep only if your YAML uses {current_year}
        "current_year": str(datetime.now().year),
    }

    try:
        MarketResearchCrew().crew().kickoff(inputs=inputs)
        print("Done! Check output/market_research_report.md")
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


def train():
    """
    Train the crew for a given number of iterations.
    """
    company_domain = input("Enter company domain (e.g., salesforce.com): ").strip()

    inputs = {
        "company_domain": company_domain,
        "current_year": str(datetime.now().year),
    }

    try:
        MarketResearchCrew().crew().train(
            n_iterations=int(sys.argv[1]),
            filename=sys.argv[2],
            inputs=inputs
        )
    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")


def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        MarketResearchCrew().crew().replay(task_id=sys.argv[1])
    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")


def test():
    """
    Test the crew execution and returns the results.
    """
    company_domain = input("Enter company domain (e.g., salesforce.com): ").strip()

    inputs = {
        "company_domain": company_domain,
        "current_year": str(datetime.now().year),
    }

    try:
        MarketResearchCrew().crew().test(
            n_iterations=int(sys.argv[1]),
            eval_llm=sys.argv[2],
            inputs=inputs
        )
    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")


def run_with_trigger():
    """
    Run the crew with trigger payload.
    """
    import json

    if len(sys.argv) < 2:
        raise Exception("No trigger payload provided. Please provide JSON payload as argument.")

    try:
        trigger_payload = json.loads(sys.argv[1])
    except json.JSONDecodeError:
        raise Exception("Invalid JSON payload provided as argument")

    # If using triggers, allow payload to provide the domain; otherwise default to empty
    inputs = {
        "crewai_trigger_payload": trigger_payload,
        "company_domain": trigger_payload.get("company_domain", ""),
        "current_year": str(datetime.now().year),
    }

    try:
        result = MarketResearchCrew().crew().kickoff(inputs=inputs)
        return result
    except Exception as e:
        raise Exception(f"An error occurred while running the crew with trigger: {e}")

if __name__ == "__main__":
    run()
