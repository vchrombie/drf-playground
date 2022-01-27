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

### 2. [Requests and Responses](https://www.django-rest-framework.org/tutorial/2-requests-and-responses/)

- Added the `@api_view` decorator to the function based views to use the `Response` & `Request` objects
- Used rest framework status codes for the `Response` object
  ```bash
  $ http --form POST http://127.0.0.1:8000/snippets/ code="Hello, World!"
  HTTP/1.1 201 Created
  Allow: OPTIONS, GET, POST
  Content-Length: 94
  Content-Type: application/json
  Date: Tue, 25 Jan 2022 13:16:10 GMT
  Referrer-Policy: same-origin
  Server: WSGIServer/0.2 CPython/3.8.10
  Vary: Accept, Cookie
  X-Content-Type-Options: nosniff
  X-Frame-Options: DENY

  {
      "code": "Hello, World",
      "id": 4,
      "language": "text",
      "linenos": false,
      "style": "friendly",
      "title": ""
  }
  ```
  ```bash
  $ http --form GET http://127.0.0.1:8000/snippets/2/
  HTTP/1.1 200 OK
  Allow: GET, DELETE, PUT, OPTIONS
  Content-Length: 123
  Content-Type: application/json
  Date: Tue, 25 Jan 2022 13:55:47 GMT
  Referrer-Policy: same-origin
  Server: WSGIServer/0.2 CPython/3.8.10
  Vary: Accept, Cookie
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
- Added optional format suffixes to the URLs
  ```bash
  $ http http://127.0.0.1:8000/snippets/1.json
  HTTP/1.1 200 OK
  Allow: OPTIONS, DELETE, GET, PUT
  Content-Length: 125
  Content-Type: application/json
  Date: Tue, 25 Jan 2022 13:17:11 GMT
  Referrer-Policy: same-origin
  Server: WSGIServer/0.2 CPython/3.8.10
  Vary: Accept, Cookie
  X-Content-Type-Options: nosniff
  X-Frame-Options: DENY

  {
      "code": "import os, datetime",
      "id": 1,
      "language": "python",
      "linenos": false,
      "style": "friendly",
      "title": "importing os, datetime"
  }
  ```
  ```bash
  $ http http://127.0.0.1:8000/snippets/1/ Accept:application/json
  HTTP/1.1 200 OK
  Allow: OPTIONS, DELETE, GET, PUT
  Content-Length: 125
  Content-Type: application/json
  Date: Tue, 25 Jan 2022 13:17:34 GMT
  Referrer-Policy: same-origin
  Server: WSGIServer/0.2 CPython/3.8.10
  Vary: Accept, Cookie
  X-Content-Type-Options: nosniff
  X-Frame-Options: DENY

  {
      "code": "import os, datetime",
      "id": 1,
      "language": "python",
      "linenos": false,
      "style": "friendly",
      "title": "importing os, datetime"
  }
  ```

### 3. [Class-based Views](https://www.django-rest-framework.org/tutorial/3-class-based-views/)

- Rewrite the function API views using class-based views
- Used mixins and generics to reducde the views
- Used generic class-based views to reduce the views even more

### 4. [Authentication & Permissions](https://www.django-rest-framework.org/tutorial/4-authentication-and-permissions/#tutorial-4-authentication-permissions)

- Added `owner` field using the django-inbuilt `User` model
- Created `UserSerializer` to create endpoints for the `User` model
- Created `UserList` and `UserRetrieve` using the generic class-based views
- Updated the `snippets.urls` to map the newly created views to `/users/` and `/user/x/`
- Created a custom permission to access the objects so that only the user that created a code snippet is able to update or delete it
- Tested the API using the `httpie` tool
  ```bash
  $ http GET http://127.0.0.1:8000/snippets/
  HTTP/1.1 200 OK
  Allow: GET, POST, HEAD, OPTIONS
  Content-Length: 289
  Content-Type: application/json
  Date: Thu, 27 Jan 2022 07:47:04 GMT
  Referrer-Policy: same-origin
  Server: WSGIServer/0.2 CPython/3.8.10
  Vary: Accept, Cookie
  X-Content-Type-Options: nosniff
  X-Frame-Options: DENY

  [
      {
          "code": "import os\r\n\r\nprint(os.getcwd())",
          "id": 2,
          "language": "python",
          "linenos": false,
          "owner": "venu",
          "style": "friendly",
          "title": "print current directory path"
      },
      {
          "code": "hi, this is a text snippet.",
          "id": 3,
          "language": "text",
          "linenos": false,
          "owner": "root",
          "style": "friendly",
          "title": ""
      }
  ]
  ```
  ```bash
  $ http GET http://127.0.0.1:8000/snippet/3/
  HTTP/1.1 403 Forbidden
  Allow: GET, PUT, PATCH, DELETE, HEAD, OPTIONS
  Content-Length: 58
  Content-Type: application/json
  Date: Thu, 27 Jan 2022 07:47:09 GMT
  Referrer-Policy: same-origin
  Server: WSGIServer/0.2 CPython/3.8.10
  Vary: Accept, Cookie
  X-Content-Type-Options: nosniff
  X-Frame-Options: DENY

  {
      "detail": "Authentication credentials were not provided."
  }

  $ http -a root:root GET http://127.0.0.1:8000/snippet/3/
  HTTP/1.1 200 OK
  Allow: GET, PUT, PATCH, DELETE, HEAD, OPTIONS
  Content-Length: 124
  Content-Type: application/json
  Date: Thu, 27 Jan 2022 07:47:18 GMT
  Referrer-Policy: same-origin
  Server: WSGIServer/0.2 CPython/3.8.10
  Vary: Accept, Cookie
  X-Content-Type-Options: nosniff
  X-Frame-Options: DENY

  {
      "code": "hi, this is a text snippet.",
      "id": 3,
      "language": "text",
      "linenos": false,
      "owner": "root",
      "style": "friendly",
      "title": ""
  }
  ```
  ```bash
  $ http POST http://127.0.0.1:8000/snippets/ code="simple code snippet."
  HTTP/1.1 403 Forbidden
  Allow: GET, POST, HEAD, OPTIONS
  Content-Length: 58
  Content-Type: application/json
  Date: Thu, 27 Jan 2022 07:47:56 GMT
  Referrer-Policy: same-origin
  Server: WSGIServer/0.2 CPython/3.8.10
  Vary: Accept, Cookie
  X-Content-Type-Options: nosniff
  X-Frame-Options: DENY

  {
      "detail": "Authentication credentials were not provided."
  }

  $ http -a root:root POST http://127.0.0.1:8000/snippets/ code="simple code snippet."
  HTTP/1.1 201 Created
  Allow: GET, POST, HEAD, OPTIONS
  Content-Length: 117
  Content-Type: application/json
  Date: Thu, 27 Jan 2022 07:48:16 GMT
  Referrer-Policy: same-origin
  Server: WSGIServer/0.2 CPython/3.8.10
  Vary: Accept, Cookie
  X-Content-Type-Options: nosniff
  X-Frame-Options: DENY

  {
      "code": "simple code snippet.",
      "id": 4,
      "language": "text",
      "linenos": false,
      "owner": "root",
      "style": "friendly",
      "title": ""
  }

  $ http -a root:root GET http://127.0.0.1:8000/snippet/4/
  HTTP/1.1 200 OK
  Allow: GET, PUT, PATCH, DELETE, HEAD, OPTIONS
  Content-Length: 117
  Content-Type: application/json
  Date: Thu, 27 Jan 2022 07:48:26 GMT
  Referrer-Policy: same-origin
  Server: WSGIServer/0.2 CPython/3.8.10
  Vary: Accept, Cookie
  X-Content-Type-Options: nosniff
  X-Frame-Options: DENY

  {
      "code": "simple code snippet.",
      "id": 4,
      "language": "text",
      "linenos": false,
      "owner": "root",
      "style": "friendly",
      "title": ""
  }
  ```

### 5. [Relationships & Hyperlinked APIs](Relationships & Hyperlinked APIs)

- Created a field for storing the HTML output of the highlighted code, this is generated using the `HtmlFormatter` of the `pygments` library
- Updated the serializers to use `HyperlinkedModelSerializer` instead of `ModelSerializer`
  - it doesn't include `id` field, so we have to mention it so that we can use it for traversing
  - it includes the `url` field by using the `HyperlinkedIdentityField`, we can use this for showing the highlighted HTML code
  - it uses `HyperlinkedRelatedField`, instead of `PrimaryKeyRelatedField`, for establishing relationships
- Added the urlpatterns to test the APIs
  ```bash
  $ http -a root:root GET http://127.0.0.1:8000/snippet/3/
  HTTP/1.1 200 OK
  Allow: GET, PUT, PATCH, DELETE, HEAD, OPTIONS
  Content-Length: 246
  Content-Type: application/json
  Date: Thu, 27 Jan 2022 10:16:59 GMT
  Referrer-Policy: same-origin
  Server: WSGIServer/0.2 CPython/3.8.10
  Vary: Accept, Cookie
  X-Content-Type-Options: nosniff
  X-Frame-Options: DENY

  {
      "code": "This is a simple text snippet.",
      "highlight": "http://127.0.0.1:8000/snippet/3/highlight/",
      "id": 3,
      "language": "output",
      "linenos": false,
      "owner": "root",
      "style": "friendly",
      "title": "simple text snippet",
      "url": "http://127.0.0.1:8000/snippet/3/"
  }
  ```
