from esmerald import Gateway

from .views import ChatBotView, ProductView

route_patterns = [
    Gateway(handler=ProductView, tags=["Product"]),
    Gateway(handler=ChatBotView, tags=["ChatBot"]),
]
