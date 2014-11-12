# -*- coding: utf-8 -*_
"""
@author: Accioma
"""
from openerp.osv import osv, fields
import openerp.addons.decimal_precision as dp

class crm_lead(osv.Model):
    _inherit="crm.lead"
    _columns={
            'acco_line_ids':fields.one2many('accommodation.tour.sale.orde.line',
                'crm_lead_id','Accommodation'
                ),
            'cruise_line_ids':fields.one2many('cruise.tour.sale.orde.line',
                'crm_lead_id','Cruise'
                ),
            'fticket_line_ids':fields.one2many('ticket.tour.sale.orde.line',
                'crm_lead_id','Ticket'
                ),
            'lodge_line_ids':fields.one2many('lodge.tour.sale.orde.line',
                'crm_lead_id','Lodge'
                ),
            'package_line_ids':fields.one2many('package.tour.sale.orde.line',
                'crm_lead_id','Package'
                ),
            'transfer_line_ids':fields.one2many('transfer.tour.sale.orde.line',
                'crm_lead_id','Transfer'
                ),
            'assistance_line_ids':fields.one2many('assistance.tour.sale.orde.line',
                'crm_lead_id','Assistance'
                ),
            'misc_line_ids':fields.one2many('misc.tour.sale.orde.line',
                'crm_lead_id','Miscellaneous'
                ),
            }

class sale_order_line(osv.Model):
    """
    @description: Class intended to manage a line of sale order

    """
    _name="tour.sale.order.line"
    _columns={
            'start_date':fields.date('Start date', required=True),
            'end_date':fields.date('End date', required=True),
            'price': fields.float('Price', required=True,
                digits_compute= dp.get_precision('Product Price'),
                readonly=False ),
            'cost': fields.float('Cost', required=True,
                digits_compute= dp.get_precision('Product Price'),
                readonly=False ),
            'itinerary':fields.text('Itinerary'),
            'tour_status':fields.selection(
                [
                ('option', 'Option'),
                ('block', 'Block'),
                ('confirmed', 'Confirmed'),
                ('confirmed_credit', 'Confirmed Credit'),
                ('full_payment_confirmed', 'Full payment confirmed'),
                ('operating', 'Operating'),
                ('billed', 'Facturado'),
                ('payment_commission', 'Payment commission'),
                ('closed', 'Closed'),
                ('canceled', 'Canceled'),
                ('not_operated', 'Not operated'),
                ],'Status', required=True),
            'limit_date':fields.date('Limit date', required=True),
            'passengers':fields.integer('Passengers', required=True),
            'acco_type':fields.char('Accommodation type', 100),
            'agent_commission':fields.integer("Agent's commission", required=True),
            'operator':fields.char('Operator', 100),
            'emergency_contact':fields.many2one('res.partner', 'Emergency \
                Contact'),
            'observations':fields.text('Observations'),
            }

    _defaults={
            'price':0.0,
            'cost':0.0,
            'tour_status':'option',


            }


#Cruise
class cruise_sale_order_line(osv.Model):
    _name="cruise.tour.sale.orde.line"
    _inherit="tour.sale.order.line"
    _columns={
            'product_id':fields.many2one('product.product', 'Product',
                domain=[('tour_category', '=','cruise')], mandatory=True),
            'crm_lead_id':fields.many2one('crm.lead', 'Lead'),
            }

    def onchange_product_id(self, cr, uid, ids, product, context=None):
        context = context or {}
        if not product:
            return {'value':{'price':0.0, 'cost':0.0}}
        product_obj = self.pool.get('product.product')
        product_obj = product_obj.browse(cr, uid, product, context=context)
        return {'value':{'price':product_obj.list_price,
            'cost':product_obj.standard_price}}

#Lodge
class lodge_sale_order_line(osv.Model):
    _name="lodge.tour.sale.orde.line"
    _inherit="tour.sale.order.line"
    _columns={
            'product_id':fields.many2one('product.product', 'Product', domain=[('tour_category', '=','lodge')]),
            'crm_lead_id':fields.many2one('crm.lead', 'Lead'),
            }
#Package
class package_sale_order_line(osv.Model):
    _name="package.tour.sale.orde.line"
    _inherit="tour.sale.order.line"
    _columns={
            'product_id':fields.many2one('product.product', 'Product', domain=[('tour_category', '=','package')]),
            'crm_lead_id':fields.many2one('crm.lead', 'Lead'),
            }
#Transfer
class transfer_sale_order_line(osv.Model):
    _name="transfer.tour.sale.orde.line"
    _inherit="tour.sale.order.line"
    _columns={
            'product_id':fields.many2one('product.product', 'Product', domain=[('tour_category', '=','transfer')]),
            'crm_lead_id':fields.many2one('crm.lead', 'Lead'),
            }
#Assistance
class assistance_sale_order_line(osv.Model):
    _name="assistance.tour.sale.orde.line"
    _inherit="tour.sale.order.line"
    _columns={
            'product_id':fields.many2one('product.product', 'Product', domain=[('tour_category', '=','assistance')]),
            'crm_lead_id':fields.many2one('crm.lead', 'Lead'),
            }
#Ticket
class ticket_sale_order_line(osv.Model):
    _name="ticket.tour.sale.orde.line"
    _inherit="tour.sale.order.line"
    _columns={
            'product_id':fields.many2one('product.product', 'Product', domain=[('tour_category', '=','fticket')]),
            'crm_lead_id':fields.many2one('crm.lead', 'Lead'),
            }
#Miscellaneous
class misc_sale_order_line(osv.Model):
    _name="misc.tour.sale.orde.line"
    _inherit="tour.sale.order.line"
    _columns={
            'product_id':fields.many2one('product.product', 'Product',
                domain=[('tour_category', '=','misc')]),
            'crm_lead_id':fields.many2one('crm.lead', 'Lead'),
            }
#Accommodation
class accommodation_sale_order_line(osv.Model):
    _name="accommodation.tour.sale.orde.line"
    _inherit="tour.sale.order.line"
    _columns={
            'product_id':fields.many2one('product.product', 'Product', domain=[('tour_category', '=','accommodation')]),
            'crm_lead_id':fields.many2one('crm.lead', 'Lead'),
            'accommodation_room_type_id':fields.many2one(\
                "tour.accommodation.room.type", 'Accommodation Type',
                 required=True),
            }

    def onchange_product_id(self, cr, uid, ids, product, context=None):
        res = {}
        value = {}
        domain = {}
        context = context or {}
        if not product:
            return {'value':{'price':0.0, 'cost':0.0}}
        product_obj = self.pool.get('product.product')
        product_obj = product_obj.browse(cr, uid, product, context=context)
        value.setdefault('price',product_obj.list_price)
        value.setdefault('cost',product_obj.standard_price)
        arto_ids = [ arto.id for arto in
                product_obj.accommodation_room_type_ids ]
        domain.setdefault('accommodation_room_type_id', [('id', 'in', arto_ids)])
        res['value'] = value
        res['domain'] = domain

        return res

        """
        acco_room_type_obj = self.pool.get('tour.accommodation.room.type')
        for arto in acco_room_type_obj:
            print arto
        """
