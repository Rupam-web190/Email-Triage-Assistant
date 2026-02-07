class AnalyticsEngine:
    def get_trends(self):
        """30-day trends, top senders, response time metrics"""
        return {
            "weekly_volume": [45, 52, 38, 65, 42],
            "top_senders": [
                {"email": "boss@company.com", "count": 15},
                {"email": "client@corp.com", "count": 12},
                {"email": "jira@atlassian.com", "count": 45}
            ],
            "response_times": {
                "urgent": "15m",
                "normal": "2h",
                "low": "1d"
            }
        }
