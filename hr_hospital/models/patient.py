import logging

from odoo import models, fields, api

_logger = logging.getLogger(__name__)


class Patient(models.Model):
    _name = 'hr.hosp.patient'
    _description = 'Patient'
    _inherit = 'hr.hosp.personal_data.mixin'

    birthday = fields.Date(
        string='Дата народження',
        help='Введіть дату народження',
        required=True,
    )

    age = fields.Integer(
        string='Вік',
        help='Кількість повних років',
        compute='_compute_age',
        compute_sudo=True,
    )

    passport = fields.Char(
        string='Паспортні дані',
        help='Введіть паспортні дані',
        required=True,
    )

    contact_person_id = fields.Many2one(
        string='Контактна особа',
        help='Введіть дані контактної особи',
        comodel_name='hr.hosp.contact_person',
    )

    person_doctor_id = fields.Many2one(
        string='Сімейний лікар',
        help='Оберіть сімейного лікаря',
        comodel_name='hr.hosp.doctor',
        domain="[('is_person_doctor', '=', True)]",
        required=True,
    )

    person_doctor_history_ids = fields.One2many(
        comodel_name='hr.hosp.personal_doctor_history',
        inverse_name='name',
    )

    diagnosis_history_ids = fields.One2many(
        comodel_name='hr.hosp.diagnosis_history',
        inverse_name='patient_id',
    )

    active = fields.Boolean(
        default=True,
    )

    @api.depends("birthday")
    def _compute_age(self):
        for rec in self:
            rec.age = (fields.Date.today() - rec.birthday).days // 365 if rec.birthday else 0

    @api.model
    def create(self, vals):
        rec = super().create(vals)
        if 'person_doctor_id' in vals:
            values = {
                'name': rec.id,
                'doctor': self.env['hr.hosp.doctor'].browse(vals.get('person_doctor_id')).name,
                'appointment_date': fields.Date.today(),
            }
            self.env['hr.hosp.personal_doctor_history'].create(values)
        return rec

    def write(self, vals):
        if 'person_doctor_id' not in vals:
            return super().write(vals)
        for rec in self:
            if rec.person_doctor_id.id != vals.get('person_doctor_id'):
                values = {
                    'name': rec.id,
                    'doctor': self.env['hr.hosp.doctor'].browse(vals.get('person_doctor_id')).name,
                    'appointment_date': fields.Date.today(),
                }
                self.env['hr.hosp.personal_doctor_history'].create(values)
        return super().write(vals)

    def hr_hosp_change_personal_doctor_multi_wizard_act_window(self):
        action = self.env['ir.actions.act_window']._for_xml_id(
            'hr_hospital.hr_hosp_change_personal_doctor_multi_wizard_act_window')
        action['context'] = {'default_product_tmpl_ids': self.ids}
        return action
