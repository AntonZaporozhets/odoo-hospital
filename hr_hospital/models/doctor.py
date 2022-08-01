import logging

from odoo import models, fields

_logger = logging.getLogger(__name__)


class Doctor(models.Model):
    _name = 'hr.hosp.doctor'
    _description = 'Doctor'

    name = fields.Char(
        string='Лікар',
        help='Введіть ПІБ повністю',
        required=True,
    )

    specialization = fields.Selection(
        string='Спеціалізація',
        help='Оберіть спеціалізацію',
        selection=[('therapist', 'терапевт'),
                   ('surgeon', 'хірург'),
                   ('gastroenterologist', 'гастроентеролог'),
                   ('ophthalmologist', 'офтальмолог'),
                   ('endocrinologist', 'ендокринолог')],
    )

    experience = fields.Integer(
        string='Стаж роботи',
        help='Введіть стаж роботи',
    )

    active = fields.Boolean(
        default=True,
    )
