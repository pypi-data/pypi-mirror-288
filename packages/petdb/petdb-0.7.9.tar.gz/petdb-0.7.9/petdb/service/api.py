
import requests

DEFAULT_PORT = 3944

class API:

	def __init__(self, password: str, port: int):
		self.password = password
		self.port = port

	def drop_db(self):
		return self.__request("/drop")

	def drop_collection(self, name: str):
		return self.__request(f"/drop/{name}")

	def collections(self) -> list[str]:
		return self.__request("/collections")

	def mutate(self, name: str, mutations: list[dict]):
		return self.__request(f"/mutate/{name}", {"mutations": mutations})

	def insert(self, name: str, doc: dict):
		return self.__request(f"/insert/{name}", {"doc": doc})

	def insert_many(self, name: str, docs: list[dict]):
		return self.__request(f"/insert_many/{name}", {"docs": docs})

	def update_one(self, name: str, update: dict, query: dict):
		return self.__request(f"/update_one/{name}", {"update": update, "query": query})

	def update(self, name: str, update: dict, query: dict):
		return self.__request(f"/update/{name}", {"update": update, "query": query})

	def remove(self, name: str, query: dict):
		return self.__request(f"/remove/{name}", {"query": query})

	def clear(self, name: str):
		return self.__request(f"/clear/{name}")

	def __request(self, endpoint: str, body: dict = None):
		if body is None:
			body = {}
		body["password"] = self.password
		response = requests.post(f"http://127.0.0.1:{self.port}{endpoint}", json=body)
		if response is not None and response.headers.get("content-type") == "application/json":
			return response.json()
