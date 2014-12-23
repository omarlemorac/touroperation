# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
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

"""
@author: Accioma
"""
from openerp.osv import osv, fields
import openerp.addons.decimal_precision as dp

class ticket_info(osv.Model):
    """Information lines for flight ticket"""
    _name='tour.ticket.info'
    _columns = {
            'ticket_date':fields.date('Date', help='Date of flight departure'),
            'route':fields.char('Route', 50, help='Route id'),
            'airline':fields.char('Airline', 100, help='Airline name'),
            'flight':fields.char('Flight', 50, help='flight number'),
            'departure':fields.float('Departure', help='Departure'),
            'arrival':fields.float('Arrival', help='Arrival'),
            'ticket_tour_sale_orde_line_id':fields.many2one('ticket.tour.sale.orde.line',
                'Ticket SO Line', help='Ticket Sale Order Line'),




            }
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

