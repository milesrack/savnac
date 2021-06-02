import re

def removeTags(text):
	TAG_RE = re.compile(r'<[^>]+>')
	return TAG_RE.sub('', text)
