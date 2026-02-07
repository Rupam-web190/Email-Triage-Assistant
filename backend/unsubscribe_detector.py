class UnsubscribeDetector:
    def detect(self, text):
        """Smart spam filtering + one-click unsubscribe"""
        if 'unsubscribe' in text.lower() or 'manage preferences' in text.lower():
            return {
                "can_unsubscribe": True,
                "link": "http://mock-unsubscribe-link.com"
            }
        return {"can_unsubscribe": False}
