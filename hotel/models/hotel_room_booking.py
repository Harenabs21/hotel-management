from odoo import models, fields, api

class HotelRoomBooking(models.Model):
    _name = 'hotel.room.booking'
    _description = 'Room booking'

    room_id = fields.Many2one('hotel.room', string='Room')
    customer_id = fields.Many2one('res.partner', string='Customer')
    start_date = fields.Date(string='Start date',required=True)
    end_date = fields.Date(string='End date',required=True)
    actual_end_date = fields.Date('Actual end date')
    people_count = fields.Integer('People count')
    equipment_ids = fields.Many2many('hotel.room.equipment', string='Equipments')
    state = fields.Selection([('confirmed', 'Confirmée'), ('done', 'Terminée'), ('cancelled', 'Annulée')], default='confirmed')
    total_price = fields.Float('Total price', compute='_compute_total_price')

    @api.depends('room_id', 'equipment_ids', 'start_date', 'end_date')
    def _compute_total_price(self):
        for booking in self:
            
            if not booking.start_date or not booking.end_date or not booking.room_id:
                booking.total_price = 0.0
                continue

            effective_end = booking.actual_end_date or booking.end_date

            if effective_end > booking.end_date:
                effective_end = booking.end_date

            days = (effective_end - booking.start_date).days + 1
            if days < 0:
                days = 0

            daily_price = booking.room_id.total_price or 0.0

            equipment_cost = sum(booking.equipment_ids.mapped('value')) if booking.equipment_ids else 0.0

            booking.total_price = (daily_price + equipment_cost) * days
