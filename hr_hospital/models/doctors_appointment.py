import logging

from odoo import models, fields

_logger = logging.getLogger(__name__)


class DoctorsAppointment(models.Model):
    _name = 'hr.hosp.doctors_appointment'
    _description = 'Doctors appointment'
    _order = "reception_datetime desc"

    reception_datetime = fields.Datetime(
        string='Дата і час прийому',
        required=True,
    )

    name = fields.Many2one(
        string='Пацієнт',
        comodel_name='hr.hosp.patient',
        required=True,
    )

    doctor_id = fields.Many2one(
        string='Лікар',
        comodel_name='hr.hosp.doctor',
        required=True,
    )

    doctor_specialization_ids = fields.Many2many(
        related='doctor_id.specialization_ids',
        readonly=True,
    )

    active = fields.Boolean(
        default=True,
    )
