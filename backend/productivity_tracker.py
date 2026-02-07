class ProductivityTracker:
    def __init__(self):
        self.stats = {
            "processed": 0,
            "time_saved_minutes": 0
        }

    def track_batch(self, count, avg_time_saved_per_email=2.0):
        """Track processing stats. Assume 2 mins saved per email."""
        self.stats["processed"] += count
        self.stats["time_saved_minutes"] += count * avg_time_saved_per_email
        
    def get_stats(self):
        return {
            "processed_total": self.stats["processed"],
            "time_saved_hours": round(self.stats["time_saved_minutes"] / 60, 1)
        }
