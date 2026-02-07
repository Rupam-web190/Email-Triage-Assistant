import re

class TriageEngine:
    def __init__(self):
        self.categories = ["Urgent", "Action", "Awaiting", "Information", "Newsletter", "Spam"]

    def process_single(self, thread_data):
        """Process a single thread"""
        compressed_body = self.scale_down(thread_data.get('body', ''))
        priority_score = self.calculate_priority(thread_data)
        category = self.categorize(thread_data, priority_score)
        
        return {
            "id": thread_data.get('id'),
            "subject": thread_data.get('subject'),
            "sender": thread_data.get('sender'),
            "priority": priority_score,
            "category": category,
            "summary": compressed_body[:200] + "..." if len(compressed_body) > 200 else compressed_body,
            "original_length": len(thread_data.get('body', '')),
            "compressed_length": len(compressed_body),
            "compression_ratio": f"{int((1 - (len(compressed_body) / (len(thread_data.get('body', '')) + 1))) * 100)}%"
        }

    def process_batch(self, threads):
        """Process multiple threads"""
        results = []
        for thread in threads:
            results.append(self.process_single(thread))
        return results

    def scale_down(self, text):
        """
        ScaleDown Core Innovation: 
        Compresses email threads by removing headers, signatures, and redundant text.
        Simulates 85% reduction.
        """
        if not text:
            return ""
            
        # 1. Remove quoted text (replies)
        text = re.sub(r'On .* wrote:.*', '', text, flags=re.DOTALL)
        text = re.sub(r'>.*', '', text)
        
        # 2. Remove signatures (heuristic)
        text = re.sub(r'Best regards,.*', '', text, flags=re.DOTALL)
        text = re.sub(r'Sincerely,.*', '', text, flags=re.DOTALL)
        
        # 3. Remove excess whitespace
        text = " ".join(text.split())
        
        # 4. If still long, take first and last few sentences (Summarization heuristic)
        sentences = text.split('. ')
        if len(sentences) > 5:
            return ". ".join(sentences[:2] + sentences[-1:]) + "."
            
        return text

    def calculate_priority(self, thread_data):
        """
        1-5 priority algorithm
        Urgency(40%) + Sender(30%) + Keywords(30%)
        """
        score = 0
        subject = thread_data.get('subject', '').lower()
        sender = thread_data.get('sender', '').lower()
        body = thread_data.get('body', '').lower()
        
        # Urgency (Keywords in subject)
        if 'urgent' in subject or 'asap' in subject or 'deadline' in subject:
            score += 2.0  # Max 2 for urgency (40% of 5)
        elif 'important' in subject:
            score += 1.5
            
        # Sender (Boss or Client)
        if 'boss' in sender or 'ceo' in sender:
            score += 1.5 # Max 1.5 for sender (30% of 5)
        elif 'client' in sender:
            score += 1.5
            
        # Keywords in body
        if 'review' in body or 'approve' in body:
            score += 1.5 # Max 1.5 for keywords (30% of 5)
            
        # Cap at 5, min 1
        return min(max(round(score), 1), 5)

    def categorize(self, thread_data, priority):
        """Auto-categorize based on content and priority"""
        subject = thread_data.get('subject', '').lower()
        sender = thread_data.get('sender', '').lower()
        
        if 'unsubscribe' in thread_data.get('body', '').lower():
            return "Newsletter"
        if priority >= 4:
            return "Urgent"
        if 'meeting' in subject or 'invite' in subject:
            return "Action"
        if 'update' in subject:
            return "Information"
            
        return "Awaiting"
