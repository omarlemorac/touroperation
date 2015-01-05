# -*- coding: utf-8 -*_
"""
@author: Accioma
"""
from openerp.osv import osv, fields

class res_partner(osv.Model):

    '''
    Add pax feature to res_partner
    '''

    _name = 'res.partner'
    _inherit = 'res.partner'

    _columns = {
            'is_pax':fields.boolean('Is Pax?'
                , help='''Check this field so you can add this contact to list of pax'''),
            'lead_pax_id':fields.many2one('crm.lead', 'Lead', help='Used to add pax'),
            }

