# -*- coding: utf-8 -*_

"""
@author: Accioma
"""
from openerp.osv import osv, fields
import openerp.addons.decimal_precision as dp

class service(osv.Model):
    _name = 'tour.service'
    _description = 'Services offered on Tour Folio'

    _columns = {
            'folio_id':fields.many2one('tour.folio', 'Folio'
            , help='Source Document'),
            'cruise_line_ids':fields.one2many('folio_cruise.line', 'folio_id'
                , 'Cuises', help='Cruises'),

    }

class folio_cruise__line(osv.Model):
    """
    Folio cruise line
    """
    _name = "folio_cruise.line"
    _description = "Line of cruise folio in line"
    _inherits = {'tour_folio.line':'tour_folio_line_id'}


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


    def _cost_total(self, cr, uid, ids, field, arg, context=None):
        """Calculates total cost from cost lines"""
        cruise_line_obj = self.browse(cr, uid, ids, context=context)
        res = {}
        for cruise_line in cruise_line_obj:
            total_cost = 0
            for cost_line in cruise_line.cruise_tour_sale_orde_price_line_ids:
                total_cost += cost_line.subtotal_cost
            res[cruise_line.id] = total_cost
        return res


    _columns={
            'service_id':fields.many2one('tour.service', 'Service'
                , help='Service'),
            'folio_id':fields.many2one('tour.folio', 'Folio'
                , help='Folio'),
            'product_id':fields.many2one('product.product', 'Product',
                domain=[('tour_category', '=','cruise')], mandatory=True),
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
            'cruise_cost_total':fields.function(_cost_total,
                method=True,
                type='float',
                store=False,
                fnct_inv=None,
                fnct_search=None,
                string = 'Cost total ',
                help='Total sum of costs'),
            'start_date':fields.date('Start Date', help='Start Date'),
            'end_date':fields.date('End Date', help='End Date'),

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


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
