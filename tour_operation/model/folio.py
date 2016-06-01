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
from openerp import api, exceptions, fields, models
import time
from openerp import netsvc
from openerp.tools.translate import _
from datetime import datetime
#import ir
#from tools import config
import pdb


class tour_folio(models.Model):

    def _incoterm_get(self, cr, uid, context={}):
        return  self.pool.get('sale.order')._incoterm_get(cr, uid, context={})

    def copy(self, cr, uid, id, default=None, context={}):
        return  self.pool.get('sale.order').copy(cr, uid, id, default=None, context={})

    def _invoiced(self, cursor, user, ids, name, arg, context=None):
        return  self.pool.get('sale.order')._invoiced(cursor, user, ids, name, arg, context=None)

    def _invoiced_search(self, cursor, user, obj, name, args):
        return  self.pool.get('sale.order')._invoiced_search(cursor, user, obj, name, args)

    def _amount_untaxed(self, cr, uid, ids, field_name, arg, context):
        return self.pool.get('sale.order')._amount_untaxed(cr, uid, ids, field_name, arg, context)

    def _amount_tax(self, cr, uid, ids, field_name, arg, context):
        return self.pool.get('sale.order')._amount_tax(cr, uid, ids, field_name, arg, context)

    def _amount_total(self, cr, uid, ids, field_name, arg, context):
        return self.pool.get('sale.order')._amount_total(cr, uid, ids, field_name, arg, context)

    _name = 'tour.folio'

    _description = 'Tour Folio Management'

    _inherits = {'sale.order':'order_id'}
    _inherit = ['mail.thread', 'ir.needaction_mixin']

    _rec_name = 'order_id'

    @api.one
    @api.depends('sch_confirm_date')
    def _sch_confirm_date(self):
        if not self.confirm_date:
            self.sch_confirm_date = False
        else:
            days =  datetime.timedelta(days = 1)
            tour_folio_date = datetime.datetime.strptime(
                    self.sch_confirm_date, '%Y-%m-%d') - days
            self.sch_confirm_date = tour_folio_date.strftime('%Y-%m-%d')

    @api.one
    @api.depends('sch_payment_date')
    def sch_payment_date_fcn(self):
        if not self.payment_date:
           self.sch_payment_date = False
        else:
            days =  datetime.timedelta(days = 1)
            tour_folio_date = datetime.datetime.strptime(
                    self.payment_date, '%Y-%m-%d') - days
            self.sch_payment_date = tour_folio_date.strftime('%Y-%m-%d')

    @api.one
    @api.depends('sch_paid_date')
    def sch_paid_date_fcn(self, cr, uid, ids, field_name, arg, context=None):
        if not self.paid_date:
           self.sch_paid_date = False
        else:
            days =  datetime.timedelta(days = 1)
            tour_folio_date = datetime.datetime.strptime(
                    self.paid_date, '%Y-%m-%d') - days
            self.sch_paid_date = tour_folio_date.strftime('%Y-%m-%d')

    @api.one
    @api.depends('unverified_payment_amount_total','unverified_outstanding_balance',
                 'folio_uv_customer_payment_ids','amount_untaxed')
    def _get_unverified_payment(self):
        if self.folio_uv_customer_payment_ids:
            amount = reduce(lambda x,y: x+y, self.folio_uv_customer_payment_ids) or 0.0
            self.unverified_payment_amount_total = amount
            self.unverified_outstanding_balance = self.amount_untaxed - amount

        if self.folio_v_customer_payment_ids:
            amount = reduce(lambda x, y: x+y, self.folio_v_customer_payment_ids) or 0.0
            self.verified_payment_amount_total = amount
            self.verified_outstanding_balance = self.amount_untaxed - amount


    order_id = fields.Many2one('sale.order', 'order_id', required=True, ondelete='cascade')
    arrival_date = fields.Datetime('Arrival', required=True, readonly=True, states={'draft':[('readonly', False)]})
    departure_date = fields.Datetime('Departure', required=True, readonly=True, states={'draft':[('readonly', False)]})
    tour_folio_line_ids = fields.One2many('tour_folio.line', 'folio_id')
    folio_uv_customer_payment_ids = fields.One2many('tour_folio.customerpayment'
          , 'folio_id'
          , help='Register custormer payments for this folio')
    tour_policy = fields.Selection([('prepaid', 'On Booking'), ('manual',
          'On Check In'), ('picking', 'On Departure')], 'Tour Policy'
          , default='manual', required=True)
    duration = fields.Float('Duration')
    confirm_date = fields.Date('Option Date', required=True
      , help='Deadline for option')
    payment_date = fields.Date('Deposit Date', required=False
      , help='Deadline for deposit')
    paid_date = fields.Date('Balance Date', required=False
      , help='Deadline of fully paid service ')
    payment_notes = fields.Text('Payment Notes')
    folio_v_customer_payment_ids = fields.One2many('account.voucher', 'folio_id'
          , 'Advance Payments', help='Advance payments for this folio', readonly=True)
    sch_confirm_date = fields.Date(compute="_sch_confirm_date"
          , string='Scheduled Option Date')
    sch_payment_date = fields.Date(compute="sch_payment_date_fcn"
          , string='Scheduled Deposit Date')
    sch_paid_date = fields.Date(compute="sch_paid_date_fcn"
          , string='Scheduled Balance Date')
    percentage_of_deposit = fields.Float('Percentage of Deposit',
            help='Percentage of first deposit')
    unverified_payment_amount_total = fields.Float(compute="_get_unverified_payment"
          , string='UV Payment', multi=True)
    unverified_outstanding_balance = fields.Float(compute="_get_unverified_payment"
          , string='UV Balance', multi=True)
    verified_payment_amount_total = fields.Float(compute="_get_unverified_payment"
          , string='Verified Payment', multi=True)
    verified_outstanding_balance = fields.Float(compute="_get_unverified_payment"
          , string='Verified Balance', multi=True)


    def print_quotation(self, cr, uid, ids, context=None):
        '''
        This function prints the sales order and mark it as sent, so that we can see more easily the next step of the workflow
        '''
        assert len(ids) == 1, 'This option should only be used for a single id at a time'
        self.signal_workflow(cr, uid, ids, 'quotation_sent')
        return self.pool['report'].get_action(cr, uid, ids, 'tour_operation.report_folio_invoice', context=context)

    @api.one
    @api.constrains('arrival_date','departure_date')
    def check_in_out_date(self):
        if self.arrival_date >= self.departure_date:
            raise exceptions.ValidationError(_("Check in Date Should be less than the Check Out Date!"))

    def name_get(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        res = []
        for record in self.browse(cr, uid, ids, context=context):
            res.append((record.id, record.name))
        return res

    @api.onchange('duration','arrival_date', 'departure_date')
    def onchange_dates(self):
        if self.arrival_date and self.departure_date:
            chkin_dt = datetime.strptime(self.arrival_date, '%Y-%m-%d %H:%M:%S')
            chkout_dt = datetime.strptime(self.departure_date, '%Y-%m-%d %H:%M:%S')
            duration_delta = chkout_dt - chkin_dt
            print duration_delta.days
            self.duration = duration_delta.days

    @api.model
    def create(self, vals):
        vals['order_policy'] = vals.get('tour_policy', 'manual')
        s = self.env['ir.sequence'].get('sale.order') or '/'
        n = self.env['tour_folio.config'].browse(1)
        vals['name'] = "{}{}".format(s,vals['name'])
        #folio = self.browse(cr, uid, ids[0], context = context)
        cd = ""
        if vals['payment_date']:
            cd = time.strftime('%d %B %Y', time.strptime(vals['payment_date'],
                '%Y-%m-%d'))
        bd = ""
        if vals['paid_date']:
            bd = time.strftime('%d %B %Y', time.strptime(vals['paid_date'],
                '%Y-%m-%d'))
        pod = 0.0

        if 'percentage_of_deposit' in vals.keys() and vals['percentage_of_deposit']:
                pod = vals['percentage_of_deposit']
        pob = 100.0 - pod

        if not vals.has_key("folio_id"):
            folio_id = super(tour_folio, self).create(vals)
            vals['note'] = n.note.format(
                                         percentage_of_deposit = pod,
                                         percentage_of_balance = 100 - pod,
                                         amount_of_deposit = folio_id.amount_total * \
                                             pod / 100,
                                         amount_of_balance = folio_id.amount_total * \
                                             pob / 100,
                                         confirm_date = cd,
                                         balance_date = bd,
                                        )
            folio_id.write(vals)
        else:
            folio_id = super(tour_folio, self).create(vals)

        return folio_id


    def onchange_shop_id(self, cr, uid, ids, shop_id):
        return  self.pool.get('sale.order').onchange_shop_id(cr, uid, ids, shop_id)

    def onchange_partner_id(self, cr, uid, ids, part, context=None):
        if context is None:
            context = {}
        a = self.pool.get('sale.order').onchange_partner_id(cr, uid, ids, part, context)
        return a


    def onchange_pricelist_id(self, cr, uid, ids, pricelist_id, order_lines,
            context=None):
        return self.pool.get('sale.order').onchange_pricelist_id(
                                cr,uid,ids,pricelist_id,order_lines)


    def button_dummy(self, cr, uid, ids, context={}):
        return  self.pool.get('sale.order').button_dummy(cr, uid, ids, context={})

    def action_invoice_create(self, cr, uid, ids, grouped=False, states=['confirmed', 'done']):
        i = self.pool.get('sale.order').action_invoice_create(cr, uid, ids, grouped=False, states=['confirmed', 'done'])
        for line in self.browse(cr, uid, ids, context={}):
            self.write(cr, uid, [line.id], {'invoiced':True})
            if grouped:
               self.write(cr, uid, [line.id], {'state' : 'progress'})
            else:
               self.write(cr, uid, [line.id], {'state' : 'progress'})
        return i


    def action_invoice_cancel(self, cr, uid, ids, context={}):
        res = self.pool.get('sale.order').action_invoice_cancel(cr, uid, ids, context={})
        for sale in self.browse(cr, uid, ids):
            for line in sale.order_line:
                self.pool.get('sale.order.line').write(cr, uid, [line.id], {'invoiced': invoiced})
        self.write(cr, uid, ids, {'state':'invoice_except', 'invoice_id':False})
        return res

    def action_cancel(self, cr, uid, ids, context={}):
        c = self.pool.get('sale.order').action_cancel(cr, uid, ids, context={})
        ok = True
        for sale in self.browse(cr, uid, ids):
            for r in self.read(cr, uid, ids, ['picking_ids']):
                for pick in r['picking_ids']:
                    wf_service = netsvc.LocalService("workflow")
                    wf_service.trg_validate(uid, 'stock.picking', pick, 'button_cancel', cr)
            for r in self.read(cr, uid, ids, ['invoice_ids']):
                for inv in r['invoice_ids']:
                    wf_service = netsvc.LocalService("workflow")
                    wf_service.trg_validate(uid, 'account.invoice', inv, 'invoice_cancel', cr)

        self.write(cr, uid, ids, {'state':'cancel'})
        return c

    def action_wait(self, cr, uid, ids, *args):
        res = self.pool.get('sale.order').action_wait(cr, uid, ids, *args)
        for o in self.browse(cr, uid, ids):
            if (o.order_policy == 'manual') and (not o.invoice_ids):
                self.write(cr, uid, [o.id], {'state': 'manual'})
            else:
                self.write(cr, uid, [o.id], {'state': 'progress'})
        return res
    def test_state(self, cr, uid, ids, mode, *args):
        write_done_ids = []
        write_cancel_ids = []
        res = self.pool.get('sale.order').test_state(cr, uid, ids, mode, *args)
        if write_done_ids:
            self.pool.get('sale.order.line').write(cr, uid, write_done_ids, {'state': 'done'})
        if write_cancel_ids:
            self.pool.get('sale.order.line').write(cr, uid, write_cancel_ids, {'state': 'cancel'})
        return res
    def procurement_lines_get(self, cr, uid, ids, *args):
        res = self.pool.get('sale.order').procurement_lines_get(cr, uid, ids, *args)
        return  res
    def action_ship_create(self, cr, uid, ids, *args):
        res = self.pool.get('sale.order').action_ship_create(cr, uid, ids, *args)
        return res
    def action_ship_end(self, cr, uid, ids, context={}):
        res = self.pool.get('sale.order').action_ship_end(cr, uid, ids, context={})
        for order in self.browse(cr, uid, ids):
            val = {'shipped':True}
            self.write(cr, uid, [order.id], val)
        return res
    def _log_event(self, cr, uid, ids, factor=0.7, name='Open Order'):
        return  self.pool.get('sale.order')._log_event(cr, uid, ids, factor=0.7, name='Open Order')
    def has_stockable_products(self, cr, uid, ids, *args):
        return  self.pool.get('sale.order').has_stockable_products(cr, uid, ids, *args)
    def action_cancel_draft(self, cr, uid, ids, *args):
        d = self.pool.get('sale.order').action_cancel_draft(cr, uid, ids, *args)
        self.write(cr, uid, ids, {'state':'draft', 'invoice_ids':[], 'shipped':0})
        self.pool.get('sale.order.line').write(cr, uid, ids, {'invoiced':False, 'state':'draft', 'invoice_lines':[(6, 0, [])]})
        return d


    def action_button_confirm(self, cr, uid, ids, context=None):

        assert len(ids) == 1, 'This option should only be used for a single id at a time.'
        ir_model_data = self.pool.get('ir.model.data')
        try:
            wizard_id = ir_model_data.get_object_reference(cr, uid,
                    'touroperation.confirm.wizard', 'tourfolio_wizard_confirm_view')[1]
        except ValueError:
            wizard_id = False

        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'tourfolio.confirm.wizard',
            'views': [(wizard_id, 'form')],
            'view_id': wizard_id,
            'target': 'new',
        }
        #return super(tour_folio, self).write(cr, uid, ids, vals, context)


    def write(self, cr, uid, ids, vals, context = None):
        if not context:
            context = {}
        folio = self.browse(cr, uid, ids[0], context = context)
        n = self.pool.get('tour_folio.config').browse(cr, uid, 1)
        cd = ""
        if 'payment_date' in vals.keys() and vals['payment_date']:
            cd = time.strftime('%d %B %Y', time.strptime(vals['payment_date'],
                '%Y-%m-%d'))
        bd = ""
        if 'paid_date' in vals.keys() and vals['paid_date']:
            bd = time.strftime('%d %B %Y', time.strptime(vals['paid_date'],
                '%Y-%m-%d'))
        pod = 0.0
        if 'percentage_of_deposit' in vals.keys() and vals['percentage_of_deposit']:
                pod = vals['percentage_of_deposit']
        pob = 100.0 - pod
        #pdb.set_trace()
        vals['note'] = n.note.format(
            percentage_of_deposit = pod,
            percentage_of_balance = 100 - pod,
            amount_of_deposit = folio.amount_total * \
                pod / 100,
            amount_of_balance = folio.amount_total * \
                pob / 100,
            confirm_date = cd,
            balance_date = bd,
            )
        return super(tour_folio, self).write(cr, uid, ids, vals, context)

