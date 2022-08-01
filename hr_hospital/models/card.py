import logging
from datetime import datetime

from odoo import models, fields

_logger = logging.getLogger(__name__)


class Card(models.Model):
    _name = 'hr.hosp.card'
    _description = 'Card'

    name = fields.Integer(
        string='Номер запису',
    )

    date = fields.Date(
        string='Дата відвідування',
        default=datetime.today()
    )

    active = fields.Boolean(
        default=True,
    )

    patient_ids = fields.Many2one(
        string='Пацієнт',
        comodel_name='hr.hosp.patient',
    )

    diagnosis_ids = fields.Many2many(
        string='Діагноз',
        comodel_name='hr.hosp.diagnosis',
    )

    doctor_ids = fields.Many2one(
        string='Лікар',
        comodel_name='hr.hosp.doctor',
    )
