# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class PurchaseOrder(models.Model):
    _name = "purchase.order"
    _inherit = [
        "purchase.order",
    ]

    qty_to_receive = fields.Float(
        string="Qty To Receive",
        compute="_compute_receive",
        store=True,
    )
    qty_received = fields.Float(
        string="Qty Received",
        compute="_compute_receive",
        store=True,
    )
    percent_received = fields.Float(
        string="Percent Received",
        compute="_compute_receive",
        store=True,
    )

    @api.depends(
        "order_line",
        "order_line.qty_to_receive",
        "order_line.qty_received",
    )
    def _compute_receive(self):
        for record in self:
            qty_to_receive = qty_received = percent_received = 0.0
            for line in record.order_line:
                qty_to_receive += line.qty_to_receive
                qty_received += line.qty_received
            if qty_to_receive != 0.0:
                try:
                    percent_received = qty_received / qty_to_receive
                except ZeroDivisionError:
                    percent_received = 0.0
            record.qty_received = qty_received
            record.percent_received = percent_received
            record.qty_to_receive = qty_to_receive
