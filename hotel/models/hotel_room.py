from odoo import models, fields, api

class HotelRoom(models.Model):
    _name = 'hotel.room'
    _description = 'Room'

    name = fields.Char(string='Name', required=True)
    state = fields.Selection([('available','Available'),('occupied','Occupied')], default='available')
    base_price = fields.Float(string='Base price',required=True)
    room_capacity = fields.Integer(string='Capacity',required=True)
    room_equipment_ids = fields.Many2many('hotel.room.equipment', string='Equipment')
    room_type_id = fields.Many2one('hotel.room.type',string='Room Type')
    total_price = fields.Float(compute="_compute_total_price",string="Total price", readonly=True)

    @api.depends('base_price','room_type_id','room_equipment_ids')
    def _compute_total_price(self):
        for room in self:
            equipments_value = sum(room.room_equipment_ids.mapped('value'))
            quality_surtax = room.room_type_id.quality_type_surtax or 0.0
            price_with_surtax = room.base_price + (room.base_price * quality_surtax)
            room.total_price = price_with_surtax + equipments_value


