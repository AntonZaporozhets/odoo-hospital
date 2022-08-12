import logging

from odoo import models, fields

_logger = logging.getLogger(__name__)


class MedTest(models.Model):
    _name = 'hr.hosp.medtest'
    _description = 'Medical test'
    _order = "issue_date desc"

    issue_date = fields.Date(
        string='Дата направлення',
        readonly=True,
    )

    name = fields.Char(
        string='Пацієнт',
        readonly=True,
    )

    doctor = fields.Char(
        string='Лікар',
        readonly=True,
    )

    medtest = fields.Char(
        string='Обстеження',
        readonly=True,
    )

    medtest_date = fields.Date(
        string='Дата обстеження',
        help='Введіть дату обстеження',
    )

    conclusion = fields.Text(
        string='Заключення',
        help='Опишіть результати дослідження',
    )

    material = fields.Binary(
        string='Матеріали',
        help='Завантажте додаткові матеріали',
    )

    active = fields.Boolean(
        default=True,
    )
