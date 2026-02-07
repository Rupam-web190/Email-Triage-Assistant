import re

class MeetingExtractor:
    def extract(self, text):
        """Detect calendar invites + auto-add to Google Calendar (Mock)"""
        # Simple regex for date/time patterns
        date_pattern = r'\b(Mon|Tue|Wed|Thu|Fri|Sat|Sun), \d{1,2} (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)( \d{4})?\b'
        time_pattern = r'\b\d{1,2}(:\d{2})? ?(am|pm|AM|PM)\b'
        
        dates = re.findall(date_pattern, text)
        times = re.findall(time_pattern, text)
        
        if dates or times or 'meeting' in text.lower() or 'zoom' in text.lower():
            return {
                "is_meeting": True,
                "suggested_title": "Meeting", # Would use NLP to extract title
                "dates_detected": [d[0] for d in dates] if dates else [],
                "times_detected": [t[0] for t in times] if times else []
            }
        return {"is_meeting": False}
