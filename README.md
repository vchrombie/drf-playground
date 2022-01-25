# drf-playground

### 1. [Serialization](https://www.django-rest-framework.org/tutorial/1-serialization/)
 
- Created `Snippet` model (`snippet/models.py`) that can store code snippets
- makemigrations and migrate
  ```
  $ poetry run makemigrations
  $ poetry run migrate
  ```
- Added some initial data to the `Snippet` model using QuerySet
- Serialized the snippet instances into representations (`snippet/serializers.py`)
- Reduced the `SnippetSerializer` using the `serializers.ModelSerializer`
- Tried out the new Serializer class using the Django shell
  ```
  $ poetry run shell
  ```
  ```py
  >>> from snippets.models import Snippet
  >>> from snippets.serializers import SnippetSerializer
  >>> serializer = SnippetSerializer(Snippet.objects.all(), many=True)
  >>> serializer.data
  [OrderedDict([('id', 1), ('title', 'importing os, datetime'), ('code', 'import os, datetime'), ('linenos', False), ('language', 'python'), ('style', 'friendly')]), OrderedDict([('id', 2), ('title', 'print statement'), ('code', 'print("Hello, World!")'), ('linenos', False), ('language', 'python'), ('style', 'friendly')]), OrderedDict([('id', 3), ('title', 'print statement'), ('code', 'print("Hello, World!")'), ('linenos', False), ('language', 'python'), ('style', 'friendly')])]
  >>> 
  >>> from rest_framework.renderers import JSONRenderer
  >>> data = JSONRenderer().render(serializer.data)
  >>> data
  b'[{"id":1,"title":"importing os, datetime","code":"import os, datetime","linenos":false,"language":"python","style":"friendly"},{"id":2,"title":"print statement","code":"print(\\"Hello, World!\\")","linenos":false,"language":"python","style":"friendly"},{"id":3,"title":"print statement","code":"print(\\"Hello, World!\\")","linenos":false,"language":"python","style":"friendly"}]'
  >>> 
  >>> import json, pprint
  >>> json.loads(data)
  [{'id': 1, 'title': 'importing os, datetime', 'code': 'import os, datetime', 'linenos': False, 'language': 'python', 'style': 'friendly'}, {'id': 2, 'title': 'print statement', 'code': 'print("Hello, World!")', 'linenos': False, 'language': 'python', 'style': 'friendly'}, {'id': 3, 'title': 'print statement', 'code': 'print("Hello, World!")', 'linenos': False, 'language': 'python', 'style': 'friendly'}]
  >>> pprint.pprint(json.loads(data))
  [{'code': 'import os, datetime',
    'id': 1,
    'language': 'python',
    'linenos': False,
    'style': 'friendly',
    'title': 'importing os, datetime'},
   {'code': 'print("Hello, World!")',
    'id': 2,
    'language': 'python',
    'linenos': False,
    'style': 'friendly',
    'title': 'print statement'},
   {'code': 'print("Hello, World!")',
    'id': 3,
    'language': 'python',
    'linenos': False,
    'style': 'friendly',
    'title': 'print statement'}]
  >>> 
  ```
- Created Django views to list the snippets, and also for CRUD operations
- Update the urls to include the snippet configurations 
- Tested the new APIs using [httpie/httpie](https://github.com/httpie/httpie)
  ```bash
  $ http http://127.0.0.1:8000/snippets/
  HTTP/1.1 200 OK
  Content-Length: 410
  Content-Type: application/json
  Date: Tue, 25 Jan 2022 12:42:07 GMT
  Referrer-Policy: same-origin
  Server: WSGIServer/0.2 CPython/3.8.10
  X-Content-Type-Options: nosniff
  X-Frame-Options: DENY

  [
      {
          "code": "import os, datetime",
          "id": 1,
          "language": "python",
          "linenos": false,
          "style": "friendly",
          "title": "importing os, datetime"
      },
      {
          "code": "print(\"Hello, World!\")",
          "id": 2,
          "language": "python",
          "linenos": false,
          "style": "friendly",
          "title": "print statement"
      },
      {
          "code": "print(\"Hello, World!\")",
          "id": 3,
          "language": "python",
          "linenos": false,
          "style": "friendly",
          "title": "print statement"
      }
  ]
  ```
  ```bash
  $ http http://127.0.0.1:8000/snippets/2/
  HTTP/1.1 200 OK
  Content-Length: 134
  Content-Type: application/json
  Date: Tue, 25 Jan 2022 12:42:14 GMT
  Referrer-Policy: same-origin
  Server: WSGIServer/0.2 CPython/3.8.10
  X-Content-Type-Options: nosniff
  X-Frame-Options: DENY

  {
      "code": "print(\"Hello, World!\")",
      "id": 2,
      "language": "python",
      "linenos": false,
      "style": "friendly",
      "title": "print statement"
  }

  ```
