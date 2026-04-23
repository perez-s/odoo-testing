from odoo import fields, models


class FieldOperationType(models.Model):
    _name = 'field.operation.type'
    _description = 'Field Operation Type'
    _order = 'sequence, name'

    name = fields.Char(required=True, translate=True)
    sequence = fields.Integer(default=10)
    active = fields.Boolean(default=True)
    uom_id = fields.Many2one(
        'uom.uom',
        string='Unit of Measure',
        required=True,
    )
    currency_id = fields.Many2one(
        'res.currency',
        default=lambda self: self.env.company.currency_id,
        required=True,
    )
    flat_rate = fields.Monetary(
        required=True,
        help="Pay per unit of measure (e.g. per m²).",
    )
    bonus_rule_ids = fields.One2many(
        'field.operation.bonus.rule',
        'operation_type_id',
        string='Bonus Rules',
    )
    note = fields.Text()
