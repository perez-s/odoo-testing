from odoo import fields, models


class FieldOperationBonusRule(models.Model):
    """Placeholder — bonus logic is not yet active.

    Rules stored here are ignored by the pay compute until Phase 2 wires
    up the evaluator. Keeping the model in place lets dispatchers capture
    the rules they'd like as soon as the business defines them.
    """
    _name = 'field.operation.bonus.rule'
    _description = 'Field Operation Bonus Rule'
    _order = 'operation_type_id, threshold_quantity'

    name = fields.Char(required=True)
    operation_type_id = fields.Many2one(
        'field.operation.type',
        required=True,
        ondelete='cascade',
    )
    threshold_quantity = fields.Float(
        required=True,
        help="Rule applies when the job's measured quantity meets or exceeds this threshold.",
    )
    bonus_type = fields.Selection(
        [
            ('fixed', 'Fixed Amount'),
            ('per_unit', 'Per Unit Over Threshold'),
            ('percentage', 'Percentage of Flat Pay'),
        ],
        default='fixed',
        required=True,
    )
    bonus_value = fields.Float(required=True)
    active = fields.Boolean(default=True)
    currency_id = fields.Many2one(
        related='operation_type_id.currency_id',
        readonly=True,
    )
