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
            'is_pax':fields.boolean('Is Passenger?'
                , help='''Check this field so you can add this contact to list of pax'''),
            'date_of_birth':fields.date('Date of Birth', help='Date of Birth'),
            'wetsuit_size':fields.char("Wetsuit Size", 100
                , help='Select the passenger wetsuit size'),
            'dietary_requirements':fields.text('Dietary Requirements'
                , help='Passenger dietary requirements'),
            'allergies_medical':fields.text('Allergies or Medical Conditions'
                , help='Allergies or medical conditions'),
            'marital_status':fields.selection([('single', 'Single'),
                ('married', 'Married'),('divorced', 'Divorced'),
                ('widowed', 'Widowed'),('separated', 'Separated'),
                ('living_common_law', 'Living common law'),
                ('other', 'Other/Not specified')
                ], string="Martial Status",
                help="Choose martial status"),
            'gender':fields.selection([('m', 'Male'), ('f', 'Female')],
                string="Gender", help="Passenger gender"),
            'nationality_id':fields.many2one('res.country', 'Nationality',
                help='Passenger nationality'),


            }

