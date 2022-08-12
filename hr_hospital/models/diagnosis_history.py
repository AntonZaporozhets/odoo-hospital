import logging

from odoo import models, fields

_logger = logging.getLogger(__name__)


class DiagnosisHistory(models.Model):
    _name = 'hr.hosp.diagnosis_history'
    _description = 'Diagnosis history'
    _order = 'name desc'

    name = fields.Char()

    patient = fields.Char(
        string='Пацієнт',
    )

    doctor = fields.Char(
        string='Сімейний лікар',
    )

    diagnosis = fields.Char(
        string='Діагноз',
    )

    disease = fields.Many2one(
        string='Хвороба',
        comodel_name='hr.hosp.diseases_handbook_category',
    )

    confirmation_date = fields.Date(
        string='Дата підтвердження',
    )

    withdrawal_date = fields.Date(
        string='Дата зняття',
    )

    active = fields.Boolean(
        default=True,
    )
