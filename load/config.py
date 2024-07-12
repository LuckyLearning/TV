import yaml


def get_urls():
	with open('urls.yml', 'r', encoding='utf-8') as file:
		config = yaml.safe_load(file)
	urls = config.get('urls', [])
	return urls


if __name__ == '__main__':
	print(get_urls())
