{
    'name': 'Field Operation',
    'version': '18.0.1.0.0',
    'summary': 'Track field jobs, worker-entered times, dispatcher-measured quantities and flat-rate pay.',
    'description': """
Field Operation
===============
Office dispatchers create and assign field jobs to workers. Workers stamp
start/finish times and attach photos/notes from mobile. Dispatchers enter
the measured quantity (e.g. m² cut) which drives flat-rate pay.

Includes a bonus-rule placeholder for future production-based incentives
(Phase 2) and a 15-day payroll summary (Phase 2).
""",
    'category': 'Services',
    'author': 'Sebastian Perez',
    'license': 'LGPL-3',
    'depends': ['base', 'mail', 'hr', 'uom'],
    'data': [
        'security/field_operation_security.xml',
        'security/ir.model.access.csv',
        'data/field_operation_data.xml',
        'views/field_operation_views.xml',
    ],
    'installable': True,
    'application': True,
}
