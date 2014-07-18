def get_unique(lists):
	sm = 0
	for i in lists:
		sm = sm + int(i.pop()) 
	return sm