# -*- coding: utf-8 -*_
"""
@author: Accioma
"""
from openerp.osv import osv, fields

class TourPackageHotelBooking(osv.Model):
    """
    @description: Class to manage hotel booking inside a touristic package
    """
    _name="tour.hotelbooking"
    _rec_name="hotel_id"
    _columns={        
        'notes':fields.text('Notes'),
        'checkin_date':fields.date('Check-in Date',
                                   help='Date when customer will check-in'),
        'checkout_date':fields.date('Check-out Date',
                                   help='Date when customer will check-out'),
        'rooms':fields.integer('Rooms',
                               help='Number of rooms wanted for the customer'),
        'hotel_id':fields.many2one('tour.product', string='Hotel',
                                   help='Select the hotel for this booking'),
        'tpkg_id':fields.many2one('tour.package', string='Package',
                                  help='Select the package for this booking')
        }

    
