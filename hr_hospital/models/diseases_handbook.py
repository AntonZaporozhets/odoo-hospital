import logging

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class DiseasesHandbookCategory(models.Model):
    _name = "hr.hosp.diseases_handbook_category"
    _description = "Diseases handbook category"
    _parent_name = "parent_id"
    _parent_store = True
    _rec_name = 'complete_name'
    _order = 'complete_name'

    name = fields.Char(
        string='Хвороба',
        help='Введіть назву хвороби',
        index=True,
        required=True,
    )

    complete_name = fields.Char(
        compute='_compute_complete_name',
        recursive=True,
        store=True,
    )

    parent_id = fields.Many2one(
        string='Повна назва хвороби',
        comodel_name='hr.hosp.diseases_handbook_category',
        index=True,
        ondelete='cascade',
    )

    parent_path = fields.Char(
        index=True,
    )

    @api.depends('name', 'parent_id.complete_name')
    def _compute_complete_name(self):
        for category in self:
            if category.parent_id:
                category.complete_name = '%s / %s' % (category.parent_id.complete_name, category.name)
            else:
                category.complete_name = category.name

    @api.constrains('parent_id')
    def _check_category_recursion(self):
        if not self._check_recursion():
            raise ValidationError(_('You cannot create recursive categories.'))

    @api.model
    def name_create(self, name):
        return self.create({'name': name}).name_get()[0]

    def name_get(self):
        if not self.env.context.get('hierarchical_naming', True):
            return [(record.id, record.name) for record in self]
        return super().name_get()


class DiseasesHandbook(models.Model):
    _name = "hr.hosp.diseases_handbook"
    _description = "Diseases handbook"
    _order = "disease_id, name"

    name = fields.Char(
        string='Діагноз',
        help='Введіть назву діагнозу',
        required=True,
    )

    disease_id = fields.Many2one(
        string='Хвороба',
        comodel_name='hr.hosp.diseases_handbook_category',
        index=True,
        required=True,
    )

    medtest_protocol_ids = fields.Many2many(
        comodel_name='hr.hosp.medtest_handbook',
        string='Протокол обстежень',
        help='Оберіть перелік обстежень згідно з протоколом',
    )

    duration = fields.Integer(
        string='Тривалість перебігу хвороби',
        help='Введіть тривалість перебігу хвороби за протоколом',
        required=True,
    )

    specialization_ids = fields.Many2many(
        string='Спеціалізація лікаря',
        comodel_name='hr.hosp.doctor_specialization',
        index=True,
        required=True,
    )

    active = fields.Boolean(
        default=True,
    )
