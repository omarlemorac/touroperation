# -*- coding: utf-8 -*_
"""
@author: Accioma
"""
from openerp.osv import osv, fields

class TourProduct(osv.Model):
    """
    @description: Tour Product model
    Tour product can be a cruise, hotel, flight ticket, lodge, miscellaneous.
    Every category has its own logic.

    """
    _name="tour.product"
    _columns={
        'name':fields.char('Title', size=64, required=True, translate=True),
        'description':fields.text('Description', readonly=False),
        'tour_category':fields.selection([
            ('cruise','Cruise'),
            ('fticket','Flight Ticket'),
            ('hotel','Hotel'),
            ('lodge','Lodge'),
            ('misc','Miscellaneous')
            ], 'Category', required=True),
        'capacity':fields.integer('Capacity'),
        'generic_website':fields.char('Generic Website', size=100),
        'has_transportation':fields.boolean('Transportation', help="Indicate if the facility has transportation")

        }

    def function():
        pass
    
