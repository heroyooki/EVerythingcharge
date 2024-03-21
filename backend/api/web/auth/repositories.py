from fastapi import Request, Response


class WebRepository:

    async def unset_for_next(self, response: Response):
        raise NotImplementedError()

    async def set_for_next(self, token: str, response: Response):
        raise NotImplementedError()

    async def extract_token(self, request: Request):
        raise NotImplementedError()


class CookiesRepo(WebRepository):
    def __init__(self, cookie_name="access_token"):
        self.cookie_name = cookie_name

    async def unset_for_next(self, response: Response):
        response.delete_cookie(self.cookie_name)

    async def set_for_next(self, token: str, response: Response):
        response.set_cookie(self.cookie_name, token)

    async def extract_token(self, request: Request):
        return request.cookies.get(self.cookie_name)


class HeadersRepo(WebRepository):
    def __init__(self, header_name):
        self.header_name = header_name

    async def unset_for_next(self, response: Response):
        del response.headers[self.header_name]

    async def set_for_next(self, token: str, response: Response):
        response.headers[self.header_name] = token

    async def extract_token(self, request: Request):
        return request.headers.get(self.header_name)