class tour_folio_line(models.Model):

    def copy(self, cr, uid, id, default=None, context={}):
        return  self.pool.get('sale.order.line').copy(cr, uid, id, default=None, context={})
    def _amount_line_net(self, cr, uid, ids, field_name, arg, context):
        return  self.pool.get('sale.order.line')._amount_line_net(cr, uid, ids, field_name, arg, context)
    def _amount_line(self, cr, uid, ids, field_name, arg, context):
        return  self.pool.get('sale.order.line')._amount_line(cr, uid, ids, field_name, arg, context)
    def _number_packages(self, cr, uid, ids, field_name, arg, context):
        return  self.pool.get('sale.order.line')._number_packages(cr, uid, ids, field_name, arg, context)
    def _get_1st_packaging(self, cr, uid, context={}):
        return  self.pool.get('sale.order.line')._get_1st_packaging(cr, uid, context={})
    @api.one
    def _get_arrival_date(self, cr, uid, context={}):
        if 'arrival_date' in context:
            return context['arrival_date']
        return time.strftime('%Y-%m-%d %H:%M:%S')
    def _get_departure_date(self, cr, uid, context={}):
        if 'arrival_date' in context:
            return context['departure_date']
        return time.strftime('%Y-%m-%d %H:%M:%S')

    _name = 'tour_folio.line'
    _description = 'tour folio line'
    _inherits = {'sale.order.line':'order_line_id'}

    order_line_id=fields.Many2one('sale.order.line', 'order_line_id', required=True, ondelete='cascade')
    folio_id=fields.Many2one('tour.folio', 'folio_id', ondelete='cascade')
    arrival_date = fields.Datetime('Arrival', default=_get_arrival_date,
            required=False)
    departure_date = fields.Datetime('Departure', default=_get_arrival_date,
            required=False)
    option_date = fields.Date('Option Date', required=True, default=time.strftime('%Y-%m-%d %H:%M:%S'))
    deposit_date = fields.Date('Deposit Date', required=True, default=time.strftime('%Y-%m-%d %H:%M:%S'))
    balance_date = fields.Date('Balance Date', required=True, default=time.strftime('%Y-%m-%d %H:%M:%S'))

    @api.model
    def create(self, vals):
        if vals.has_key("folio_id"):
            folio = self.env["tour.folio"].browse([vals['folio_id']])[0]
            vals.update({'order_id':folio.order_id.id})
        roomline = super(tour_folio_line, self).create(vals)
        return roomline

    def uos_change(self, cr, uid, ids, product_uos, product_uos_qty=0, product_id=None):
        return  self.pool.get('sale.order.line').uos_change(cr, uid, ids, product_uos, product_uos_qty=0, product_id=None)

    def product_id_change(self, cr, uid, ids, pricelist, product, qty=0,
            uom=False, qty_uos=0, uos=False, name='', partner_id=False,
            lang=False, update_tax=True, date_order=False):
        return  self.pool.get('sale.order.line').product_id_change(cr, uid, ids, pricelist, product, qty=0,
            uom=False, qty_uos=0, uos=False, name='', partner_id=partner_id,
            lang=False, update_tax=True, date_order=False)

    def product_uom_change(self, cursor, user, ids, pricelist, product, qty=0,
            uom=False, qty_uos=0, uos=False, name='', partner_id=False,
            lang=False, update_tax=True, date_order=False):
        return  self.pool.get('sale.order.line').product_uom_change(cursor, user, ids, pricelist, product, qty=0,
            uom=False, qty_uos=0, uos=False, name='', partner_id=partner_id,
            lang=False, update_tax=True, date_order=False)

    def on_change_checkout(self, cr, uid, ids, arrival_date=time.strftime('%Y-%m-%d %H:%M:%S'), departure_date=time.strftime('%Y-%m-%d %H:%M:%S'), context=None):
        qty = 1
        if departure_date < arrival_date:
            raise osv.except_osv ('Error !', 'Departure must be greater or equal checkin date')
        if arrival_date:
            diffDate = datetime.datetime(*time.strptime(departure_date, '%Y-%m-%d %H:%M:%S')[:5]) - datetime.datetime(*time.strptime(arrival_date, '%Y-%m-%d %H:%M:%S')[:5])
            qty = diffDate.days
            if qty == 0:
                qty = 1
        return {'value':{'product_uom_qty':qty}}

    def button_confirm(self, cr, uid, ids, context={}):

        return  self.pool.get('sale.order.line').button_confirm(cr, uid, ids, context={})
    def button_done(self, cr, uid, ids, context={}):
        res = self.pool.get('sale.order.line').button_done(cr, uid, ids, context={})
        wf_service = netsvc.LocalService("workflow")
        res = self.write(cr, uid, ids, {'state':'done'})
        for line in self.browse(cr, uid, ids, context):
            wf_service.trg_write(uid, 'sale.order', line.order_id.id, cr)
        return res


    def uos_change(self, cr, uid, ids, product_uos, product_uos_qty=0, product_id=None):
        return  self.pool.get('sale.order.line').uos_change(cr, uid, ids, product_uos, product_uos_qty=0, product_id=None)
    def copy(self, cr, uid, id, default=None, context={}):
        return  self.pool.get('sale.order.line').copy(cr, uid, id, default=None, context={})

