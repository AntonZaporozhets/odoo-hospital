import logging

from odoo import models, fields, api

_logger = logging.getLogger(__name__)


class Doctor(models.Model):
    _name = 'hr.hosp.doctor'
    _description = 'Doctor'
    _inherit = 'hr.hosp.personal_data.mixin'

    specialization_ids = fields.Many2many(
        string='Спеціалізація',
        help='Оберіть спеціалізацію',
        comodel_name='hr.hosp.doctor_specialization',
        required=True,
    )

    is_intern = fields.Boolean(
        string='Інтерн',
        help='Чи є інтерном?',
        default=False,
    )

    is_mentor = fields.Boolean(
        string='Ментор',
        help='Чи є ментором?',
        default=False,
    )

    is_person_doctor = fields.Boolean(
        string='Спеціалізація персонального лікаря',
        help='Чи має спеціалізацію персонального лікаря?',
        compute='_compute_is_person_doctor',
        default=False,
        store=True,
    )

    mentor_id = fields.Many2one(
        string='Лікар-ментор',
        help='Оберіть ментора',
        comodel_name='hr.hosp.doctor',
        domain="[('is_intern', '=', False)]",
    )

    mentor_name = fields.Char(
        related='mentor_id.name',
    )

    mentor_phone = fields.Char(
        string='Телефон',
        related='mentor_id.phone',
    )

    mentor_email = fields.Char(
        string='Електронна пошта',
        related='mentor_id.email',
    )

    mentor_photo = fields.Image(
        max_width=128,
        max_height=128,
        related='mentor_id.photo',
    )

    mentor_sex = fields.Selection(
        string='Стать',
        related='mentor_id.sex',
    )

    mentor_specialization_ids = fields.Many2many(
        string='Спеціалізація',
        related='mentor_id.specialization_ids',
    )

    mentor_ids = fields.One2many(
        comodel_name='hr.hosp.doctor',
        inverse_name='mentor_id',
    )

    active = fields.Boolean(
        default=True,
    )

    @api.depends("specialization_ids")
    def _compute_is_person_doctor(self):
        if not self.specialization_ids:
            self.is_person_doctor = False
        temp = False
        for rec in self.specialization_ids:
            temp = True if ('сімейний лікар' == rec.name) or (temp) else False
        self.is_person_doctor = temp

    @api.onchange('is_intern')
    def _onchange_is_intern(self):
        if not self.is_intern:
            self.mentor_id = False

    @api.onchange('mentor_id')
    def _onchange_mentor_id(self):
        if self.mentor_id.id == self._origin.id:
            self.mentor_id = False

    @api.model
    def create(self, vals):
        rec = super().create(vals)
        if 'mentor_id' in vals:
            self.browse(vals.get('mentor_id')).write({'is_mentor': True})
        return rec

    def write(self, vals):
        temp = self.mentor_id.id
        if 'is_intern' in vals and not vals.get('is_intern') or vals.get('mentor_id') == self.id:
            vals['mentor_id'] = False
        rec = super().write(vals)
        if 'mentor_id' in vals:
            if temp > 0:
                if temp in self.search([]).mapped('mentor_id.id'):
                    self.browse(temp).write({'is_mentor': True})
                else:
                    self.browse(temp).write({'is_mentor': False})
            if self.mentor_id.id > 0:
                self.browse(self.mentor_id.id).write({'is_mentor': True})
        return rec
