from odoo import models, fields, api, exceptions
import re
from dateutil.relativedelta import relativedelta


class Patient(models.Model):
    _name = "hms.patient"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Patient"
    _rec_name = "f_name"

    f_name = fields.Char(string="First Name", required=True)
    l_name = fields.Char(string="Last Name", required=True)
    email = fields.Char()
    _sql_constraints = [("Duplicated_Email", "UNIQUE(email)", "Email Already Exists")]
    birth_date = fields.Date()
    age = fields.Integer(compute="compute_age")
    history = fields.Html(tracking=1)
    cr_ratio = fields.Float()
    blood_type = fields.Selection(
        [('a+', 'A+'),
         ('a-', 'A-'),
         ('b+', 'B+'),
         ('b-', 'B-'),
         ('ab+', 'AB+'),
         ('ab-', 'AB-'),
         ('O+', 'O+'),
         ('O-', 'O-')]
    )
    pcr = fields.Boolean()
    image = fields.Binary()
    address = fields.Text()
    department_id = fields.Many2one("hms.department")
    department_capacity = fields.Integer(related="department_id.capacity")
    doctors_ids = fields.Many2many("hms.doctor")
    log_history_ids = fields.One2many("patient.log.history", "patient_id")
    add_history_wizard_ids = fields.One2many("wizard.add_history", "patient_id")
    state = fields.Selection([
        ('undetermined', "Undetermined"),
        ('good', "Good"),
        ('fair', "Fair"),
        ('serious', "Serious")
    ], default='undetermined', tracking=1)

    @api.constrains("email")
    def check_email(self):
        for rec in self:
            if rec.email:
                valid_email = re.match(r"^[A-z0-9]+@[A-z0-9]+\.(com|net|org|info|gov)$", rec.email)
                if not valid_email:
                    return exceptions.ValidationError("Invalid email address")

    @api.depends("birth_date")
    def compute_age(self):
        for rec in self:
            if rec.birth_date:
                rec.age = relativedelta(fields.Date.today(), rec.birth_date).years
            else:
                rec.age = False

    def undetermined(self):
        self.state = 'undetermined'
        self.env['patient.log.history'].create(
            {
                'patient_id': self._uid,
                'current_date': fields.Datetime.now(),
                'description': f'state changed to {self.state}',
            }
        )

    def good(self):
        self.state = 'good'
        self.env['patient.log.history'].create(
            {
                'patient_id': self._uid,
                'current_date': fields.Datetime.now(),
                'description': f'state changed to {self.state}',
            }
        )

    def fair(self):
        self.state = 'fair'
        self.env['patient.log.history'].create(
            {
                'patient_id': self._uid,
                'current_date': fields.Datetime.now(),
                'description': f'state changed to {self.state}',
            }
        )

    def serious(self):
        self.state = 'serious'
        self.env['patient.log.history'].create(
            {
                'patient_id': self._uid,
                'current_date': fields.Datetime.now(),
                'description': f'state changed to {self.state}',
            }
        )

    @api.onchange('age')
    def _onchange_age(self):
        if self.age > 30:
            self.pcr = True
            return {
                'warning': {
                    'message': 'PCR has been changed.'
                }
            }

    def action_add_history(self):
        action = self.env['ir.actions.actions']._for_xml_id('hms.history_wizard_action')
        action['context'] = {
            'default_patient_id': self.id,
            'default_current_date': fields.Datetime.now(),
        }
        return action


class PatientLogHistory(models.Model):
    _name = "patient.log.history"

    patient_id = fields.Many2one("hms.patient")
    current_date = fields.Datetime()
    description = fields.Text()
