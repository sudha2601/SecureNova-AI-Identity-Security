# Prompt Injection Assessment – Results

## Objective
Evaluate three malicious document scenarios using local keyword-based detection and rule-based response simulation.

## Test Results

| Test ID | Attack Scenario | Detection | Simulated Response |
|---|---|---|---|
| PI-01 | System prompt extraction | Detected | Blocked |
| PI-02 | Credential extraction | Detected | Blocked |
| PI-03 | Unauthorized customer data access | Detected | Blocked |

## Summary
- Total test scenarios: 3
- Suspicious inputs detected: 3
- Simulated blocking responses: 3

## Methodology
The Python detection script searches for predefined keywords in the malicious documents. A separate simulation script generates predefined blocking responses when matching content is found.

## Limitation
This assessment is a local rule-based simulation. It does not test a live AI model, actual authentication, tool execution, or real access-control enforcement.

## Conclusion
All three prepared malicious inputs were detected by the keyword-based checks, and all three generated simulated blocking responses.
