from models import Url

url = Url()
url.collection.create_index('short_key', unique = True)