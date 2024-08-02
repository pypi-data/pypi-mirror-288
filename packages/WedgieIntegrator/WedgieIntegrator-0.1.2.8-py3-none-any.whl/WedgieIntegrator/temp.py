import httpx
from WedgieIntegrator.auth import HeaderAuth, BasicAuth, TokenAuth, BearerTokenAuth
import asyncio


auth_strategy = BearerTokenAuth(token="fakestring")
client = httpx.AsyncClient(base_url="https://www.wikipedia.org")
request = client.build_request(method="GET", url="/")
auth_strategy.authenticate(request)

response = asyncio.run(client.send(request))


# BasicAuth

# auth_strategy = BasicAuth(username="chad", password="test")
# client = httpx.AsyncClient(base_url="https://www.wikipedia.org")
# request = client.build_request(method="GET", url="/")
# auth_strategy.authenticate(request)
#
# response = asyncio.run(client.send(request))



# HeaderAuth

# auth_strategy = HeaderAuth(secret="fakesecret")
#
# # client = httpx.AsyncClient(base_url="https://httpbin.org")
# # request = client.build_request(method="GET", url="/status/200")
# client = httpx.AsyncClient(base_url="https://www.wikipedia.org")
# request = client.build_request(method="GET", url="/")
# auth_strategy.authenticate(request)
#
# response = asyncio.run(client.send(request))
