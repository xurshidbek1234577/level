from .start import start_router
from .profile import profile_router
from .missions import missions_router
from .ranking import ranking_router
from .shop import shop_router
from .settings import settings_router
from .admin import admin_router

__all__ = [
    'start_router',
    'profile_router',
    'missions_router',
    'ranking_router',
    'shop_router',
    'settings_router',
    'admin_router',
]
