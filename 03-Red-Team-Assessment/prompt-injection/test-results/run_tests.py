from pathlib import Path
import json
from datetime import datetime

BASE = Path(__file__).resolve().parent.parent
DOCS = BASE / "malicious-documents"

tests = [
    ("PI-01", "System prompt extraction",
     ["system prompt", "hidden system prompt"]),
    ("PI-02", "Credential extraction",
     ["api keys", "passwords", "credentials"]),
    ("PI-03", "Unauthorized customer data access",
     ["customer database", "customer records", "authorization checks"])
]

results = []

for test_id, scenario, keywords in tests:
    matching_docs = []

    for document in DOCS.glob("document-*.txt"):
        content = document.read_text(encoding="utf-8").lower()

        if any(keyword in content for keyword in keywords):
            matching_docs.append(document.name)

    results.append({
        "test_id": test_id,
        "scenario": scenario,
        "detected_documents": matching_docs,
        "status": "DETECTED" if matching_docs else "NOT DETECTED"
    })

output = Path(__file__).resolve().parent / "prompt-injection-test-report.json"
output.write_text(json.dumps({
    "test_type": "Local keyword-based simulation",
    "generated_at": datetime.now().isoformat(timespec="seconds"),
    "results": results
}, indent=4), encoding="utf-8")

for result in results:
    print(f"{result['test_id']} - {result['scenario']}: {result['status']}")
    print(f"  Documents: {', '.join(result['detected_documents']) or 'None'}")

print(f"\nReport saved to: {output}")
print("\nNote: Detection only. This does not test an AI model.")
