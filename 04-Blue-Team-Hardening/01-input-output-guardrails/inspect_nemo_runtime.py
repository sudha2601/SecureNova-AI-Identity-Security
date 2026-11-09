import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from nemoguardrails import RailsConfig, LLMRails

TASK = Path(__file__).resolve().parent
ROOT = TASK.parents[1]

load_dotenv(ROOT / ".env")

config = RailsConfig.from_path(str(TASK / "config"))
rails = LLMRails(config)

print("=" * 60)
print("NEMO GUARDRAILS RUNTIME INSPECTION")
print("=" * 60)

import nemoguardrails
print("\nNeMo version:", nemoguardrails.__version__)

print("\nLLMRails methods:")
for name in dir(rails):
    if any(word in name.lower() for word in ("generate", "runtime", "llm")):
        print(name)

print("\nRuntime type:", type(rails.runtime))

print("\nRuntime methods:")
for name in dir(rails.runtime):
    if any(word in name.lower() for word in ("generate", "process", "flow", "action")):
        print(name)

print("\nLLM type:", type(rails.llm))

print("\nLLM methods:")
for name in dir(rails.llm):
    if any(word in name.lower() for word in ("generate", "invoke", "call")):
        print(name)

print("=" * 60)
