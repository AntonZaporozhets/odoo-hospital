import logging

from odoo import models, fields

_logger = logging.getLogger(__name__)


class ContactPerson(models.Model):
    _name = 'hr.hosp.contact_person'
    _description = 'Contact person'
    _inherit = 'hr.hosp.personal_data.mixin'

    active = fields.Boolean(
        default=True,
    )
