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
from openerp.osv import fields, osv
import time
import netsvc
from openerp.tools.translate import _
#import ir
from mx import DateTime
import datetime
from tools import config
#import pdb

class location(osv.Model):
    _description = """
    Tour location
    """
    _name = "tour.location"
    _columns = {
        'name':fields.char('Name', 255, help='Location name'),
        'description':fields.char('Description', 255, help='Location description'),
    }

class visit_point(osv.Model):
    _description = """
    Tour visit point
    """
    _name = "tour.visit_point"
    _columns={
        'name':fields.char('Name', 255, help='Visit poin name'),
        'location_id':fields.many2one('tour.location', 'Location'
            , help='Visit point location'),
        'description':fields.char('Description', 255, help='Location description'),
    }

class voucher_of_service(osv.Model):
    _description = """
    Voucher of service
    """
    _name="tour.voucherofservice"
    _columns={
        'name':fields.char('Name', 255, help='Name of Voucher of Service'),
        'folio_id':fields.many2one('tour.folio', 'Folio', help='fields help'),
        'passenger_ids':fields.many2many('res.partner',
            'voucherofservice_partner_rel', 'voucherofservice_id',
            'passenger_id', 'Passengers', help='Passengers List'),
        'overnight_ids':fields.one2many('tour.vos_itinerary_overnight'
            , 'voucherofservice_id', 'Visit Points'
            , help='Visit points'),
        'included':fields.text('Included', help='Included items'),
        'excluded':fields.text('Excluded', help='Excluded items'),
        'important_notes':fields.text('Important Notes'
            , help="""Explain the recipient of this document what needs to be
            taken in account so he will be correctly informed.   """),
        'ib_ap_dep_id':fields.many2one('touroperation.airport'
            , 'Departure Airport Inbound'
            , help='Select departure airport inbound'),
        'ib_ap_arr_id':fields.many2one('touroperation.airport'
            , 'Arrival Airport Inbound'
            , help='Select arrival airport inbound'),
        'ib_time_dep':fields.datetime('Departure Inbound Time'),
        'ib_time_arr':fields.datetime('Arrival Inbound Time'),
        'ib_airline_id':fields.many2one('touroperation.airline'
            , 'Departure Airline Inbound'
            , help='Select inbound departure airline'),
        'ib_flight_no':fields.char('Inbound Flight Number'
            , help='Inbound Flight Number'),
        'ob_ap_dep_id':fields.many2one('touroperation.airport'
            , 'Departure Airport Outbound'
            , help='Select outbound departure airport'),
        'ob_ap_arr_id':fields.many2one('touroperation.airport'
            , 'Arrival Airport Outbound'
            , help='Select arrival airport outbound'),
        'ob_time_dep':fields.datetime('Departure Outbound Time'),
        'ob_time_arr':fields.datetime('Arrival Outbound Time'),
        'ob_airline_id':fields.many2one('touroperation.airline'
            , 'Departure Airline Outbound'
            , help='Select departure outbound airline'),
        'ob_flight_no':fields.char('Outbound Flight Number'
            , help='outbound Flight Number'),
        'hotel_contact':fields.text('Emergency Phones', help="""Provide
            information about hotel and contacts."""),
        'emergency_phones':fields.char('Emergency Phones', help='Emergency Phones'),
    }

class voucherofservice_itinerary_overnight(osv.Model):
    _description="""
    Overnight for itinerary
    """
    _name='tour.vos_itinerary_overnight'
    _columns={
        'sequence':fields.integer('Sequence',
        help='Sequence for sort visit points.'),
        'voucherofservice_id':fields.many2one('tour.voucherofservice',
            'Voucher Of Service', help='Voucher of service'),
        'visitpoint_ids':fields.one2many('tour.vos_visitpoint'
            , 'overnight_id', 'Visit Points', help='Visit Points on ititnerary'),
        'visitpoint_id':fields.many2one('tour.visit_point', 'Location'),
        "date" : fields.date("Date", help="Location of overnight place"),
    }
    _order = 'sequence'

class voucherofservice_itinerary_visitpoint(osv.Model):
    _description="""
    Visit point of ititnerary depends of overnight.
    """
    _name="tour.vos_visitpoint"
    _columns={
        'overnight_id':fields.many2one('tour.vos_itinerary_overnight'
            , 'Overnight', help='Overnight'),
        'hour':fields.char('Hour', 10, help='Hour of visit'),
        'breakfast':fields.boolean('Breakfast', help='Is breakfast offered?'),
        'lunch':fields.boolean('Lunch', help='Is lunch offered?'),
        'dinner':fields.boolean('Dinner', help='Is dinner offered?'),
        'visitpoint_id':fields.many2one('tour.visit_point', 'Visit Point',
            help='Visit point'),
        'location_id':fields.related('visitpoint_id', 'location_id',
            string='Location', readonly='True', type='many2one',
            relation='tour.location'
            , help='Location of visit point'),
        'note':fields.char('Note', 255, help='Useful note'),


    }
