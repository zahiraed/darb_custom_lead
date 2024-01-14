from odoo import models, fields


class ResPartnerInherit(models.Model):
    _inherit = 'res.partner'

    # add field lead ids that contain only current leads of each customer
    lead_ids = fields.One2many('crm.lead', 'partner_id', string="Current leads",
                               domain=[('type', '=', 'lead')], readonly=True)
