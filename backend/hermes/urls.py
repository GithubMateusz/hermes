from esmerald import Gateway
from sqlalchemy.exc import IntegrityError

from .handlers import handle_integrity_error
from .views.chatbot import ChatBotView
from .views.products import ProductView

route_patterns = [
    Gateway(
        handler=ProductView,
        tags=["Product"],
        exception_handlers={IntegrityError: handle_integrity_error},
    ),
    Gateway(handler=ChatBotView, tags=["ChatBot"]),
]
