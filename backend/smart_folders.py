class SmartFolders:
    def categorize(self, thread):
        """Auto-categorize into 8 folders"""
        priority = thread.get('priority', 1)
        subject = thread.get('subject', '').lower()
        
        if priority == 5:
            return "Urgent"
        elif 'meeting' in subject:
            return "Calendar"
        elif 'invoice' in subject or 'payment' in subject:
            return "Finance"
        elif 'newsletter' in subject or 'unsubscribe' in thread.get('body', '').lower():
            return "Newsletters"
        elif 'receipt' in subject:
            return "Receipts"
        elif 'update' in subject:
            return "Awaiting"
        else:
            return "Inbox"
