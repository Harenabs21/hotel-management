from odoo import models, fields

class HotelRoomEquipment(models.Model):
    _name = 'hotel.room.equipment'
    _description = 'Room equipment'

    name = fields.Char(string='Name',required=True)
    value = fields.Float(string='Value',required=True)