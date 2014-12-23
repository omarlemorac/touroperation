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

class package_price_line(osv.Model):
    """docstring for package_price_line"""
    _name="package.tour.sale.orde.price.line"
    _inherit="tour.price.line"

    _columns={
            'description':fields.char('Description', 255, help='Package description'),
            'package_tour_sale_orde_line_id':fields.many2one("package.tour.sale.orde.line",
               'Order Line'),
            }


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

