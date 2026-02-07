class AutoReplier:
    def __init__(self):
        self.templates = {
            "professional": "Hi {name},\n\nThanks for your email regarding '{subject}'.\n\nI have received it and will review shortly.\n\nBest,\n[My Name]",
            "casual": "Hey {name},\n\nGot your message about '{subject}'. I'll take a look soon!\n\nCheers,\n[My Name]",
            "urgent": "Hi {name},\n\nI acknowledge the urgency of '{subject}'. I am prioritizing this and will get back to you ASAP.\n\nRegards,\n[My Name]"
        }

    def generate(self, thread_data, tone='professional'):
        """Generate smart response"""
        subject = thread_data.get('subject', 'No Subject')
        sender = thread_data.get('sender', 'Sender')
        # Extract name from sender "Name <email>"
        if '<' in sender:
            name = sender.split('<')[0].strip().replace('"', '')
        else:
            name = sender.split('@')[0]
            
        template = self.templates.get(tone, self.templates['professional'])
        return template.format(name=name, subject=subject)
