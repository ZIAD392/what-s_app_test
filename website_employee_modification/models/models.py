from odoo import models, fields, api


class IrHttp(models.AbstractModel):
    _inherit = 'ir.http'

    @classmethod
    def _get_translation_frontend_modules_name(cls):
        modules = super()._get_translation_frontend_modules_name()
        return modules + ['website_employee_modification']


class HrEmployeeBaseInherit(models.AbstractModel):
    _inherit = "hr.employee.base"
    work_phone = fields.Char('Personal mobile', compute="_compute_work_contact_details", store=True,
                             inverse='_inverse_work_contact_details')
    job_id = fields.Many2one('hr.job', 'Job Position',
                             domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]")
    # job_title = fields.Char("Job Title", compute="_compute_job_title", store=True, readonly=True)


class HrEmployeeHistory(models.Model):
    _inherit = "hr.contract.history"
    country_id = fields.Many2one(related="employee_id.country_id", readonly=True)


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    # contract_position = fields.Char("Job Title", compute="_compute_job_title", store=True, readonly=True, translate=True)

    # name = fields.Char(string="Employee Name", related='resource_id.name', store=True, readonly=False, tracking=True, translate=True)
    english_name = fields.Char('English Name', translate=True)
    id_issuance_date = fields.Date('ID Issuance Date')
    id_expiry_date = fields.Date('ID Expiry Date')
    profession = fields.Char(string='Profession', translate=True)
    sponsor = fields.Char(string='Sponsor', translate=True)
    passport_copy = fields.Binary('Passport Copy')
    identification_id = fields.Char(string='ID No', groups="hr.group_hr_user", tracking=True, translate=True)
    passport_issuance_date = fields.Date('Passport Issuance Date')
    passport_expiry_date = fields.Date('Passport Expiry Date')
    driving_license_category = fields.Selection([
        ('private', 'Private'),
        ('heavy', 'Heavy Duty'),
        ('temp', 'Temporary'),
        ('moto', 'Motorcycle')
    ], string='Category', default='private', )
    employment_types = fields.Selection([
        ('local', 'Local Recruitment'),
        ('international', 'International Recruitment'),
        ('sponsorship', 'Sponsorship Transferring'),
        ('saudi', 'Saudi v'),
        ('tamheer', 'Tamheer'),
        ('remotely', 'Remotely'),
        ('part', 'Part Time'),
        ('ajeer', 'Ajeer'),
        ('consultant', 'Consultant'),
        ('work', 'Work Visit'),
        ('other', 'Other'),
    ], 'Employment Type', )
    driving_license_expiry_date = fields.Datetime('Driving License Expiry Date')
    driving_license_issuance_date = fields.Date('Driving License Issuance Date')
    certificate = fields.Selection([
        ('primary', 'Primary'),
        ('secondary', 'Secondary'),
        ('intermediate', 'Intermediate'),
        ('upper', 'Upper intermediate'),
        ('graduate', 'Graduate'),
        ('bachelor', 'Bachelor'),
        ('master', 'Master'),
        ('doctor', 'Doctor'),
        ('other', 'Other'),
    ], 'Certificate Level', default='other', groups="hr.group_hr_user", tracking=True)

    latest_job_position = fields.Char(
        string="Job Position",
        related="contract_id.job_id.name",
    )


class HrContract(models.Model):
    _inherit = 'hr.contract'

    country_id = fields.Many2one(related="employee_id.country_id", readonly=True)
    probation_period_end_date = fields.Date('Probation Period End Date')
    ticket_allowance = fields.Monetary(string='Ticket Allowance')
    leave_salary = fields.Monetary(string='Leave Salary')


class Department(models.Model):
    _inherit = "hr.department"

    name = fields.Char('Department Name', required=True, translate=True)
