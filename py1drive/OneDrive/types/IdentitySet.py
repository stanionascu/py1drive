from .Identity import Identity

class IdentitySet(object):
	user = None
	application = None
	device = None

	def __init__(self, user=None, application=None, device=None):
		self.user = Identity(**user)
		if (self.application):
			self.application = Identity(**application)
		if (self.device):
			self.device = Identity(**device)
