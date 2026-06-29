# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)


class CongViec(models.Model):
    _name = 'cong_viec'
    _description = 'Quản lý công việc và tương tác khách hàng'
    _rec_name = 'tieu_de'
    _order = 'ngay_bat_dau desc'

    ma_cong_viec = fields.Char("Mã công việc", readonly=True, copy=False)
    tieu_de = fields.Char("Tiêu đề", required=True)
    
    loai_cong_viec = fields.Selection([
        ('goi_dien', 'Gọi điện'),
        ('gui_bao_gia', 'Gửi báo giá'),
        ('lich_hen', 'Lịch hẹn'),
        ('gap_mat', 'Gặp mặt'),
        ('email', 'Email'),
        ('khac', 'Khác')
    ], string="Loại công việc", required=True, default='goi_dien')
    
    khach_hang_id = fields.Many2one('khach_hang', string="Khách hàng", required=True)
    du_an_id = fields.Many2one('du_an', string="Dự án")
    
    ngay_bat_dau = fields.Datetime("Ngày bắt đầu", default=fields.Datetime.now)
    ngay_hoan_thanh = fields.Datetime("Ngày hoàn thành")
    thoi_luong = fields.Float("Thời lượng (giờ)")
    
    trang_thai = fields.Selection([
        ('moi', 'Mới'),
        ('dang_thuc_hien', 'Đang thực hiện'),
        ('hoan_thanh', 'Hoàn thành'),
        ('huy', 'Hủy')
    ], string="Trạng thái", default='moi', required=True)
    
    muc_do_uu_tien = fields.Selection([
        ('thap', 'Thấp'),
        ('trung_binh', 'Trung bình'),
        ('cao', 'Cao'),
        ('khan_cap', 'Khẩn cấp')
    ], string="Mức độ ưu tiên", default='trung_binh')
    
    phong_ban_phu_trach_id = fields.Many2one('phong_ban', string="Phòng ban phụ trách", required=True)
    nguoi_thuc_hien_id = fields.Many2one('nhan_vien', string="Nhân viên được gán", readonly=True)
    
    mo_ta = fields.Text("Mô tả")
    ket_qua = fields.Text("Kết quả")
    
    gia_tri_bao_gia = fields.Float("Giá trị báo giá")
    trang_thai_bao_gia = fields.Selection([
        ('chua_gui', 'Chưa gửi'),
        ('da_gui', 'Đã gửi'),
        ('dong_y', 'Đồng ý'),
        ('tu_choi', 'Từ chối')
    ], string="Trạng thái báo giá")
    
    ghi_chu = fields.Text("Ghi chú")
    
    google_calendar_event_id = fields.Char("Google Calendar Event ID", readonly=True, copy=False)
    sync_to_google_calendar = fields.Boolean("Đồng bộ với Google Calendar", default=True)
    last_sync_date = fields.Datetime("Lần đồng bộ cuối", readonly=True)
    
    @api.onchange('phong_ban_phu_trach_id')
    def _onchange_phong_ban_phu_trach(self):
        if self.phong_ban_phu_trach_id:
            employee = self._find_free_employee(self.phong_ban_phu_trach_id)
            if employee:
                self.nguoi_thuc_hien_id = employee
    
    @api.model
    def create(self, vals):
        loai_map = {
            'goi_dien': 'GD',
            'gui_bao_gia': 'BG',
            'lich_hen': 'LH',
            'gap_mat': 'GM',
            'email': 'EM',
            'khac': 'KH'
        }
        
        loai = vals.get('loai_cong_viec', 'khac')
        ma_loai = loai_map.get(loai, 'CV')
        
        counter = 1
        ma_cong_viec = f"{ma_loai}{counter:04d}"
        while self.search([('ma_cong_viec', '=', ma_cong_viec)], limit=1):
            counter += 1
            ma_cong_viec = f"{ma_loai}{counter:04d}"
        
        vals['ma_cong_viec'] = ma_cong_viec

        dept_id = vals.get('phong_ban_phu_trach_id')
        if dept_id and not vals.get('nguoi_thuc_hien_id'):
            employee = self._find_free_employee(self.env['phong_ban'].browse(dept_id))
            if employee:
                vals['nguoi_thuc_hien_id'] = employee.id
        
        record = super(CongViec, self).create(vals)
        
        if record.sync_to_google_calendar and record.ngay_bat_dau:
            record._sync_google_calendar_event()
        
        return record

    def write(self, vals):
        if 'phong_ban_phu_trach_id' in vals and not vals.get('nguoi_thuc_hien_id'):
            dept_id = vals.get('phong_ban_phu_trach_id') or self.phong_ban_phu_trach_id.id
            if dept_id:
                employee = self._find_free_employee(self.env['phong_ban'].browse(dept_id))
                if employee:
                    vals['nguoi_thuc_hien_id'] = employee.id
        
        result = super().write(vals)
        
        # Tự động cập nhật trạng thái khách hàng khi công việc hoàn thành
        if vals.get('trang_thai') == 'hoan_thanh':
            for rec in self:
                if rec.khach_hang_id:
                    kh = rec.khach_hang_id
                    if rec.loai_cong_viec == 'lich_hen':
                        kh.write({'trang_thai': 'dang_dam_phan'})
                    elif rec.loai_cong_viec == 'gui_bao_gia':
                        if rec.trang_thai_bao_gia == 'dong_y':
                            kh.write({'trang_thai': 'thanh_cong'})
                        else:
                            kh.write({'trang_thai': 'dang_dam_phan'})
                    elif rec.loai_cong_viec in ['goi_dien', 'email', 'gap_mat']:
                        if kh.trang_thai == 'tiem_nang':
                            kh.write({'trang_thai': 'da_lien_he'})

        # Đồng bộ Google Calendar
        sync_fields = ['ngay_bat_dau', 'ngay_hoan_thanh', 'tieu_de', 'mo_ta', 'trang_thai']
        if any(field in vals for field in sync_fields):
            for record in self:
                if record.sync_to_google_calendar and record.ngay_bat_dau:
                    record._sync_google_calendar_event()
        
        return result

    def _find_free_employee(self, department):
        if not department:
            return False
        employees = self.env['nhan_vien'].search([('phong_ban_id', '=', department.id)])
        for emp in employees:
            active_tasks = self.env['cong_viec'].search_count([
                ('nguoi_thuc_hien_id', '=', emp.id),
                ('trang_thai', 'in', ['moi', 'dang_thuc_hien'])
            ])
            active_projects = self.env['du_an'].search_count([
                ('nguoi_phu_trach_id', '=', emp.id),
                ('trang_thai', 'in', ['ke_hoach', 'dang_tien_hanh', 'tam_dung'])
            ])
            if active_tasks == 0 and active_projects == 0:
                return emp
        return employees[:1] if employees else False
    
    def action_bat_dau(self):
        self.write({'trang_thai': 'dang_thuc_hien'})
    
    def action_hoan_thanh(self):
        for rec in self:
            rec.write({
                'trang_thai': 'hoan_thanh',
                'ngay_hoan_thanh': fields.Datetime.now()
            })
    
    def action_huy(self):
        self.write({'trang_thai': 'huy'})
    
    def _sync_google_calendar_event(self):
        self.ensure_one()
        if not self.sync_to_google_calendar:
            return
        try:
            if self.google_calendar_event_id:
                self._update_google_event()
            else:
                self._create_google_event()
            self.sudo().write({'last_sync_date': fields.Datetime.now()})
        except Exception as e:
            _logger.error(f"Lỗi khi đồng bộ với Google Calendar: {str(e)}")
    
    def _prepare_google_event_data(self):
        self.ensure_one()
        start_time = self.ngay_bat_dau
        end_time = self.ngay_hoan_thanh or start_time
        description_parts = []
        if self.ma_cong_viec:
            description_parts.append(f"Ma: {self.ma_cong_viec}")
        if self.loai_cong_viec:
            loai_dict = dict(self._fields['loai_cong_viec'].selection)
            description_parts.append(f"Loai: {loai_dict.get(self.loai_cong_viec)}")
        if self.khach_hang_id:
            description_parts.append(f"Khach hang: {self.khach_hang_id.ten_khach_hang}")
        if self.nguoi_thuc_hien_id:
            description_parts.append(f"Nguoi thuc hien: {self.nguoi_thuc_hien_id.ho_ten_day_du}")
        if self.mo_ta:
            description_parts.append(f"Mo ta: {self.mo_ta}")
        event_data = {
            'summary': f"[{self.ma_cong_viec}] {self.tieu_de}",
            'description': '\n'.join(description_parts),
            'start': {
                'dateTime': start_time.strftime('%Y-%m-%dT%H:%M:%S'),
                'timeZone': 'Asia/Ho_Chi_Minh',
            },
            'end': {
                'dateTime': end_time.strftime('%Y-%m-%dT%H:%M:%S'),
                'timeZone': 'Asia/Ho_Chi_Minh',
            },
        }
        color_map = {
            'khan_cap': '11',
            'cao': '9',
            'trung_binh': '5',
            'thap': '2',
        }
        if self.muc_do_uu_tien:
            event_data['colorId'] = color_map.get(self.muc_do_uu_tien, '5')
        return event_data
    
    def _create_google_event(self):
        self.ensure_one()
        try:
            event_data = self._prepare_google_event_data()
            calendar_event = self.env['calendar.event'].sudo().create({
                'name': event_data['summary'],
                'description': event_data.get('description', ''),
                'start': self.ngay_bat_dau,
                'stop': self.ngay_hoan_thanh or self.ngay_bat_dau,
                'user_id': self.env.user.id,
                'privacy': 'public',
            })
            if calendar_event:
                calendar_event.write({'need_sync': True})
                if hasattr(calendar_event, 'google_id') and calendar_event.google_id:
                    self.sudo().write({'google_calendar_event_id': calendar_event.google_id})
                else:
                    self.sudo().write({'google_calendar_event_id': f'odoo_{calendar_event.id}'})
            _logger.info(f"Da tao Google Calendar event cho cong viec {self.ma_cong_viec}")
        except Exception as e:
            _logger.error(f"Loi khi tao Google Calendar event: {str(e)}")
            raise
    
    def _update_google_event(self):
        self.ensure_one()
        try:
            event_data = self._prepare_google_event_data()
            calendar_event = None
            if self.google_calendar_event_id and not self.google_calendar_event_id.startswith('odoo_'):
                calendar_event = self.env['calendar.event'].sudo().search([
                    ('google_id', '=', self.google_calendar_event_id)
                ], limit=1)
            if not calendar_event and self.google_calendar_event_id and self.google_calendar_event_id.startswith('odoo_'):
                event_id = int(self.google_calendar_event_id.replace('odoo_', ''))
                calendar_event = self.env['calendar.event'].sudo().browse(event_id)
                if not calendar_event.exists():
                    calendar_event = None
            if calendar_event:
                calendar_event.sudo().write({
                    'name': event_data['summary'],
                    'description': event_data.get('description', ''),
                    'start': self.ngay_bat_dau,
                    'stop': self.ngay_hoan_thanh or self.ngay_bat_dau,
                    'need_sync': True,
                })
            else:
                self.sudo().write({'google_calendar_event_id': False})
                self._create_google_event()
        except Exception as e:
            _logger.error(f"Loi khi cap nhat Google Calendar event: {str(e)}")
            raise
    
    def action_sync_google_calendar(self):
        for record in self:
            if not record.ngay_bat_dau:
                raise UserError(_("Vui long nhap ngay bat dau truoc khi dong bo voi Google Calendar."))
            record._sync_google_calendar_event()
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Thanh cong'),
                'message': _('Da dong bo voi Google Calendar'),
                'type': 'success',
                'sticky': False,
            }
        }
    
    def unlink(self):
        for record in self:
            if record.google_calendar_event_id:
                try:
                    calendar_event = self.env['calendar.event'].sudo().search([
                        ('google_id', '=', record.google_calendar_event_id)
                    ], limit=1)
                    if calendar_event:
                        calendar_event.sudo().unlink()
                except Exception as e:
                    _logger.error(f"Loi khi xoa Google Calendar event: {str(e)}")
        return super().unlink()