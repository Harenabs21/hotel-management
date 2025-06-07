from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import date, timedelta

class HotelRoomBooking(models.Model):
    _name = 'hotel.room.booking'
    _description = 'Room booking'


    name = fields.Char(string='Booking Reference', required=True, copy=False, readonly=True, default=lambda self: _('New'))
    room_id = fields.Many2one('hotel.room', string='Room')
    customer_id = fields.Many2one('res.partner', string='Customer')
    start_date = fields.Date(string='Start date',required=True)
    end_date = fields.Date(string='End date',required=True)
    actual_end_date = fields.Date('Actual end date')
    people_count = fields.Integer('People count')
    equipment_ids = fields.Many2many('hotel.room.equipment', string='Equipments')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('done', 'Completed'),
        ('cancelled', 'Cancelled')
    ], string='Status', default='draft')
    total_price = fields.Float('Total price', compute='_compute_total_price')
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.company.currency_id)

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('hotel.room.booking') or _('New')
        return super(HotelRoomBooking, self).create(vals)

    @api.depends('room_id.total_price', 'equipment_ids.value', 'start_date', 'end_date', 'actual_end_date', 'state')
    def _compute_total_price(self):
        for booking in self:
            
            if not booking.start_date or not booking.end_date or not booking.room_id or not booking.room_id.total_price:
                booking.total_price = 0.0
                continue

            effective_end = booking.end_date
            if booking.actual_end_date and booking.actual_end_date <= booking.end_date:
                effective_end = booking.actual_end_date
            
            if booking.start_date > effective_end:
                days = 0
            else:
                days = (effective_end - booking.start_date).days + 1

            daily_room_price = booking.room_id.total_price
            equipment_cost_for_booking = sum(booking.equipment_ids.mapped('value'))
            
            booking.total_price = (daily_room_price + equipment_cost_for_booking) * days
            
    @api.constrains('start_date', 'end_date', 'people_count', 'room_id', 'state')
    def _check_booking_constraints(self):
        for booking in self:
            if booking.start_date and booking.end_date:
                if booking.start_date > booking.end_date:
                    raise ValidationError(_("The start date must be before or equal to the end date."))
                if booking.start_date < date.today() and booking.state not in ('done', 'cancelled'):
                    raise ValidationError(_("Cannot create or modify a booking for a past date."))
            
            if booking.room_id and booking.people_count:
                if booking.people_count > booking.room_id.room_capacity:
                    raise ValidationError(_("The number of people (%s) exceeds the room's maximum capacity (%s)." % (booking.people_count, booking.room_id.room_capacity)))

            if booking.state == 'confirmed':
                overlapping_bookings = self.search([
                    ('room_id', '=', booking.room_id.id),
                    ('id', '!=', booking.id),
                    ('state', 'in', ['confirmed', 'done']), 
                    ('start_date', '<=', booking.end_date),
                    ('end_date', '>=', booking.start_date),
                ])
                if overlapping_bookings:
                    raise ValidationError(_("This room is already booked for part or all of the selected period. "
                                            "Please choose another room or adjust dates."))

    def action_confirm(self):
        for booking in self:
            booking._check_booking_constraints() 
            booking.room_id.state = 'occupied'
            booking.state = 'confirmed'

    def action_complete(self):
        for booking in self:
            booking.state = 'done'

            if not booking.actual_end_date:
                booking.actual_end_date = date.today()
            
            
            next_booking = self.search([
                ('room_id', '=', booking.room_id.id),
                ('id', '!=', booking.id),
                ('state', '=', 'confirmed'),
                ('start_date', '=', booking.actual_end_date + timedelta(days=1))
            ], limit=1)
            
            if not next_booking:
                booking.room_id.state = 'available'

    def action_cancel(self):
        for booking in self:
            booking.state = 'cancelled'
            booking.room_id.state = 'available'