{
    "name": "Hospital Management System",
    "author": "Kareem ",
    "description": """
             
    "summary": "This is the System for Management Hospital and assignment patients Information""",
    "data": [
        "reports/print_patient_template.xml",
        "reports/print_patient.xml",
        "security/ir.model.access.csv",
        "security/security_view.xml",
        "views/base_menus.xml",
        "views/patient_view.xml",
        "views/department_view.xml",
        "views/doctor_view.xml",
        # "views/customer_inherit_view.xml",
        'wizard/add_history_wizard.xml',

    ],
    'depends': ['base', 'web', 'mail'],
}
