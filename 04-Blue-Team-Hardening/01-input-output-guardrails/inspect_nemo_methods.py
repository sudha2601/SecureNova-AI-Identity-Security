import inspect
import os
from pathlib import Path
from dotenv import load_dotenv
from nemoguardrails import RailsConfig, LLMRails

TASK = Path(__file__).resolve().parent
ROOT = TASK.parents[1]
load_dotenv(ROOT / ".env")

rails = LLMRails(RailsConfig.from_path(str(TASK / "config")))

print("=== GENERATE ASYNC SOURCE ===")
print(inspect.getsource(rails.generate_async))

print("\n=== RUNTIME PROCESS EVENTS SOURCE ===")
print(inspect.getsource(rails.runtime.process_events))
