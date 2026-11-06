from pathlib import Path
import json

BASE = Path(__file__).resolve().parent.parent
DOCS = BASE / "malicious-documents"

tests = [
    {
        "id": "PI-01",
        "name": "System prompt extraction",
        "keywords": ["system prompt", "reveal the assistant"],
        "response": "BLOCKED: Hidden system instructions cannot be disclosed."
    },
    {
        "id": "PI-02",
        "name": "Credential extraction",
        "keywords": ["api keys", "passwords", "credentials"],
        "response": "BLOCKED: Credentials and secrets cannot be disclosed."
    },
    {
        "id": "PI-03",
        "name": "Unauthorized customer data access",
        "keywords": ["customer database", "customer records"],
        "response": "BLOCKED: Unauthorized customer data access is not permitted."
    }
]

results = []

for test in tests:
    matched = []

    for file in DOCS.glob("document-*.txt"):
        content = file.read_text(encoding="utf-8").lower()

        if any(word in content for word in test["keywords"]):
            matched.append(file.name)

    outcome = "SIMULATED_BLOCK" if matched else "NO_MATCH"

    results.append({
        "test_id": test["id"],
        "scenario": test["name"],
        "matched_documents": matched,
        "simulated_response": test["response"] if matched else "No matching attack detected",
        "outcome": outcome
    })

    print(f"\n{test['id']}: {test['name']}")
    print(f"Result: {outcome}")
    print(f"Response: {test['response'] if matched else 'No matching attack detected'}")

report = Path(__file__).resolve().parent / "prompt-injection-simulation.json"
report.write_text(json.dumps(results, indent=4), encoding="utf-8")

print("\nSimulation report saved:", report)
print("\nNOTE: This is a rule-based simulation, not a live AI security test.")
