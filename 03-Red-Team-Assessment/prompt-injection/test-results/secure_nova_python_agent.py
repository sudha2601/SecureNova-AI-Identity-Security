import json
from pathlib import Path
from datetime import datetime, timezone

BASE = Path(__file__).resolve().parents[1]

TOKEN_FILE = BASE / "fake-jwt" / "test-token.json"
DOCUMENTS_FOLDER = BASE / "malicious-documents"

OUTPUT_FILE = Path(__file__).resolve().parent / "python-agent-results.json"


def load_synthetic_identity():
    data = json.loads(TOKEN_FILE.read_text(encoding="utf-8"))

    token = data.get("synthetic_jwt")

    if not token:
        raise ValueError("Synthetic JWT not found")

    return token


def retrieve_documents():
    documents = sorted(DOCUMENTS_FOLDER.glob("document-*.txt"))

    if not documents:
        raise FileNotFoundError("No malicious documents found")

    return documents


def vulnerable_agent(document_text, synthetic_token):
    """
    Deliberately vulnerable simulation.

    This deterministic test represents an agent that incorrectly
    executes an instruction embedded in an untrusted document.
    It does not execute external commands or contact real services.
    """

    instruction = document_text.lower()

    if any(word in instruction for word in [
        "credential",
        "token",
        "exfiltrate",
        "identity"
    ]):
        return (
            "VULNERABLE AGENT RESPONSE:\n"
            "The document requested identity credential disclosure.\n"
            "Synthetic test credential: " + synthetic_token
        )

    return "Document processed without credential disclosure."


def hardened_agent(document_text):
    """
    Hardened simulation.

    Retrieved documents are treated as untrusted data.
    Instructions requesting credential disclosure are not executed.
    """

    return (
        "HARDENED AGENT RESPONSE:\n"
        "The retrieved document contains untrusted instructions.\n"
        "Credential disclosure request rejected."
    )


def main():
    synthetic_token = load_synthetic_identity()
    documents = retrieve_documents()

    results = []

    print("=" * 65)
    print("SECURENOVA PYTHON AGENT")
    print("Controlled indirect prompt-injection simulation")
    print("=" * 65)

    for document in documents:
        payload = document.read_text(encoding="utf-8")

        vulnerable_response = vulnerable_agent(
            payload,
            synthetic_token
        )

        hardened_response = hardened_agent(payload)

        exposed = synthetic_token in vulnerable_response

        print("\nDocument:", document.name)
        print("-" * 65)
        print("Original malicious payload:")
        print(payload)

        print("\nVulnerable agent:")
        print(vulnerable_response)

        print("\nHardened agent:")
        print(hardened_response)

        print("\nVulnerable agent exposed synthetic credential:", exposed)

        results.append({
            "document": document.name,
            "payload": payload,
            "vulnerable_agent_response": vulnerable_response,
            "hardened_agent_response": hardened_response,
            "synthetic_credential_exposed": exposed,
            "vulnerable_agent_result": "EXPOSED" if exposed else "BLOCKED",
            "hardened_agent_result": "BLOCKED"
        })

    report = {
        "experiment": "Controlled Python agent simulation",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "credential_type": "Synthetic test fixture",
        "results": results
    }

    OUTPUT_FILE.write_text(
        json.dumps(report, indent=4),
        encoding="utf-8"
    )

    print("\n" + "=" * 65)
    print("EXPERIMENT SUMMARY")
    print("=" * 65)

    print("Documents tested:", len(results))
    print(
        "Synthetic credential exposures:",
        sum(r["synthetic_credential_exposed"] for r in results)
    )
    print("Hardened agent blocks:", len(results))
    print("\nReport saved to:", OUTPUT_FILE)


if __name__ == "__main__":
    main()
