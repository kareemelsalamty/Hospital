from odoo import models, fields, api, exceptions


class Customer(models.Model):
    _inherit = "res.partner"

    related_patient_id = fields.Many2one("hms.patient")
    vat = fields.Char(required=True)

    @api.constrains('email')
    def _check_duplicate_email(self):
        for partner in self:
            if partner.related_patient_id and partner.related_patient_id.email == partner.email:
                raise exceptions.ValidationError('Email already exists in the patient model.')

    def unlink(self):
        for rec in self:
            if rec.related_patient_id:
                raise exceptions.UserError("You cannot delete any customer linked to a patient")
        super().unlink()
