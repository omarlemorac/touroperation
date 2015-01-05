# -*- coding: utf-8 -*-
{
    "name":"Tour Lead",
    "description":"""\
Detailed leads for tour operation
_____________________________________________

- Manage tour leads:
  Cruises, accommodations, flight tickets, lodges, transfers, miscellaneous.
- Travel itinerary.
- Sale order creation. TODO:
- Account invoice integration. TODO:
    """,
    "category":"Tour & Travel Operation",
    "author":"Accioma",
    "data":[
        'wizard/quot_advance_payment_inv.xml',
        'views/crm_lead_view.xml',
        'views/partner_view.xml',
        'security/res_groups.xml',
        'report/report_opportunity.xml',
        'security/ir.model.access.csv',
           ],

    "depends":["base", "sale", "crm","report_webkit","tour_operation"],
    "installable":True
}
