

class AbstractUserRepo(metaclass=abc.ABCMeta):

    async def get(self, user_id: uuid.UUID) -> domain.User:
        ...

    async def get_multi(self, user_ids: list[uuid.UUID]) -> list[domain.User]:
        # В самую последнюю очередь
        ...

    async def put(self, user: domain.User) -> domain.User:
        ...

    async def put_multi(self, user_ids: list[uuid.UUID]) -> list[domain.User]:
        # В самую последнюю очередь
        ...

    async def delete(self, user_id: uuid.UUID) -> None:
        ...

    async def search(self, **search_params) -> list[domain.User]:
        # Здесь в первую очередь мы реализуем получение всех пользователей
        ...