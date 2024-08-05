from ..exceptions import ParsingException


class ProjectException(ParsingException):
	
	def __init__(self, path):
		super().__init__()
		self._project_path = str(path)
	

class InexistentPathException(ProjectException):

	def __init__(self, path):
		super().__init__(path)
	
	def __str__(self):
		return "No project found at path '%s'"%self._project_path
	

class WrongProjectFormat(ProjectException):

	def __init__(self, path):
		super().__init__(path)
	
	def __str__(self):
		return "Wrong project format at path '%s'"%self._project_path
	

class ProjectNotBuiltException(ProjectException):

	def __init__(self, path):
		super().__init__(path)
	
	def __str__(self):
		return "Poem '%s' has not yet been compiled"%self._project_path
		