class folio_customer_payment(models.Model):
    _name = 'tour_folio.customerpayment'
    _description = 'Customer payment voucher and notification'

    name = fields.Char('Memo', help='Memo')
    reference = fields.Char('Reference', help='Reference')
    folio_id = fields.Many2one('tour.folio', 'folio_id', ondelete='cascade')
    payment_date = fields.Date('Option Date', required=True)
    amount = fields.Float('Amount', help='Amount of customer payment')
    journal_id = fields.Many2one('account.journal', 'Payment Method',
        help='Use this payment method')

    def create(self, cr, uid, vals, context=None, check=True):
        folio_customer_payment_id = super(folio_customer_payment,
                self).create(cr,uid,vals,context)
        invoice_payment_ids = self.pool.get('ir.module.category').search(
                cr,uid,[('name','=', 'Accounting')], context=None)[0]

        users = self.pool.get('res.groups').browse(cr, uid, invoice_payment_ids,
                context=None).users
        recipient_partners = []
        for user in users:
            recipient_partners.append((4, user.partner_id.id))

        payment = self.browse(cr, uid, [folio_customer_payment_id])[0]
        folio = self.pool.get('tour.folio')

        message = _('Se ha registrado un pago por {: .2f} para el {}'.format(
            payment.amount, payment.payment_date))
        post_vars = {
            'subject':'New payment created',
            'body':message,
            'partner_ids':recipient_partners,
        }
        folio.message_post(cr,uid,[payment.folio_id.id],
                subtype='mt_comment',
                context=None,**post_vars)



