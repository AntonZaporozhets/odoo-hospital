import logging

from odoo import models, fields

_logger = logging.getLogger(__name__)


class DoctorSpecialization(models.Model):
    _name = 'hr.hosp.doctor_specialization'
    _description = 'Doctor specialization'
    _order = "name"

    name = fields.Char(
        string='Спеціалізація',
        help='Введіть назви спеціалізацій',
        required=True,
    )

    active = fields.Boolean(
        default=True,
    )
