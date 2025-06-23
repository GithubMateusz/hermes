from esmerald import Gateway

from .views import ProductView

route_patterns = [
    Gateway(handler=ProductView, tags=["Product"]),
]
