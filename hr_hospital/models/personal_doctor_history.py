import logging

from odoo import models, fields

_logger = logging.getLogger(__name__)


class PersonalDoctorHistory(models.Model):
    _name = 'hr.hosp.personal_doctor_history'
    _description = 'Personal doctor history'
    _order = "name"

    name = fields.Char(
        string='Пацієнт',
    )

    doctor = fields.Char(
        string='Сімейний лікар',
    )

    appointment_date = fields.Date(
        string='Дата призначення',
    )

    active = fields.Boolean(
        default=True,
    )
