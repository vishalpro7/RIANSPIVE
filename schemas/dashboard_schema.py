from pydantic import BaseModel

class DashBoardResponse(BaseModel):

    total_users : int

    total_products : int

    total_orders : int

    pending_orders : int

    delivered_orders : int

    cancelled_orders : int

    total_revenue : int

