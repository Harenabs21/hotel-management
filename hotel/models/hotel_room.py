from odoo import models, fields, api
from odoo.exceptions import ValidationError

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
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.company.currency_id)

    @api.depends('base_price','room_type_id','room_equipment_ids')
    def _compute_total_price(self):
        for room in self:
            equipments_value = sum(room.room_equipment_ids.mapped('value'))
            quality_surtax = room.room_type_id.surtax_percentage or 0.0
            price_with_surtax = room.base_price + (room.base_price * quality_surtax)
            room.total_price = price_with_surtax + equipments_value


    @api.constrains('base_price', 'room_capacity')
    def _check_positive_values(self):
        for record in self:
            if record.base_price < 0:
                raise ValidationError(_("Base price cannot be negative."))
            if record.room_capacity <= 0:
                raise ValidationError(_("Room capacity must be greater than zero."))