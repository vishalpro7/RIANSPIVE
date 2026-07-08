from pydantic import BaseModel

class BestSellingProduct(BaseModel):

    product: str

    quantity_sold: int


class AnalyticsResponse(BaseModel):

    best_selling_products: list[BestSellingProduct]

