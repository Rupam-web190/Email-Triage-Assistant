class PriorityScorer:
    def calculate(self, thread_data):
        """
        1-5 priority algorithm
        Urgency(40%) + Sender(30%) + Keywords(30%)
        """
        score = 0
        subject = thread_data.get('subject', '').lower()
        sender = thread_data.get('sender', '').lower()
        body = thread_data.get('body', '').lower()
        
        # Urgency
        if 'urgent' in subject or 'asap' in subject or 'deadline' in subject:
            score += 2.0
        elif 'important' in subject:
            score += 1.5
            
        # Sender
        if 'boss' in sender or 'ceo' in sender:
            score += 1.5
        elif 'client' in sender:
            score += 1.5
            
        # Keywords
        if 'review' in body or 'approve' in body:
            score += 1.5
            
        return min(max(round(score), 1), 5)
