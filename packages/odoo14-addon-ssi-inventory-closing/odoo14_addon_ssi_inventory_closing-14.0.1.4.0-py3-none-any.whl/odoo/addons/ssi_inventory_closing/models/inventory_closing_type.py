# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class InventoryClosingType(models.Model):
    _name = "inventory_closing_type"
    _description = "Inventory Closing Type"
    _inherit = [
        "mixin.master_data",
        "mixin.picking_type_m2o_configurator",
        "mixin.picking_type_category_m2o_configurator",
        "mixin.product_product_m2o_configurator",
        "mixin.product_category_m2o_configurator",
    ]

    _product_product_m2o_configurator_insert_form_element_ok = True
    _product_product_m2o_configurator_form_xpath = "//page[@name='product']"
    _product_category_m2o_configurator_insert_form_element_ok = True
    _product_category_m2o_configurator_form_xpath = "//page[@name='product']"
    _picking_type_m2o_configurator_insert_form_element_ok = True
    _picking_type_m2o_configurator_form_xpath = "//page[@name='inventory']"
    _picking_type_category_m2o_configurator_insert_form_element_ok = True
    _picking_type_category_m2o_configurator_form_xpath = "//page[@name='inventory']"

    picking_type_ids = fields.Many2many(
        relation="rel_inventory_closing_type_2_picking_type",
        column1="inventory_closing_type_id",
        column2="picking_type_id",
    )
    picking_type_category_ids = fields.Many2many(
        relation="rel_inventory_closing_type_2_picking_type_category",
        column1="inventory_closing_type_id",
        column2="picking_type_category_id",
    )
    product_ids = fields.Many2many(
        relation="rel_inventory_closing_type_2_product_product",
        column1="inventory_closing_type_id",
        column2="product_id",
    )
    product_category_ids = fields.Many2many(
        relation="rel_inventory_closing_type_2_product_category",
        column1="inventory_closing_type_id",
        column2="product_category_id",
    )
    journal_id = fields.Many2one(
        string="Journal",
        comodel_name="account.journal",
        required=True,
    )
