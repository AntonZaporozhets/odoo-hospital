import logging

from odoo import models, fields, api

_logger = logging.getLogger(__name__)


class VisitDoctor(models.Model):
    _name = 'hr.hosp.visit_doctor'
    _description = 'Visit doctor'
    _rec_name = 'patient_id'
    _order = "reception_datetime desc"

    reception_datetime = fields.Datetime(
        string='Дата і час прийому',
        default=fields.Datetime.now(),
        readonly=True,
    )

    doctor_id = fields.Many2one(
        string='Лікар',
        comodel_name='hr.hosp.doctor',
        required=True,
    )

    patient_id = fields.Many2one(
        string='Пацієнт',
        comodel_name='hr.hosp.doctors_appointment',
        domain="[('doctor_id', '=', doctor_id)]",
        required=True,
    )

    initial_visit_id = fields.Many2one(
        string='Первинне звернення',
        help='Оберіть при повторному візиті пацієнта',
        comodel_name='hr.hosp.diagnosis_history',
    )

    complaint = fields.Text(
        string='Скарги',
        help='Введіть скарги',
        required=True,
    )

    anamnesis = fields.Text(
        string='Анамнез',
        help='Введіть анамнез',
    )

    external_inspection = fields.Text(
        string='Зовнішній огляд',
        help='Введіть результати зовнішнього огляду',
        required=True,
    )

    doctor_specialization_ids = fields.Many2many(
        related='doctor_id.specialization_ids',
    )

    diagnosis_id = fields.Many2one(
        string='Діагноз',
        help='Оберіть діагноз',
        comodel_name='hr.hosp.diseases_handbook',
        domain="[('specialization_ids', 'in', doctor_specialization_ids)]",
        required=True,
    )

    disease_id = fields.Many2one(
        string='Хвороба',
        related='diagnosis_id.disease_id',
    )

    clarification_diagnosis = fields.Text(
        string='Уточнення діагнозу',
        help='Введіть уточнення діагнозу',
    )

    medtest_ids = fields.Many2many(
        string='Обстеження',
        comodel_name='hr.hosp.medtest_handbook',
    )

    specialist_consultation_ids = fields.Many2many(
        string='Консультації вузьких спеціалістів',
        help='Оберіть спеціалістів',
        comodel_name='hr.hosp.doctor_specialization',
    )

    prescribed_treatment = fields.Text(
        string='Призначене лікування',
        help='Введіть призначене лікування',
    )

    diagnosis_status = fields.Selection(
        string='Стан діагнозу',
        help='Оберіть стан діагнозу',
        selection=[('preliminary', 'попередній'), ('confirmed', 'підтверджений'), ('canceled', 'знятий')],
        default='preliminary',
        required=True,
    )

    is_intern = fields.Boolean(
        related='doctor_id.is_intern',
    )

    mentor_comment = fields.Text(
        string='Коментар ментора',
        help='Введіть коментар ментора',
    )

    patient_card_id = fields.Many2one(
        related='patient_id.name',
    )

    active = fields.Boolean(
        default=True,
    )

    @api.onchange('diagnosis_id')
    def _onchange_diagnosis_id(self):
        self.medtest_ids = self.diagnosis_id.medtest_protocol_ids

    @api.onchange('initial_visit_id')
    def _onchange_initial_visit(self):
        if self.initial_visit_id.name:
            arr = self.initial_visit_id.name.split(' // ')
            self.doctor_id = self.env['hr.hosp.doctor'].search([('name', '=', arr[1])])
            self.patient_id = self.env['hr.hosp.doctors_appointment'].search([('name', '=', arr[2])])[0].id
            self.diagnosis_id = self.env['hr.hosp.diseases_handbook'].search([('name', '=', arr[3])])
            self.clarification_diagnosis = arr[4] if self.clarification_diagnosis else ""
            self.complaint = arr[5]
            self.anamnesis = arr[6]
            self.external_inspection = arr[7]

    @api.model
    @api.depends('reception_datetime', 'doctor_id', 'patient_id', 'diagnosis_id', 'disease_id', 'complaint', 'anamnesis', 'external_inspection', 'clarification_diagnosis')
    def create(self, vals):
        rec = super().create(vals)
        rec.patient_id.active = False
        if not vals.get('initial_visit_id'):
            values = {
                'name': '%s // %s // %s // %s // %s // %s // %s // %s' % (fields.Date.to_string(rec.reception_datetime),
                                                              rec.doctor_id.name,
                                                              rec.patient_id.name.name,
                                                              rec.diagnosis_id.name,
                                                              rec.clarification_diagnosis,
                                                              rec.complaint,
                                                              rec.anamnesis,
                                                              rec.external_inspection),
                'patient_id': rec.patient_id.name.id,
                'doctor': rec.doctor_id.name,
                'diagnosis': rec.diagnosis_id.name,
                'disease': rec.disease_id.id,
                'confirmation_date': rec.reception_datetime if rec.diagnosis_status == 'confirmed' else None,
            }
            self.env['hr.hosp.diagnosis_history'].create(values)
        elif (rec.diagnosis_status == 'confirmed') and (not self.env['hr.hosp.diagnosis_history'].browse(vals.get('initial_visit_id')).confirmation_date):
            values = {
                'confirmation_date': rec.reception_datetime,
            }
            self.env['hr.hosp.diagnosis_history'].browse(vals.get('initial_visit_id')).write(values)
        elif rec.diagnosis_status == 'canceled':
            values = {
                'withdrawal_date': rec.reception_datetime,
            }
            self.env['hr.hosp.diagnosis_history'].browse(vals.get('initial_visit_id')).write(values)
        for elem in rec.medtest_ids:
            values = {
                'issue_date': fields.Date.to_date(rec.reception_datetime),
                'name': self.env['hr.hosp.patient'].search([('name', '=', rec.patient_id.name.name)]).id,
                'doctor': rec.doctor_id.name,
                'medtest_id': elem.id,
            }
            self.env['hr.hosp.medtest'].create(values)
        return rec
