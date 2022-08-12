import logging

from odoo import models, fields

_logger = logging.getLogger(__name__)


class ChangePersonalDoctorMultiWizard(models.TransientModel):
    _name = 'hr.hosp.change_personal_doctor_multi_wizard'
    _description = 'Change personal doctor multi wizard'

    patient_ids = fields.Many2many(
        string='Пацієнт',
        help='Оберіть пацієнта',
        comodel_name='hr.hosp.patient',
        required=True,
    )

    doctor_id = fields.Many2one(
        string='Лікар',
        help='Оберіть лікаря',
        comodel_name='hr.hosp.doctor',
        required=True,
    )

    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        res['patient_ids'] = [(6, 0, self._context.get("active_ids"))]
        return res

    def action_set(self):
        self.ensure_one()
        self.patient_ids.write({'person_doctor_id': self.doctor_id.id})
