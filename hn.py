from hackernews import HackerNews
import numpy

hn = HackerNews()

class Item:
	def __init__(self, id, score, text, link, last_score=None):
		self.id = id
		self.score = score
		self.last_score = last_score
		self.text = text
		self.link = link

data = {}
items = {}
def get_items():
	items_list = []
	for story_id in hn.top_stories(limit=20):
		item = hn.get_item(story_id)
		items_list.append(item)
		items[item.item_id] = Item(item.item_id, item.score, item.title, item.url)
	return items_list


def processing_title(title):
	''' Set score, based on the title
		TODO
	'''
	pass

def processing_score(scores, noise=True):
	'''
	set score based on the score
	'''

	# First, sort a list with scores
	sort_result = sorted(scores, key=lambda x: x[1], reverse=True)
	# next check, if item with id is already represented on dict and calculation of growth rate
	grown_result = []
	for (item_id, score) in sort_result:
		if item_id in data:
			item_object = data[item_id]
			noise_value = 1
			if noise: noise_value = abs(numpy.random.normal(0,0.1))
			if score == item_object.score:
				grown_result.append((item_id, score))
				continue
			growth = float(score - item_object.score)/float(item_object.score)
			data[item_id] = Item(item_id, growth, "", "")
			grown_result.append((item_id, growth))
		else:
			data[item_id] = Item(item_id, score, "", "")
			grown_result.append((item_id, score))
	sort_result = sorted(grown_result, key=lambda x: x[1], reverse=True)
	return sort_result



def processing_comments(comments, low_rate=0.2, high_rate=2):
	'''
	 set score for processing comments
	'''
	sort_result = sorted(comments, key=lambda x: x[1], reverse=True)
	# Get Average number of comments
	avg_comments = numpy.mean([res[1] for res in sort_result])
	new_result = []
	for (id, count) in sort_result:
		if count < avg_comments:
			new_rate = high_rate * count
		else:
			new_rate = low_rate * count
		new_result.append((id, new_rate))
	return sorted(new_result, key=lambda x: x[1], reverse=True)


def sorting(data, dict_data):
	for i, (x, score) in enumerate(data):
		if x in dict_data:
			dict_data[x]+=(len(data) - i) * score
		else:
			dict_data[x] = (len(data) - i) * score
	return dict_data	

def processing():
	items_list = get_items()
	result_comments = processing_comments([(item.item_id, len(item.kids)) for item in items_list if item.kids is not None])
	result_score = processing_score([(item.item_id, item.score) for item in items_list])
	result = {}
	result = sorting(result_comments, result)
	result = sorting(result_score, result)
	pre_result = sorted([(key, value) for (key, value) in result.items()],key=lambda x: x[1], reverse=True)
	# output results
	for (key, value) in pre_result[:7]:
		print(items[key].text)


processing()