class ThreadRanker:
    def rank_threads(self, threads):
        """Sort threads by priority (descending) then date"""
        # Assuming threads have 'priority' and 'date' fields
        # Date parsing might be needed if date is a string
        return sorted(threads, key=lambda x: (x.get('priority', 0), x.get('date', '')), reverse=True)
