safibase

A Python library for safibase. A high performance realtime database.

Installation

You can install this package using pip:

```sh
pip install safibase


##Usage

from safibase import Safibase

# Get your api key 'your_api_key' with the actual API key
api_key = 'your_api_key'

# Usage with lake specified separately
safibase = Safibase(api_key)
response = safibase.lake('test_lake').record('test_record').create(model).run()
print(response)

#Deleting a record operation
response = safibase.lake('test_lake').record('test_record').delete('at id='2'').run()
print(response)

# Usage with lake specified along with API key
safibase = safibase(api_key, lake_name='test_lake')
response = safibase.record('test_record').create(model).run()
print(response)

response = safibase.record('test_record').delete('at id='2'').run()
print(response)
