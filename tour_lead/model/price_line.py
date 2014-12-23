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

#price line
class price_line(osv.Model):
    _name="tour.price.line"

    def _subtotal_price(self, cr, uid, ids, field, arg, context=None):
        """Sum price and cost """
        if not context:
            context = []
        st = lambda q, p : q*p
        price_objs = self.browse(cr, uid, ids, context=context)
        return {po.id:st(po.qtty, po.unit_price) for po in price_objs}

    def _subtotal_cost(self, cr, uid, ids, field, arg, context=None):
        """Sum price and cost """
        if not context:
            context = []
        st = lambda q, p : q*p
        price_objs = self.browse(cr, uid, ids, context=context)
        return {po.id:st(po.qtty, po.unit_cost) for po in price_objs}

    _columns={
            'unit_price': fields.float('Price', required=True,
                digits_compute= dp.get_precision('Product Price'),
                readonly=False ),
            'unit_cost': fields.float('Cost', required=True,
                digits_compute= dp.get_precision('Product Cost'),
                readonly=False ),
            'qtty': fields.float('Units', required=True,
                digits_compute= dp.get_precision('Units'),
                readonly=False ),
            'subtotal_price':fields.function(_subtotal_price,
                method=True,
                type='float',
                store=False,
                fnct_inv=None,
                fnct_search=None, string='Subtotal Price',
                help='Calculated subtotal price'
                ),
            'subtotal_cost':fields.function(_subtotal_cost,
                method=True,
                type='float',
                store=False,
                fnct_inv=None,
                fnct_search=None, string='Subtotal Cost',
                help='Calculated subtotal cost'
                ),

            }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

