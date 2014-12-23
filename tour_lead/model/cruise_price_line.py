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

#Cruise price line
class cruise_price_line(osv.Model):
    _name="cruise.tour.sale.orde.price.line"
    _inherit="tour.price.line"

    _columns={
           'cruise_tour_sale_orde_line_id':fields.many2one("cruise.tour.sale.orde.line",
               'Order Line'),
            'cruise_cabin_id':fields.many2one(\
                "tour.cruise.cabin", 'Cabin Type',
                 required=True),
            }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

