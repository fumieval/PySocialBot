from pysocialbot import botlib
class TwitterConversation():
    def __init__(self):
        self.table = {}
    def append(self, status):
        self.table[status.id] = (status, [])
        if status.in_reply_to_status_id in self.table:
            status.table[status.id][1].append(status.id)