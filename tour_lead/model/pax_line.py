# -*- coding: utf-8 -*_
"""
@author: Accioma
"""

from osv import osv, fields

class pax_line(osv.Model):

    '''
    Allows the creation of lines for pax in *tour_lead*
    referencing *res.partner* module
    '''

    _name = 'tour.lead.paxline'

    _columns = {
            'partner_id':fields.many2one('res.partner', 'Pax',
                domain=[('is_pax', '=', True)],  help='Add a pax'),
            'tour_lead_id':fields.many2one('crm.lead', 'Tour Lead',help='Reference to the *tour_lead*'),
            }

