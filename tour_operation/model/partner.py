# -*- coding: utf-8 -*_
"""
@author: Accioma
"""
from openerp import api, exceptions, fields, models

class res_partner(models.Model):

    '''
    Add pax feature to res_partner
    '''

    _inherit = 'res.partner'

    is_pax = fields.Boolean('Is Passenger?',
            help='''Check this field so you can add this contact to list of pax''')
    date_of_birth = fields.Date('Date of Birth', help='Date of Birth')
    wetsuit_size = fields.Char('Wetsuit Size'
            , help='passenger wetsuit size')
    dietary_requirements = fields.Text('Dietary Requirements',
            help='Passenger dietary requirements')
    allergies_medical = fields.Text('Allergies or Medical Conditions',
            help='Allergies or medical conditions')
    marital_status = fields.Selection([('single', 'Single'),
                ('married', 'Married'),('divorced', 'Divorced'),
                ('widowed', 'Widowed'),('separated', 'Separated'),
                ('living_common_law', 'Living common law'),
                ('other', 'Other/Not specified')],
                string="Martial Status",
                help='Choose martial status')
    gender = fields.Selection([('m', 'Male'), ('f', 'Female')]
           , help='fields help')

    nationality_id = fields.Many2one('res.country', 'Nationality',
            help='Passenger nationality')
