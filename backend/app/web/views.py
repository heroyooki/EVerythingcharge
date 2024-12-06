from pydantic import BaseModel


class PaginationView(BaseModel):
    current_page: int
    last_page: int
    total: int
