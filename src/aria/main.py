# #!/usr/bin/env python
# import sys
# import warnings

# from datetime import datetime

# from crew import Aria


# warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# # This main file is intended to be a way for you to run your
# # crew locally, so refrain from adding unnecessary logic into this file.
# # Replace with inputs you want to test with, it will automatically
# # interpolate any tasks and agents information

# def run():
#     """
#     Run the crew.
#     """
#     inputs = {
#         'topic': 'AI LLMs',
#         'current_year': str(datetime.now().year)
#     }
    
#     try:
#         Aria().crew().kickoff(inputs=inputs)
#     except Exception as e:
#         raise Exception(f"An error occurred while running the crew: {e}")


# def train():
#     """
#     Train the crew for a given number of iterations.
#     """
#     inputs = {
#         "topic": "AI LLMs",
#         'current_year': str(datetime.now().year)
#     }
#     try:
#         Aria().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

#     except Exception as e:
#         raise Exception(f"An error occurred while training the crew: {e}")

# def replay():
#     """
#     Replay the crew execution from a specific task.
#     """
#     try:
#         Aria().crew().replay(task_id=sys.argv[1])

#     except Exception as e:
#         raise Exception(f"An error occurred while replaying the crew: {e}")

# def test():
#     """
#     Test the crew execution and returns the results.
#     """
#     inputs = {
#         "topic": "AI LLMs",
#         "current_year": str(datetime.now().year)
#     }
    
#     try:
#         Aria().crew().test(n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs)

#     except Exception as e:
#         raise Exception(f"An error occurred while testing the crew: {e}")
#!/usr/bin/env python

# import sys
# import warnings
# from datetime import datetime

# from crew import Aria
# warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# def run():
#     """Run the crew."""
#     inputs = {
#         "topic": "AI LLMs",
#         "current_year": str(datetime.now().year)
#     }
#     try:
#         Aria().crew().kickoff(inputs=inputs)

#         print("✅ Crew finished! Check for output files (report.md, reviewed_report.md).")
#     except Exception as e:
#         print(f"❌ Error occurred: {e}")
#         raise

# if __name__ == "__main__":
#     run()
import warnings
from datetime import datetime
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from aria.crew import Aria

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

app = FastAPI(title="ARIA Crew API")

class CrewInput(BaseModel):
    topic: str

@app.post("/run-crew")
def run_crew(input_data: CrewInput):
    """
    Run the ARIA crew for a given topic.
    """
    inputs = {
        "topic": input_data.topic,
        "current_year": str(datetime.now().year),
        "output_path": "/app/output"
    }
    try:
        Aria().crew().kickoff(inputs=inputs)
        return {"status": "success", "message": "Crew finished! Check for output files (report.md, reviewed_report.md)."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error occurred: {e}")

@app.get("/")
def root():
    return {"message": "Send a POST request to /run-crew with JSON: {'topic': 'Your topic here'}"}

    
# #!/usr/bin/env python
# import sys
# import warnings
# from datetime import datetime
# from dotenv import load_dotenv
# import os

# from aria.crew import Aria

# warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# # Load environment variables
# load_dotenv()

# def run():
#     """
#     Run the crew for the research workflow.
#     """
#     inputs = {
#         'topic': 'AI LLMs',
#         'current_year': str(datetime.now().year)
#     }
    
#     try:
#         crew_instance = Aria().crew()
#         print("🚀 Starting ARIA Crew...")
#         crew_instance.kickoff(inputs=inputs)
#         print("✅ Crew finished execution.")
#     except Exception as e:
#         print(f"❌ Error occurred: {e}")

# def train():
#     """
#     Train the crew for a given number of iterations.
#     Usage: python main.py train <iterations> <filename>
#     """
#     if len(sys.argv) < 3:
#         print("Usage: python main.py train <iterations> <filename>")
#         return

#     iterations = int(sys.argv[2])
#     filename = sys.argv[3]

#     inputs = {
#         "topic": "AI LLMs",
#         'current_year': str(datetime.now().year)
#     }
#     try:
#         Aria().crew().train(n_iterations=iterations, filename=filename, inputs=inputs)
#         print("✅ Crew training completed.")
#     except Exception as e:
#         print(f"❌ Error occurred during training: {e}")

# def replay():
#     """
#     Replay the crew execution from a specific task.
#     Usage: python main.py replay <task_id>
#     """
#     if len(sys.argv) < 3:
#         print("Usage: python main.py replay <task_id>")
#         return

#     task_id = sys.argv[2]
#     try:
#         Aria().crew().replay(task_id=task_id)
#         print("✅ Crew replay finished.")
#     except Exception as e:
#         print(f"❌ Error occurred during replay: {e}")

# def test():
#     """
#     Test the crew execution and return the results.
#     Usage: python main.py test <n_iterations> <eval_llm>
#     """
#     if len(sys.argv) < 4:
#         print("Usage: python main.py test <n_iterations> <eval_llm>")
#         return

#     n_iterations = int(sys.argv[2])
#     eval_llm = sys.argv[3]

#     inputs = {
#         "topic": "AI LLMs",
#         "current_year": str(datetime.now().year)
#     }
    
#     try:
#         Aria().crew().test(n_iterations=n_iterations, eval_llm=eval_llm, inputs=inputs)
#         print("✅ Crew testing finished.")
#     except Exception as e:
#         print(f"❌ Error occurred during testing: {e}")

# if __name__ == "__main__":
#     if len(sys.argv) < 2:
#         # Default: just run
#         run()
#     else:
#         command = sys.argv[1].lower()
#         if command == "train":
#             train()
#         elif command == "replay":
#             replay()
#         elif command == "test":
#             test()
#         else:
#             print(f"Unknown command '{command}'. Available commands: run, train, replay, test")
