
from modules.partner.partner_controller import PartnerController
from modulare.decorators import Module

@Module({
    'controllers': [ PartnerController ]
})
class PartnerModule:
    pass