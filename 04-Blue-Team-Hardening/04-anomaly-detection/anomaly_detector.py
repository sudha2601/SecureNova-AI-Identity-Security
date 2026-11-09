from collections import defaultdict, deque
from datetime import datetime, timedelta


class AnomalyDetector:
    def __init__(self):
        self.failed_logins = defaultdict(deque)
        self.tool_calls = defaultdict(deque)
        self.allowed_ips = {"192.168.1.10"}

    def check_failed_logins(self, user, timestamp):
        events = self.failed_logins[user]
        events.append(timestamp)

        while events and timestamp - events[0] > timedelta(minutes=5):
            events.popleft()

        if len(events) >= 5:
            return f"ALERT: Repeated failed logins for {user}"

        return "NORMAL: Failed login count within threshold"

    def check_tool_calls(self, agent, timestamp):
        events = self.tool_calls[agent]
        events.append(timestamp)

        while events and timestamp - events[0] > timedelta(minutes=1):
            events.popleft()

        if len(events) > 10:
            return f"ALERT: Unusual tool invocation spike by {agent}"

        return "NORMAL: Tool invocation rate within threshold"

    def check_ip(self, ip):
        if ip not in self.allowed_ips:
            return f"ALERT: Access from unexpected IP {ip}"

        return "NORMAL: Recognized IP address"


def run_tests():
    detector = AnomalyDetector()
    now = datetime.now()

    print("=== SecureNova Anomaly Detection Tests ===")

    print("\n1. Failed login detection")
    for i in range(5):
        result = detector.check_failed_logins(
            "agent-A", now + timedelta(seconds=i)
        )
    print(result)

    print("\n2. Tool invocation spike detection")
    for i in range(11):
        result = detector.check_tool_calls(
            "agent-A", now + timedelta(seconds=i)
        )
    print(result)

    print("\n3. Unexpected IP detection")
    print(detector.check_ip("203.0.113.50"))

    print("\n=== Test Summary ===")
    print("All three anomaly scenarios tested.")


if __name__ == "__main__":
    run_tests()
