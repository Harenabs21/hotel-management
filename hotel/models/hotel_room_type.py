from odoo import models, fields, api

class HotelRoomType(models.Model):
    _name = 'hotel.room.type'
    _description = 'Room type'

    name = fields.Selection([
        ('standard', 'Standard'),
        ('executive', 'Executive'),
        ('deluxe', 'Deluxe')
    ], required=True)

    surtax_percentage = fields.Float(string='Quality Type Surtax', compute='_compute_surtax_percentage', store=True)

    @api.depends('name')
    def _compute_surtax_percentage(self):
        for record in self:
            if record.name == 'standard':
                record.surtax_percentage = 0.0
            elif record.name == 'executive':
                record.surtax_percentage = 0.2
            elif record.name == 'deluxe':
                record.surtax_percentage = 0.3
            else:
                record.surtax_percentage = 0.0
