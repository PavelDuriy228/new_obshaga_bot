from .general import router as gen_router
from handlers.adm_handlers import edit_strst_routers, gen_adm_router
from .strst_handls import gen_star_router, star_router2
from .statistik import router as statistik_router
from .user_handlers import gen_user_router, event_user_router
from .eventer_handlers import funcs_event_rt, events_rt, gen_event_rt

__all__=[    
    'gen_router',
    'edit_strst_routers', 
    'gen_adm_router',
    'gen_star_router',
    'star_router2', 
    'statistik_router', 
    'gen_user_router',
    'funcs_event_rt' ,
    'events_rt', 'gen_event_rt',
    'event_user_router'
]