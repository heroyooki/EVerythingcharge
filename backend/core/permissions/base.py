from fastapi import Request


class BasePermission:

    async def __call__(self, request: Request):
        return await self.has_permission(request)

    async def has_permission(self, request: Request):
        raise NotImplementedError()
