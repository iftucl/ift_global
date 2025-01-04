import re
from pydantic import validate_call

@validate_call
def trim_string(x: str, what: str, action_regex: str = '\\s+') -> str:
	"""
	Trim end and/or start of a string based on regex expr

	:param x: a string to be cleaned
	:type x: str
	:param what: either leading (start), trailing (end) or both
		if the replace happens at the beginning or end or both
	:type what: str
	:param action_regex: a regex expression, defaults to '\s+'
	:type action_regex: str, optional
	:raises ValueError: if the what argument is not in the specified
	:return: trimmed string
	:rtype: str
	"""
	if what not in ('both', 'leading', 'trailing', 'none'):
		raise ValueError('Only "both", "leading" and "trailing" are accepted for "what" argument')
	
	match what:        
		case 'both':
			return re.sub(f'^[{action_regex}]+|[{action_regex}]+$', '', x)
		case 'leading':
			return re.sub(f'^[{action_regex}]+', '', x)
		case 'trailing':
			return re.sub(f'[{action_regex}]+$', '', x)