#        thread_pool = payment.folio_id.pool.get('mail.thread')
#        thread_pool.message_post(
#                cr, uid, [payment.folio_id.id],
#                type='notification',
#                subtype='mt_comment',
#                context=None,
#                **post_vars)

        return folio_customer_payment_id

class account_voucher(models.Model):
    _inherit = 'account.voucher'
    folio_id = fields.Many2one('tour.folio', 'Folio'
        , help='Referenced Folio')

    def write(self, cr, uid, ids, vals, context=None):
        write_res = super(account_voucher, self).write(cr, uid, ids, vals, context=None)
        folio_pool = self.pool.get('tour.folio')
        voucher_obj = self.browse(cr, uid, ids)

        for my_voucher in voucher_obj:
            folio = my_voucher.folio_id
            residual = folio.amount_total
            for voucher in folio.folio_v_customer_payment_ids:
                if voucher.state == 'posted':
                    residual -= voucher.amount
            if residual <= 0:
                folio_pool.write(cr, uid, [folio.id], {'state':'progress'})
            elif residual < folio.amount_total:
                folio_pool.write(cr, uid, [folio.id], {'state':'sent'})

        return write_res

class folio_config(models.Model):
    _name = 'tour_folio.config'

    note = fields.Text('Note', help='Folio note configuration')

class TourFolioConfirmWizard(models.TransientModel):
    _name = "tourfolio.confirm.wizard"

    deposit_date = fields.Date('Deposit Date', required=True, help='Deposit date')


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:



