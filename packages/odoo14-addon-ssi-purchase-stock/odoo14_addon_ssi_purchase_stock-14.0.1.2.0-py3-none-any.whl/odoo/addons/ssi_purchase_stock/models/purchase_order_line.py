# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class PurchaseOrderLine(models.Model):
    _name = "purchase.order.line"
    _inherit = [
        "purchase.order.line",
    ]

    percent_received = fields.Float(
        string="Percent Received",
        compute="_compute_receive",
        store=True,
        compute_sudo=True,
    )
    qty_to_receive = fields.Float(
        string="Qty To Receive",
        compute="_compute_receive",
        store=True,
        compute_sudo=True,
    )

    @api.depends(
        "qty_received",
        "product_uom_qty",
    )
    def _compute_receive(self):
        for record in self:
            percent_received = qty_to_receive = qty_recieved = 0.0
            if record.product_id.type != "service":
                qty_to_receive = record.product_uom_qty
                qty_recieved = record.qty_received

            if qty_to_receive != 0.0:
                try:
                    percent_received = qty_recieved / qty_to_receive
                except ZeroDivisionError:
                    percent_received = 0.0
            record.percent_received = percent_received
            record.qty_to_receive = qty_to_receive
