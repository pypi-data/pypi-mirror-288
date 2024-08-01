from modules.partner.dto.create_partner_dto import CreatePartnerDTO
from modules.partner.dto.update_partner_dto import UpdatePartnerDTO
from modulare.logger import console

class PartnerService:
    async def create(self, create_partner_dto: CreatePartnerDTO):
        console.info('should create partner')

        return create_partner_dto
  
    async def update(self, update_partner_dto: UpdatePartnerDTO):
        console.info('should update partner')

        return update_partner_dto
    
    async def remove(self, partner_id: int):
        console.info('should remove partner')

        return partner_id
    
    async def findAll(self):
        message = 'should find all partners'

        console.info(message)

        return message
    
    async def findOne(self, partner_id: int):
        console.info('should find one partner')

        return partner_id