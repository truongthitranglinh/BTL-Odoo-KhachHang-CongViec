# -*- coding: utf-8 -*-
{
    'name': "quan_ly_khach_hang",

    'summary': """
        Module quản lý khách hàng""",

    'description': """
        Module quản lý thông tin khách hàng, theo dõi các tương tác và hoạt động bán hàng.
        Bao gồm quản lý thông tin liên hệ, lịch sử tương tác và các giao dịch.
    """,

    'author': "pnguyen",
    'website': "http://www.yourcompany.com",

    'category': 'Sales',
    'version': '0.1',

    'depends': ['base', 'nhan_su'],

    'data': [
        'security/ir.model.access.csv',
        'views/khach_hang.xml',
        'views/hop_dong.xml',
        'views/phan_hoi.xml',
        'views/khach_hang_phan_hoi.xml',
        'views/chien_dich.xml',
        'views/nhan_vien_extend.xml',
        'data/cron.xml',
        'views/menu.xml',
    ],

    'demo': [],
    'installable': True,
    'application': True,
}