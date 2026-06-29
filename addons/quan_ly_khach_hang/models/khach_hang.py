# -*- coding: utf-8 -*-
from odoo import models, fields, api
import unicodedata


class KhachHang(models.Model):
    _name = 'khach_hang'
    _description = 'Quản lý thông tin khách hàng'
    _rec_name = 'ten_khach_hang'

    ma_khach_hang = fields.Char("Mã khách hàng", readonly=True, copy=False)
    ten_khach_hang = fields.Char("Tên khách hàng", required=True)
    loai_khach_hang = fields.Selection([
        ('ca_nhan', 'Cá nhân'),
        ('doanh_nghiep', 'Doanh nghiệp')
    ], string="Loại khách hàng", default='ca_nhan', required=True)

    email = fields.Char("Email")
    so_dien_thoai = fields.Char("Số điện thoại", required=True)
    dia_chi = fields.Text("Địa chỉ")
    ngay_sinh = fields.Date("Ngày sinh")

    ma_so_thue = fields.Char("Mã số thuế")
    website = fields.Char("Website")

    trang_thai = fields.Selection([
        ('tiem_nang', 'Tiềm năng'),
        ('da_lien_he', 'Đã liên hệ'),
        ('dang_dam_phan', 'Đang đàm phán'),
        ('thanh_cong', 'Thành công'),
        ('that_bai', 'Thất bại')
    ], string="Trạng thái", default='tiem_nang')

    nguoi_phu_trach_id = fields.Many2one('nhan_vien', string="Người phụ trách")
    ghi_chu = fields.Text("Ghi chú")
    phan_hoi_ids = fields.One2many('phan_hoi', 'khach_hang_id', string='Phan hoi')

    # ===== CẢI TIẾN: Thống kê công việc liên quan =====
    so_cong_viec = fields.Integer(
        "Số công việc",
        compute='_compute_so_cong_viec'
    )

    def _compute_so_cong_viec(self):
        CongViec = self.env.get('cong_viec')
        for rec in self:
            if CongViec is not None:
                rec.so_cong_viec = CongViec.search_count([
                    ('khach_hang_id', '=', rec.id)
                ])
            else:
                rec.so_cong_viec = 0

    def action_tao_lich_hen(self):
        """Tạo lịch hẹn → tự động tạo công việc loại lich_hen"""
        for rec in self:
            nhan_vien = rec.nguoi_phu_trach_id
            if not nhan_vien or not nhan_vien.phong_ban_id:
                continue
            self.env['cong_viec'].create({
                'tieu_de': f"Lịch hẹn với {rec.ten_khach_hang}",
                'loai_cong_viec': 'lich_hen',
                'khach_hang_id': rec.id,
                'phong_ban_phu_trach_id': nhan_vien.phong_ban_id.id,
                'nguoi_thuc_hien_id': nhan_vien.id,
                'mo_ta': f"Lịch hẹn tự động tạo cho khách hàng {rec.ten_khach_hang}",
                'muc_do_uu_tien': 'cao',
                'trang_thai': 'moi',
            })
            rec.write({'trang_thai': 'dang_dam_phan'})
        return {
            'type': 'ir.actions.act_window',
            'name': 'Công việc',
            'res_model': 'cong_viec',
            'view_mode': 'list,form',
            'domain': [('khach_hang_id', 'in', self.ids)],
            'context': {'default_khach_hang_id': self.id},
        }

    def action_tao_bao_gia(self):
        """Tạo báo giá → tự động tạo công việc loại gui_bao_gia"""
        for rec in self:
            nhan_vien = rec.nguoi_phu_trach_id
            if not nhan_vien or not nhan_vien.phong_ban_id:
                continue
            self.env['cong_viec'].create({
                'tieu_de': f"Gửi báo giá cho {rec.ten_khach_hang}",
                'loai_cong_viec': 'gui_bao_gia',
                'khach_hang_id': rec.id,
                'phong_ban_phu_trach_id': nhan_vien.phong_ban_id.id,
                'nguoi_thuc_hien_id': nhan_vien.id,
                'mo_ta': f"Báo giá tự động tạo cho khách hàng {rec.ten_khach_hang}",
                'muc_do_uu_tien': 'cao',
                'trang_thai': 'moi',
            })
        return {
            'type': 'ir.actions.act_window',
            'name': 'Công việc',
            'res_model': 'cong_viec',
            'view_mode': 'list,form',
            'domain': [('khach_hang_id', 'in', self.ids)],
            'context': {'default_khach_hang_id': self.id},
        }

    def action_xem_cong_viec(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Công việc liên quan',
            'res_model': 'cong_viec',
            'view_mode': 'list,form',
            'domain': [('khach_hang_id', '=', self.id)],
            'context': {
                'default_khach_hang_id': self.id,
                'default_nguoi_thuc_hien_id': self.nguoi_phu_trach_id.id,
            },
        }

    def _remove_accents(self, text):
        text = text.replace('Đ', 'D').replace('đ', 'd')
        text = unicodedata.normalize('NFD', text)
        text = text.encode('ascii', 'ignore').decode('utf-8')
        return text

    @api.onchange('ten_khach_hang')
    def _onchange_ma_khach_hang(self):
        if self.ten_khach_hang:
            ten_khong_dau = self._remove_accents(self.ten_khach_hang)
            ma_co_ban = ''.join([word[0].upper() for word in ten_khong_dau.split()])
            ma_co_ban = 'KH' + ma_co_ban
            counter = 1
            ma_khach_hang = f"{ma_co_ban}{counter:02d}"
            while self.search([('ma_khach_hang', '=', ma_khach_hang), ('id', '!=', self.id or 0)], limit=1):
                counter += 1
                ma_khach_hang = f"{ma_co_ban}{counter:02d}"
            self.ma_khach_hang = ma_khach_hang

    @api.model
    def create(self, vals):
        if vals.get('ten_khach_hang'):
            ten_khong_dau = self._remove_accents(vals['ten_khach_hang'])
            ma_co_ban = ''.join([word[0].upper() for word in ten_khong_dau.split()])
            ma_co_ban = 'KH' + ma_co_ban
            counter = 1
            ma_khach_hang = f"{ma_co_ban}{counter:02d}"
            while self.search([('ma_khach_hang', '=', ma_khach_hang)], limit=1):
                counter += 1
                ma_khach_hang = f"{ma_co_ban}{counter:02d}"
            vals['ma_khach_hang'] = ma_khach_hang
        records = super(KhachHang, self).create(vals)
        records._add_birthday_campaign_if_today()
        return records

    def write(self, vals):
        res = super(KhachHang, self).write(vals)
        self._add_birthday_campaign_if_today()
        return res

    def _add_birthday_campaign_if_today(self, today=None):
        today = today or fields.Date.context_today(self)
        if not today:
            return
        birthday_customers = self.filtered(
            lambda c: c.ngay_sinh and (c.ngay_sinh.month, c.ngay_sinh.day) == (today.month, today.day)
        )
        if not birthday_customers:
            return
        Campaign = self.env['chien_dich'].sudo()
        for customer in birthday_customers:
            campaign_name = f"Mừng sinh nhật {customer.ten_khach_hang}"
            campaign = Campaign.search([('ten_chien_dich', '=', campaign_name)], limit=1)
            if not campaign:
                Campaign.create({
                    'ten_chien_dich': campaign_name,
                    'loai_chien_dich': 'khac',
                    'ngay_bat_dau': today,
                    'trang_thai': 'dang_chay',
                    'muc_tieu': f'Chăm sóc sinh nhật cho {customer.ten_khach_hang}.',
                    'khach_hang_ids': [(6, 0, [customer.id])],
                })
            else:
                campaign.write({
                    'ten_chien_dich': campaign_name,
                    'khach_hang_ids': [(4, customer.id)],
                })

    @api.model
    def _cron_add_birthdays_to_campaign(self):
        today = fields.Date.context_today(self)
        if not today:
            return
        birthday_customers = self.search([('ngay_sinh', '!=', False)])
        birthday_customers._add_birthday_campaign_if_today(today=today)