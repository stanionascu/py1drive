class Quota(object):
	total = int()
	used = int()
	remaining = int()
	deleted = int()
	state = str()

	def __init__(self, total=0, used=0, remaining=0, deleted=0, state=None):
		self.total = total
		self.used = used
		self.remaining = remaining
		self.deleted = deleted
		self.state = state