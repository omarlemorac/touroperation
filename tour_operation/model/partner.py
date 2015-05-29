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
            'passport_number':fields.char('Passport Number', 50
                , help='Passenger passport number'),
            'date_of_birth':fields.date('Date of Birth', help='Date of Birth'),
            'shoe_size':fields.char('Shoe Size', 10
                , help='Shoe Size'),
            'clothing_size':fields.selection(
                [('xs', 'XS'),('s', 'S'),('m', 'M'),('l', 'L'),('xl', 'XL'),
                 ('xxl', 'XXL'),
                ], string = "Clothing Size"
                , help='Select the passenger clothing size'),
            'dietary_requirements':fields.text('Dietary Requirements'
                , help='Passenger dietary requirements'),
            'allergies_medical':fields.text('Allergies or Medical Conditions'
                , help='Allergies or medical conditions'),

            }

