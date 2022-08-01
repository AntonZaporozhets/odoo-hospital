import logging

from odoo import models, fields

_logger = logging.getLogger(__name__)


class Patient(models.Model):
    _name = 'hr.hosp.patient'
    _description = 'Patient'

    name = fields.Char(
        string='Пацієнт',
        help='Введіть ПІБ повністю',
        invisible=False,
        readonly=False,
        required=True,
        index=False,
        default=None,
        store=True,
        trim=True,
    )
    # властивості по замовчуваанню один раз виписав, щоб запам'ятати

    sex = fields.Selection(
        string='Стать',
        help='Оберіть стать',
        selection=[('male', 'чол.'), ('female', 'жін.')]
    )

    birthday = fields.Date(
        string='Дата народження',
        help='Введіть дату народження',
    )

    insurance = fields.Boolean(
        string='Страхування',
        default=False,
    )

    active = fields.Boolean(
        default=True,
    )
