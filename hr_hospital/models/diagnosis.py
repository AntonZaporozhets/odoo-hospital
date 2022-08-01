import logging

from odoo import models, fields

_logger = logging.getLogger(__name__)


class Diagnosis(models.Model):
    _name = 'hr.hosp.diagnosis'
    _description = 'Diagnosis'
    _rec_name = 'diagnosis'

    diagnosis = fields.Char(
        string='Діагноз',
        help='Введіть діагноз',
    )

    conclusion = fields.Text(
        string='Медичний висновок',
        help='Введіть медичний висновок',
    )

    recommendations = fields.Text(
        string='Рекомендації',
        help='Введіть рекомендації',
    )

    active = fields.Boolean(
        default=True,
    )
