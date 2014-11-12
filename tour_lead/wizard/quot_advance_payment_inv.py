
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

from openerp.osv import fields, osv
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
import pdb
class quot_advance_payment_inv(osv.TransientModel):
    _name = "quot.advance.payment.inv"
    _description = "Lead Advance Payment Quotation"

    def _get_default_shop(self, cr, uid, context=None):
        company_id = self.pool.get('res.users').browse(cr, uid, uid, context=context).company_id.id
        shop_ids = self.pool.get('sale.shop').search(cr, uid, [('company_id','=',company_id)], context=context)
        if not shop_ids:
            raise osv.except_osv(_('Error!'), _('There is no default shop for the current user\'s company!'))
        return shop_ids[0]

    _columns = {
        'shop_id': fields.many2one('sale.shop', 'Shop', required=True),
    }

    _defaults = {
        'shop_id': _get_default_shop,
            }

    def _prepare_quot(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        result = []
        lead_obj = self.pool.get('crm.lead')
        pricelist_obj = self.pool.get('product.pricelist')
        inv_line_obj = self.pool.get('sale.order.line')
        lead_ids = context.get('active_ids', [])
        partner_obj = self.pool.get('res.partner')
        wizard = self.browse(cr, uid, ids[0], context)
        shop_obj = self.pool.get('sale.shop')
        result = []
        for lead in lead_obj.browse(cr, uid, lead_ids, context=context):
            pricelist = wizard.shop_id.pricelist_id
            lang = lead.partner_id.lang
            context_partner = {'lang': lang, 'partner_id': lead.partner_id}
            inv_line_values_tot = []
            for acco_line_id in lead.acco_line_ids:
                #FIXME Corregir el precio para que tome de la linea
                product = acco_line_id.product_id
                val = inv_line_obj.product_id_change(cr, uid, ids, pricelist.id,
                         product.id, qty=1,uom=False, qty_uos=0, uos=False,
                         name='', partner_id=lead.partner_id.id,lang=False,
                         update_tax=False,date_order=False, packaging=False,
                         fiscal_position=False, flag=False, context=None)
                val['value']['price_unit'] = 50.0
                res = val['value']

                # create the invoice
                inv_line_values = {
                    'name': res.get('name'),
                    'origin': lead.name,
                    'price_unit': res['price_unit'],
                    'quantity': 1.0,
                    'discount': False,
                    'uos_id': False,
                    'product_id': acco_line_id.product_id.id,
                    'product_uos_qty': 1.0,
                    'invoice_line_tax_id': False,
                    'account_analytic_id': False,
                }
                inv_line_values_tot.append((0, 0, inv_line_values))
            inv_values = {
                'name': lead.name,
                'origin': lead.name,
                'type': 'make_to_order',
                'reference': False,
                'account_id': lead.partner_id.property_account_receivable.id,
                'partner_id': lead.partner_id.id,
                'partner_shipping_id': lead.partner_id.id,
                'partner_invoice_id': lead.partner_id.id,
                'pricelist_id': pricelist.id,
                'order_line': inv_line_values_tot,
                'comment': '',
            }
            result.append((lead.id, inv_values))
        return result

    def open_quotations(self, cr, uid, ids, quotation_ids, context=None):
        """ open a view on one of the given invoice_ids """
        ir_model_data = self.pool.get('ir.model.data')
        form_res = ir_model_data.get_object_reference(cr, uid, 'sale',
                'view_order_form')
        form_id = form_res and form_res[1] or False
        tree_res = ir_model_data.get_object_reference(cr, uid, 'sale',
                'view_quotation_tree')
        tree_id = tree_res and tree_res[1] or False

        return {
            'name': _('Advance Sale'),
            'view_type': 'form',
            'view_mode': 'form,tree',
            'res_model': 'account.invoice',
            'res_id': quotation_ids[0],
            'view_id': False,
            'views': [(form_id, 'form'), (tree_id, 'tree')],
            #'context': "{'type': 'out_invoice'}",
            'type': 'ir.actions.act_window',
        }

    def _create_quotations(self, cr, uid, inv_values, sale_id, context=None):
        sale_obj = self.pool.get('sale.order')
        lead_obj = self.pool.get('crm.lead')
        print inv_values
        sale_id = sale_obj.create(cr, uid, inv_values, context=context)
        # add the invoice to the sales order's invoices
        #FIXME Agregar el campo sale_id en el lead
        #lead_obj.write(cr, uid, sale_id, {'sale_ids': [(4, sale_id)]}, context=context)
        return sale_id

    def create_quot(self, cr, uid, ids, context=None):
        """ create quotations for the active sales orders """
        lead_obj = self.pool.get('crm.lead')
        act_window = self.pool.get('ir.actions.act_window')
        wizard = self.browse(cr, uid, ids[0], context)
        lead_ids = context.get('active_ids', [])
        inv_ids = []
        for lead_id, inv_values in self._prepare_quot(cr, uid, ids, context=context):
            inv_ids.append(self._create_quotations(cr, uid, inv_values, lead_id, context=context))

        return self.open_quotations( cr, uid, ids, inv_ids, context=context)


quot_advance_payment_inv()
