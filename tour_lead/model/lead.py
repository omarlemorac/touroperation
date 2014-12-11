# -*- coding: utf-8 -*_
"""
@author: Accioma
"""
from openerp.osv import osv, fields
import openerp.addons.decimal_precision as dp

class crm_lead(osv.Model):
    _inherit="crm.lead"
    def _amount_acco(self, cr, uid, ids, field_name, arg, context=None):
        cur_obj = self.pool.get('res.currency')
        res = {}
        for l in self.browse(cr, uid, ids, context=context):
            val = val1 = 0.0
            for acco_line in l.acco_line_ids:
                val1 += acco_line.total_line_price
            res[l.id] = val1
        return res

    def _amount_cruise(self, cr, uid, ids, field_name, arg, context=None):
        cur_obj = self.pool.get('res.currency')
        res = {}
        for l in self.browse(cr, uid, ids, context=context):
            val = val1 = 0.0
            for cruise_line in l.cruise_line_ids:
                val1 += cruise_line.total_line_price
            res[l.id] = val1
        return res
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
            'acco_amount_total':fields.function(_amount_acco,
                digits_compute=dp.get_precision('Account'),
                string='Accommodation Amount',type='float', method=True),
            'cruise_amount_total':fields.function(_amount_cruise,
                digits_compute=dp.get_precision('Account'),
                string='Cruise Amount',type='float', method=True)
            }


    def button_dummy(self, cr, uid, ids, context=None):
        return True

class sale_order_line(osv.Model):
    """
    @description: Class intended to manage a line of sale order

    """

    def _delta_days(self, end_date, start_date):
        from datetime import datetime as DT
        dateformat = '%Y-%m-%d'
        d1 = DT.strptime(end_date, dateformat)
        d2 = DT.strptime(start_date, dateformat)
        return (d1 - d2).days

    def _fcn_nights_stay(self, cr, uid, ids, field_name, arg, context):
        result = {}
        lines = self.browse(cr, uid, ids, context)
        for l in lines:
            result[l.id] = self._delta_days(l.end_date, l.start_date)
        return result

    def _fcn_total_line_price(self, cr, uid, ids, field_name, arg, context):
        result = {}
        lines = self.browse(cr, uid, ids, context)
        for l in lines:
            nigths_stay = self._delta_days(l.end_date, l.start_date)
            result[l.id] = l.unit_price * l.qtty * nigths_stay
        return result


    _name="tour.sale.order.line"
    _columns={
            'start_date':fields.date('Start date', required=True),
            'end_date':fields.date('End date', required=True),
            'unit_price': fields.float('Price', required=True,
                digits_compute= dp.get_precision('Product Price'),
                readonly=False ),
            'unit_cost': fields.float('Cost', required=True,
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
            'qtty':fields.integer('Units', required=True),
            'acco_type':fields.char('Accommodation type', 100),
            'agent_commission':fields.integer("Agent's commission", required=True),
            'operator':fields.char('Operator', 100),
            'emergency_contact':fields.many2one('res.partner', 'Emergency \
                Contact'),
            'observations':fields.text('Observations'),
            'nigths_stay':fields.function(_fcn_nights_stay, type='integer',
                    string='Nigths Stay', method=True),
            'total_line_price':fields.function(_fcn_total_line_price, type='float',
                    string='Total Price', method=True),
            }

    _defaults={
            'unit_price':0.0,
            'unit_cost':0.0,
            'tour_status':'option',
            'start_date':fields.date.context_today,
            'end_date':fields.date.context_today,
            'limit_date':fields.date.context_today,

            }


    def _end_date_after_start_date(self, cr, uid, ids):
        for line in self.browse(cr, uid, ids):
            if line.start_date > line.end_date:
                return False
        return True

    def _no_date_before_today(self, cr, uid, ids):
        for line in self.browse(cr, uid, ids):
            if fields.date.context_today > line.start_date\
                    or fields.date.context_today > line.end_date\
                    or fields.date.context_today > line.limit_date:
                return False
        return True


    _constraints = [
       (_end_date_after_start_date,
        'End date after start date',
        ['start_date', 'end_date']),
       (_no_date_before_today,
        'No date shall be entered before today',
        ['start_date', 'end_date', 'limit_date']),

        ]

#Cruise price line
class cruise_price_line(osv.Model):
    _name="cruise.tour.sale.orde.price.line"

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
           'cruise_tour_sale_orde_line_id':fields.many2one("cruise.tour.sale.orde.line",
               'Order Line'),
            'cruise_cabin_id':fields.many2one(\
                "tour.cruise.cabin", 'Cabin Type',
                 required=True),
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
                fnct_search=None, string='Subtotal Price',
                help='Calculated subtotal price'
                ),

            }
#Cruise
class cruise_sale_order_line(osv.Model):
    _name="cruise.tour.sale.orde.line"
    _inherit="tour.sale.order.line"
    def _price_total(self, cr, uid, ids, field, arg, context=None):
        """Calculates total price from price lines"""
        cruise_line_obj = self.browse(cr, uid, ids, context=context)
        res = {}
        for cruise_line in cruise_line_obj:
            total_price = 0
            for price_line in cruise_line.cruise_tour_sale_orde_price_line_ids:
                total_price += price_line.subtotal_price
            res[cruise_line.id] = total_price
        return res

    _columns={
            'product_id':fields.many2one('product.product', 'Product',
                domain=[('tour_category', '=','cruise')], mandatory=True),
            'crm_lead_id':fields.many2one('crm.lead', 'Lead'),
            'cruise_generic_url':fields.related('product_id',
                'cruise_generic_url', type='char', string='Generic Website',
                readonly=True),
            'cruise_tour_sale_orde_price_line_ids':\
                    fields.one2many('cruise.tour.sale.orde.price.line',
                'cruise_tour_sale_orde_line_id', 'Price Lines',
                help='Add price lines'),
            'cruise_price_total':fields.function(_price_total,
                method=True,
                type='float',
                store=False,
                fnct_inv=None,
                fnct_search=None,
                string = 'Price total ',
                help='Total sum of prices'),
            }

    def onchange_product_id(self, cr, uid, ids, product, context=None):
        res = {}
        value = {}
        domain = {}
        context = context or {}
        if not product:
            return {'value':{'unit_price':0.0, 'unit_cost':0.0}}
        product_obj = self.pool.get('product.product')
        product_obj = product_obj.browse(cr, uid, product, context=context)
        value.setdefault('unit_price',product_obj.list_price)
        value.setdefault('unit_cost',product_obj.standard_price)
        ccto_ids = [ ccto.id for ccto in
                product_obj.cruise_cabin_ids ]
        domain.setdefault('cruise_cabin_id', [('id', 'in', ccto_ids)])
        res['value'] = value
        res['domain'] = domain
        return {'value':{'unit_price':product_obj.list_price,
            'unit_cost':product_obj.standard_price}}

    def button_dummy(self, cr, uid, ids, context=None):
        return True

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
            return {'value':{'unit_price':0.0, 'unit_cost':0.0}}
        product_obj = self.pool.get('product.product')
        product_obj = product_obj.browse(cr, uid, product, context=context)
        value.setdefault('unit_price',product_obj.list_price)
        value.setdefault('unit_cost',product_obj.standard_price)
        arto_ids = [ arto.id for arto in
                product_obj.accommodation_room_type_ids ]
        domain.setdefault('accommodation_room_type_id', [('id', 'in', arto_ids)])
        res['value'] = value
        res['domain'] = domain

        return res

