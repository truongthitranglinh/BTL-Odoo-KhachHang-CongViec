# -*- coding: utf-8 -*-
from odoo import models, fields


class NhanVienExtend(models.Model):
    _inherit = 'nhan_vien'

    khach_hang_ids = fields.One2many('khach_hang', 'nguoi_phu_trach_id', string='Khách hàng phụ trách')