from odoo import _, api, fields, models
from odoo.exceptions import UserError


class FieldOperation(models.Model):
    _name = 'field.operation'
    _description = 'Field Operation'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date_planned desc, id desc'

    name = fields.Char(
        string='Reference',
        required=True,
        copy=False,
        readonly=True,
        default=lambda self: _('New'),
        tracking=True,
    )
    partner_id = fields.Many2one('res.partner', string='Customer', required=True, tracking=True)
    site_address = fields.Char(tracking=True)
    operation_type_id = fields.Many2one(
        'field.operation.type',
        string='Operation Type',
        required=True,
        tracking=True,
    )
    worker_id = fields.Many2one(
        'hr.employee',
        string='Worker',
        required=True,
        tracking=True,
    )
    dispatcher_id = fields.Many2one(
        'res.users',
        string='Dispatcher',
        default=lambda self: self.env.user,
        tracking=True,
    )
    date_planned = fields.Date(
        default=fields.Date.context_today,
        required=True,
        tracking=True,
    )
    state = fields.Selection(
        [
            ('draft', 'Draft'),
            ('assigned', 'Assigned'),
            ('in_progress', 'In Progress'),
            ('done', 'Done'),
            ('closed', 'Closed'),
        ],
        default='draft',
        required=True,
        tracking=True,
    )
    start_datetime = fields.Datetime(tracking=True)
    end_datetime = fields.Datetime(tracking=True)
    quantity = fields.Float(
        tracking=True,
        help="Measured by the dispatcher. Drives pay calculation.",
    )
    uom_id = fields.Many2one(related='operation_type_id.uom_id', readonly=True)
    flat_rate = fields.Monetary(related='operation_type_id.flat_rate', readonly=True)
    currency_id = fields.Many2one(related='operation_type_id.currency_id', readonly=True)
    flat_pay = fields.Monetary(compute='_compute_pay', store=True)
    bonus_amount = fields.Monetary(compute='_compute_pay', store=True)
    total_pay = fields.Monetary(compute='_compute_pay', store=True)
    note = fields.Text()

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('name') or vals['name'] == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('field.operation') or _('New')
        return super().create(vals_list)

    @api.depends('quantity', 'flat_rate')
    def _compute_pay(self):
        for record in self:
            record.flat_pay = record.quantity * record.flat_rate
            # Bonus evaluator lands in Phase 2 — keep zero for now.
            record.bonus_amount = 0.0
            record.total_pay = record.flat_pay + record.bonus_amount

    def action_assign(self):
        self.write({'state': 'assigned'})

    def action_start(self):
        for record in self:
            record.write({
                'state': 'in_progress',
                'start_datetime': record.start_datetime or fields.Datetime.now(),
            })

    def action_finish(self):
        for record in self:
            record.write({
                'state': 'done',
                'end_datetime': record.end_datetime or fields.Datetime.now(),
            })

    def action_close(self):
        for record in self:
            if not record.quantity:
                raise UserError(_("Enter the measured quantity before closing %s.") % record.name)
        self.write({'state': 'closed'})

    def action_reset_to_draft(self):
        self.write({'state': 'draft'})
