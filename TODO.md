# PyDK - Simple Python SDK

## Main Todos

- zvážit řešení:
    - A: opravdu obalit vygenerovaný kód vlastní z části duplicitní ale manažovatelnou vrstvou
        - to samé co v B níže, ale ještě přidám vlastní objekty a opravdový adaptér, má fasáda by tedy byla použitelná
          pro různá řešení dle adaptace
        - loose coupling
    - B: trivialisticky použít obalení spíše jako adaptér než fasádu
        - jen připravím volání na vytvoření objektů a jejich provolání s mezilogikou na auth a logy a cache
        - vlastně více tight coupling
- Adaptace:
    - zvářit vlastní řešení skrze httpx, tak tight coupled adapter client dle generovaného

## Todos Consultation

- create SDK facade & vygenerované a safixované
- learn: kvargs and args
- serializace a normalizace
  objektů https://medium.com/@HeCanThink/marshmallow-a-sweet-python-library-for-object-serialization-and-deserialization-3001438b4708
  nebo Pydantic
- Python je o dekorování, lol @ znamená, že to je dekorované
- sync like: httpx, requests, aiohttp
- Python
  Backoff https://stackoverflow.com/questions/75224154/python-backoff-decorator-library-for-retrying-with-exception-treatment
- popřípadě libka či jiné řešení - race for status - 200 a 201 responses
- seznámit se s tím - dekorátory v Pythonu
- key - je to python, NEŘEEEEŠ -> PYTHONIC
- dev dependencies

## Challanges

- caching on SDK level even if app is not running every time (file, Redis like storage, server approach - test usage on
  fastapi)
- prepare facade logic to provide this kinda usage:
    - create desired object (manually or from factory)
    - denormalize object into desired form (json, array, strings, whatever - just choose one working)
    - prepare & use denormalized object for queries
    - perform auth in background
    - perform request (post, get, del, put, patch - for actual data and data methods)
    - return response in normalized form
- further points of challenge:
    - models
    - their normalization and denormalization
    - request logic
        - data
        - auth
    - generalized request logic mapped to the generated solution as in:
        - adapter to the generated solution
        - interface for adapters
    - logging - setting and usage (instead of prints)
        - maybe file too or file in default?
- cache adapter and interface for multiple solutions?
  - json file cache
  - ram cache
  - disk cache
  - sqlite cache?

## Criticism

- https://stackoverflow.com/questions/34116942/how-to-cache-asyncio-coroutines
- better makefile
- configurable!
- facade!
- tests by function and endpoints and data
- aknowledge problem about cache but to not resolve it
- make it ready as package
- my own exceptions
- the FIELD implementaion