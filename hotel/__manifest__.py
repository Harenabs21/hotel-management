
{
    'name': "hotel",

    'summary': "Hotel management",

    'description': """
Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    'category': 'Hostel industry',
    'version': '0.1',

    'depends': ['base','web'],
    'icon': '/hotel/static/src/icons/hotel.png',

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/hotel_booking_sequence.xml',
        'views/hotel_room_equipment_views.xml',
        'views/hotel_room_type_views.xml',
        'views/hotel_room_views.xml',
        'views/hotel_room_booking_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

