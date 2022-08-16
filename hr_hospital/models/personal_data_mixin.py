import logging

from odoo import models, fields

_logger = logging.getLogger(__name__)


class AddressMixin(models.AbstractModel):
    _name = 'hr.hosp.personal_data.mixin'
    _description = 'Personal data mixin'
    _order = "name"

    name = fields.Char(
        string='ПІБ',
        help='Введіть ПІБ повністю',
        required=True,
    )

    phone = fields.Char(
        string='Телефон',
        help='Введіть контактний телефон',
        required=True,
    )

    email = fields.Char(
        string='Електронна пошта',
        help='Введіть електронна пошта',
    )

    photo = fields.Image(
        string='Фото',
        help='Оберіть фото',
        max_width=128,
        max_height=128,
        required=True,
    )

    sex = fields.Selection(
        string='Стать',
        help='Оберіть стать',
        selection=[('male', 'чол.'), ('female', 'жін.')],
        required=True,
    )
