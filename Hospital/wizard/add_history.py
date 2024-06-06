from odoo import models, fields


class AddHistory(models.Model):
    _name = "wizard.add_history"

    patient_id = fields.Many2one('hms.patient')
    # created_by = fields.Many2one('res.users')
    current_date = fields.Datetime()
    description = fields.Text()

    def action_add_history(self):
        if self.description:
            self.patient_id.history = self.description


