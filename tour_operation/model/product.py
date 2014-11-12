# -*- coding: utf-8 -*_
"""
@author: Accioma
"""
from openerp.osv import osv, fields

class Product(osv.Model):
    """
    @description: Inheritance of offical Product model
    Adds features of product service for Tour Operators.
    Product attribute must be inside the following list: cruise, hotel, flight ticket, lodge, miscellaneous.
    Every category has its own logic.

    """
    _inherit="product.product"
    _columns={
        'tour_category':fields.selection([
            ('cruise','Cruise'),
            ('fticket','Flight Ticket'),
            ('accommodation','Accommodation'),
            ('lodge','Lodge'),
            ('package','Package'),
            ('transfer','Transfer'),
            ('assistance','Assistance'),
            ('misc','Miscellaneous'),
            ('none','None')
            ], 'Tour Category', required=False)
        ,'sales_commission': fields.float('Sales Commision %', digits=(4,2), help="Percentage over sales")


        #Accommodation
        #
        ,'accommodation_style_id':fields.many2one('tour.accommodation.style', 'Style', help='Choose the style of this accommodation')
        ,'accommodation_class':fields.selection([
            ('1star','1 Star'),
            ('2star','2 Stars'),
            ('3star','3 Stars'),
            ('4star','4 Stars'),
            ('5star','5 Stars'),
            ], 'Class', required=False)
        ,'accommodation_sharing':fields.boolean('Sharing')
        ,'accommodation_capacity':fields.integer('Capacity')
        ,'accommodation_location':fields.char('Location', size=255)
        ,'accommodation_room_type_ids':fields.one2many("tour.accommodation.room.type", 'product_id', 'Room Types')
        #
        #Cruise
        #
        ,'cruise_class_id':fields.many2one(
            "tour.cruise.class", "Class",
            help="Choose the class of cruise"
            )
        ,'cruise_style_id':fields.many2one(
            "tour.cruise.style", "Style",
            help="Choose the style of cruise"
            )
        ,'cruise_capacity':fields.integer("Capacity")
        ,'cruise_generic_url':fields.char('Generic Website', size=255)
        ,'cruise_kayak':fields.selection([
            ('inc', 'Included'),
            ('not-inc', 'Not Included'),
            ('not-have', "It doesn't have"),
            ], 'Kayaks', help="Cruise include kayaks?")
        ,'cruise_snorkelling':fields.boolean('Snorkelling',
            help='Check if snorkelling included')
        ,'cruise_wetsuit':fields.boolean('Wetsuite',
            help='Check if wetsuit included')
        ,'cruise_cabin_ids':fields.one2many(
            'tour.cruise.cabin', "product_id", "Cabin",
            help="Choose cabin styles for the cruise"
            )
        ,'cruise_bed_ids':fields.one2many(
            'tour.cruise.bed.type', "product_id",'Bed Type',
            help="Tour bed type available"
            )
        ,'cruise_room_sharing':fields.selection([
            ('yes-sgng',"YES, Same Gender Guaranteed"),
            ('yes-sgng', "YES, Same Gender Not Guaranteed"),
            ('no', "NO"),
            ], 'Room Sharing', help="Choose room sharing available")
        #
        # Lodge
        #
        ,'lodge_capacity':fields.integer("Capacity")
        ,'lodge_generic_url':fields.char("Generic Website", size=255)
        ,'lodge_class_id':fields.many2one("tour.lodge.class"
                , "Class", help="Choose class for lodge")
        ,'lodge_location':fields.char("Location", size=255)
        ,'lodge_language_ids':fields.one2many(
                'tour.language', 'product_id','Language',
                help='Chose language(s) available(s)')
        ,'lodge_has_transportation':fields.boolean('Transportation')

        ,'lodge_room_sharing':fields.selection([
            ('yes-sgng',"YES, Same Gender Guaranteed"),
            ('yes-sgng', "YES, Same Gender Not Guaranteed"),
            ('no', "NO"),
            ], 'Room Sharing', required=False, help="Choose room sharing available")

        ,'lodge_room_type_ids':fields.one2many(
                'tour.lodge.room.type', 'product_id', 'Room Style',
                help='Choose room types'
                )

        #Package
        ,'package_locations':fields.text('Locations')
        ,'package_class':fields.selection([
            ('luxury','Luxury'),
            ('first','First Class'),
            ('tourist_sup','Tourist Superior'),
            ('tourist','Tourist'),
            ('economy','Economy')
            ], 'Class', required=False, help='Select package class')
        ,'package_duration':fields.integer('Duration',
                help='Duration in days')
        ,'package_is_private':fields.boolean('Private')

        ,'package_language_ids':fields.one2many(
                'tour.language', 'product_id','Language',
                help='Chose language(s) available(s)')
        ,'package_has_assistance':fields.boolean('Assistance',
                help='Does this package has assistance?')
        ,'itinerary':fields.binary('Itinerary')
        #Transfers
        ,'transfer_language_ids':fields.one2many(
                'tour.language', 'product_id','Language',
                help='Chose language(s) available(s)')
        ,'transfer_has_assistance':fields.boolean('Assistance',
                help='Has the transfer assistance?')

        }
    _defaults={
        'tour_category':'none'

        }
