from odoo import models, fields, api

class HotelRoomType(models.Model):
    _name = 'hotel.room.type'
    _description = 'Room type'

    name = fields.Selection([
        ('standard', 'Standard'),
        ('executive', 'Executive'),
        ('deluxe', 'Deluxe')
    ], required=True)

    quality_type_surtax = fields.Float(string='Quality Type Surtax', compute='_compute_quality_type_surtax', store=True)

    @api.depends('name')
    def _compute_quality_type_surtax(self):
        for record in self:
            if record.name == 'standard':
                record.quality_type_surtax = 0.0
            elif record.name == 'executive':
                record.quality_type_surtax = 0.2
            elif record.name == 'deluxe':
                record.quality_type_surtax = 0.3
            else:
                record.quality_type_surtax = 0.0
