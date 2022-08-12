import logging

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class MedTestHandbookCategory(models.Model):
    _name = "hr.hosp.medtest_handbook_category"
    _description = "Medtest handbook category"
    _parent_name = "parent_id"
    _parent_store = True
    _rec_name = 'complete_name'
    _order = 'complete_name'

    name = fields.Char(
        string='Вид обстеження',
        help='Введіть вид обстеження',
        index=True,
        required=True,
    )

    complete_name = fields.Char(
        compute='_compute_complete_name',
        recursive=True,
        store=True,
    )

    parent_id = fields.Many2one(
        string='Група обстежень',
        comodel_name='hr.hosp.medtest_handbook_category',
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


class MedtestHandbook(models.Model):
    _name = "hr.hosp.medtest_handbook"
    _description = "Medtest handbook"
    _rec_name = "full_name"
    _order = "medtest_group_id, name"

    name = fields.Char(
        string='Назва обстеження',
        help='Введіть назву обстеження',
        required=True,
    )

    medtest_group_id = fields.Many2one(
        string='Група обстежень',
        comodel_name='hr.hosp.medtest_handbook_category',
        index=True,
        required=True,
    )

    full_name = fields.Char(
        compute='_compute_full_name',
        store=True,
    )

    price = fields.Float(
        string='Вартість',
        help='Введіть вартість',
    )

    active = fields.Boolean(
        default=True,
    )

    @api.depends('name', 'medtest_group_id')
    def _compute_full_name(self):
        self.full_name = '%s / %s' % (self.medtest_group_id.complete_name, self.name)
