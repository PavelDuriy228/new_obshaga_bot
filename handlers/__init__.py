from .general import router as gen_router
from handlers.adm_handlers import edit_strst_routers, gen_adm_router

__all__=[    
    'gen_router',
    'edit_strst_routers', 
    'gen_adm_router'
]