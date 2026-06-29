# -*- coding: utf-8 -*-
import json
import requests
import re
import os

from odoo import fields, models, _
from odoo.exceptions import UserError
from odoo.modules.module import get_module_resource


class ChatbotNoiQuyMessage(models.Model):
    _name = "chatbot.noiquy.message"
    _description = "Chatbot Nội Quy Message"
    _order = "id desc"

    message = fields.Text(string="Tin nhắn")
    timestamp = fields.Datetime(string="Thời gian")


class ChatbotNoiQuyChat(models.Model):
    _name = "chatbot.noiquy.chat"
    _description = "Chatbot Nội Quy (Groq)"
    _order = "id desc"

    question = fields.Text(string="Câu hỏi", required=True)
    answer = fields.Text(string="Trả lời", readonly=True)
    last_error = fields.Text(string="Lỗi (nếu có)", readonly=True)

    GROQ_MODEL = "llama-3.1-8b-instant"

    def _get_api_key(self):
        # Đọc từ file .env
        env_file = os.path.join(os.path.dirname(__file__), '../../../../.env')
        if os.path.exists(env_file):
            with open(env_file) as f:
                for line in f:
                    if line.startswith('GROQ_API_KEY='):
                        return line.strip().split('=', 1)[1]
        # Fallback: đọc từ biến môi trường hệ thống
        return os.environ.get('GROQ_API_KEY', '')

    def _load_policy_text(self):
        path = get_module_resource("chatbot_noiquy", "data", "noi_quy.md")
        try:
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception:
            return ""

    def _call_groq(self, question, system_text=None, timeout=30):
        url = "https://api.groq.com/openai/v1/chat/completions"
        api_key = self._get_api_key()
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        }
        messages = []
        if system_text:
            messages.append({"role": "system", "content": system_text})
        messages.append({"role": "user", "content": question})
        payload = {
            "model": self.GROQ_MODEL,
            "messages": messages,
            "temperature": 0.2,
        }
        try:
            resp = requests.post(url, headers=headers, data=json.dumps(payload), timeout=timeout)
        except requests.RequestException as e:
            raise UserError(_("Không gọi được Groq API: %s") % str(e))
        if resp.status_code != 200:
            raise UserError(_("Groq API lỗi (%s): %s") % (resp.status_code, resp.text))
        data = resp.json()
        try:
            return data["choices"][0]["message"]["content"]
        except Exception:
            return json.dumps(data, ensure_ascii=False, indent=2)

    def action_ask(self):
        for rec in self:
            rec.answer = False
            rec.last_error = False
            prompt = (rec.question or "").strip()
            if not prompt:
                rec.last_error = "Vui lòng nhập câu hỏi."
                continue
            policy = rec._load_policy_text()
            system_text = (
                "Bạn là một trợ lý thông minh hỗ trợ nhân viên. "
                "Nếu có nội quy công ty được cung cấp, hãy ưu tiên trả lời dựa trên nội quy. "
                "Nếu câu hỏi không liên quan đến nội quy, bạn vẫn có thể trả lời hữu ích. "
                "Trả lời ngắn gọn, rõ ràng, bằng tiếng Việt."
            )
            if policy:
                prompt = (
                    f"CÂU HỎI: {prompt}\n\n"
                    f"NỘI QUY CÔNG TY:\n{policy}\n\n"
                    "Hãy trả lời câu hỏi, ưu tiên dựa trên nội quy nếu liên quan."
                )
            try:
                rec.answer = rec._call_groq(question=prompt, system_text=system_text)
            except Exception as e:
                rec.answer = False
                rec.last_error = str(e)
        return True