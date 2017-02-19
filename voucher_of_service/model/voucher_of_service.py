# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from openerp import fields, models
#from openerp.tools.translate import _
#from openerp.tools import config
#import ir
#import pdb


class Location(models.Model):
    """Location of Voucher Of Service"""
    _description = """
    Tour location
    """
    _name = "tour.location"
    name = fields.Char('Name', required=True, help='Name')
    description = fields.Char('Description', required=True, help='Description')
    lat = fields.Float('Latitude', digits=(9, 6), help='Latitude')
    lng = fields.Float('Longitude', digits=(9, 6), help='Longitude')


class VisitPoint(models.Model):
    """Visit point to be used in itinerary"""
    _description = """
    Tour visit point
    """
    _name = "tour.visit_point"
    name = fields.Char('Name', help='Visit point name')
    location_id = fields.Many2one('tour.location', 'Location', help='Location')
    description = fields.Char('Description', help='Description')


class VoucherOfService(models.Model):
    """Voucher of Service"""
    _description = """
    Voucher of service
    """
    _name = "tour.voucherofservice"
    name = fields.Char('Name', help='Name of Voucher of Service')
    folio_id = fields.Many2one('tour.folio', 'Folio', help='fields help')
    passenger_ids = fields.Many2many('res.partner',
                                     'voucherofservice_partner_rel',
                                     'voucherofservice_id',
                                     'passenger_id', 'Passengers',
                                     help='Passengers List')
    overnight_ids = fields.One2many('tour.vos_itinerary_overnight',
                                    'voucherofservice_id',
                                    'Visit Points', help='Visit points')
    included = fields.Text('Included', help='Included items')
    excluded = fields.Text('Excluded', help='Excluded items')
    important_notes = fields.Text('Important Notes',
                                  help="""Explain the recipient of this document
                                  what needs to be taken in account so he will
                                  be correctly informed.""")
    ib_ap_dep_id = fields.Many2one('touroperation.airport',
                                   'Departure Airport Inbound',
                                   help='Select departure airport inbound')
    ib_ap_arr_id = fields.Many2one('touroperation.airport',
                                   'Arrival Airport Inbound',
                                   help='Select arrival airport inbound')
    ib_time_dep = fields.Datetime('Departure Inbound Time')
    ib_time_arr = fields.Datetime('Arrival Inbound Time')
    ib_airline_id = fields.Many2one('touroperation.airline',
                                    'Departure Airline Inbound',
                                    help='Select inbound departure airline')
    ib_flight_no = fields.Char('Inbound Flight Number',
                               help='Inbound Flight Number')
    ob_ap_dep_id = fields.Many2one('touroperation.airport',
                                   'Departure Airport Outbound',
                                   help='Select outbound departure airport')
    ob_ap_arr_id = fields.Many2one('touroperation.airport',
                                   'Arrival Airport Outbound',
                                   help='Select arrival airport outbound')
    ob_time_dep = fields.Datetime('Departure Outbound Time')
    ob_time_arr = fields.Datetime('Arrival Outbound Time')
    ob_airline_id = fields.Many2one('touroperation.airline',
                                    'Departure Airline Outbound',
                                    help='Select departure outbound airline')
    ob_flight_no = fields.Char('Outbound Flight Number',
                               help='outbound Flight Number')
    hotel_contact = fields.Text('Emergency Phones', help="""Provide
        information about hotel and contacts.""")
    emergency_phones = fields.Char('Emergency Phones', help='Emergency Phones')


class ItineraryOvernight(models.Model):
    """Voucher of Service Overnight"""
    _description = """
    Overnight for itinerary
    """
    _name = 'tour.vos_itinerary_overnight'
    _order = 'sequence'
    sequence = fields.Integer('Sequence',
                              help='Sequence for sort visit points.')
    voucherofservice_id = fields.Many2one('tour.voucherofservice',
                                          'Voucher Of Service',
                                          help='Voucher of service')
    visitpoint_ids = fields.One2many('tour.vos_visitpoint',
                                     'overnight_id',
                                     'Visit Points',
                                     help='Visit Points on ititnerary')
    visitpoint_id = fields.Many2one('tour.visit_point', 'Location')
    date = fields.Date("Date", help="Location of overnight place")


class ItineraryVisitpoint(models.Model):
    """Voucher of Service Visit Point"""
    _description = """ Visit point of ititnerary """
    _name = "tour.vos_visitpoint"
    overnight_id = fields.Many2one('tour.vos_itinerary_overnight',
                                   'Overnight', help='Overnight')
    hour = fields.Char('Hour', help='Hour of visit')
    breakfast = fields.Boolean('Breakfast', help='Is breakfast offered?')
    lunch = fields.Boolean('Lunch', help='Is lunch offered?')
    dinner = fields.Boolean('Dinner', help='Is dinner offered?')
    visitpoint_id = fields.Many2one('tour.visit_point', 'Visit Point',
                                    help='Visit point')
    """
    location_id = fields.Related('visitpoint_id', 'location_id',
        string='Location',
        readonly='True', type='many2one', relation='tour.location'
        , help='Location of visit point')
    """
    note = fields.Char('Note', help='Useful note')
