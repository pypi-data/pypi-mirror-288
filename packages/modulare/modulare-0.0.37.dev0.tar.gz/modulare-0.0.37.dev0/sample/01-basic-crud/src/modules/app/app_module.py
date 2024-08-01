from modules.partner.partner_module import PartnerModule
from modulare.decorators import Module
from modules.app.app_controller import AppController

@Module({
    'imports': [ PartnerModule ],
    'controllers': [ AppController ]
})
class AppModule:
    pass