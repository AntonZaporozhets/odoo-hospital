import logging

from odoo import models, fields, api

_logger = logging.getLogger(__name__)


class Doctor(models.Model):
    _name = 'hr.hosp.doctor'
    _description = 'Doctor'
    _inherit = 'hr.hosp.personal_data.mixin'

    specialization_ids = fields.Many2many(
        string='Спеціалізація',
        help='Оберіть спеціалізацію',
        comodel_name='hr.hosp.doctor_specialization',
        required=True,
    )

    is_intern = fields.Boolean(
        string='Інтерн',
        help='Чи є інтерном?',
        default=False,
    )

    mentor_id = fields.Many2one(
        string='Лікар-ментор',
        help='Оберіть ментора',
        comodel_name='hr.hosp.doctor',
        domain="[('is_intern', '=', False)]",
    )

    active = fields.Boolean(
        default=True,
    )

    @api.onchange('is_intern')
    def _onchange_is_intern(self):
        if not self.is_intern:
            self.mentor_id = False

    @api.onchange('mentor_id')
    def _onchange_mentor_id(self):
        if self.mentor_id.id == self._origin.id:
            self.mentor_id = False

    def write(self, vals):
        if 'is_intern' in vals and not vals.get('is_intern') or vals.get('mentor_id') == self.id:
            vals['mentor_id'] = False
        return super().write(vals)
