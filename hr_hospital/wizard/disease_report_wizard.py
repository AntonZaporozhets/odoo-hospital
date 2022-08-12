import logging

from odoo import models, fields

_logger = logging.getLogger(__name__)


class DiseaseReportWizard(models.TransientModel):
    _name = 'hr.hosp.disease_report_wizard'
    _description = 'Disease report wizard'

    date = fields.Date(
        string='Дата',
        help='Оберіть дату',
    )

    def action_print_disease_report(self):
        records = self.env['hr.hosp.diagnosis_history'].search([]).filtered(lambda r: r.confirmation_date is not False and (r.confirmation_date >= fields.Date.start_of(self.date,'month') and r.confirmation_date <= fields.Date.end_of(self.date,'month')))
        list_report = []
        for rec in records.mapped('disease'):
            filtered = records.filtered(lambda r: r.disease.id == rec.id)
            list_report.append(
                {
                    'disease': rec.complete_name,
                    'diagnosis': [*set([elem.diagnosis for elem in filtered])],
                    'count': len(filtered),
                }
            )
        return self.env.ref('hr_hospital.action_report_disease').report_action(self, data={'diseases': list_report})
