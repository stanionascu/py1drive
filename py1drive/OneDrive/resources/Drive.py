from ..types import IdentitySet
from ..facets import Quota

class Drive(object):
	id = str()
	driveType = str()
	owner = None
	quota = None

	def __init__(self, id=None, driveType=None, owner=None, quota=None, **kwargs):
		self.id = id
		self.driveType = driveType
		self.owner = IdentitySet(**owner)
		self.quota = Quota(**quota)