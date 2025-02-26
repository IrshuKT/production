from odoo import models, fields, api, _, exceptions
from odoo.exceptions import UserError, ValidationError
import logging
import xml.etree.ElementTree as ET
import io
import base64
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment
from lxml import etree

_logger = logging.getLogger(__name__)


class StageMain(models.Model):
    _name = 'stage.main'
    _description = 'Main Entry Display'

    voucher_no = fields.Char('Voucher Number')
    remarks = fields.Text('Remarks')
    stage_status = fields.Selection([
        ('stage_1', 'STAGE 1'), ('stage_2', 'STAGE 2'), ('stage_3', 'STAGE 3'), ('stage_4', 'STAGE 4'),
        ('stage_5', 'STAGE 5'), ('stage_6', 'STAGE 6')
    ], default='stage_1', string='Stage Status')

    product_one_id = fields.One2many('stage.one.product', 'stage_one_product_id', ondelete='cascade')
    component_one_id = fields.One2many('stage.one.component', 'stage_one_component_id', ondelete='cascade')
    byproduct_one_id = fields.One2many('stage.one.byproduct', 'stage_one_byproduct_id', ondelete='cascade')

    product_two_id = fields.One2many('stage.two.product', 'stage_two_product_id', ondelete='cascade')
    component_two_id = fields.One2many('stage.two.component', 'stage_two_component_id', ondelete='cascade')
    byproduct_two_id = fields.One2many('stage.two.byproduct', 'stage_two_byproduct_id', ondelete='cascade')

    product_three_id = fields.One2many('stage.three.product', 'stage_three_product_id', ondelete='cascade')
    component_three_id = fields.One2many('stage.three.component', 'stage_three_component_id', ondelete='cascade')
    byproduct_three_id = fields.One2many('stage.three.byproduct', 'stage_three_byproduct_id', ondelete='cascade')

    product_four_id = fields.One2many('stage.four.product', 'stage_four_product_id', ondelete='cascade')
    component_four_id = fields.One2many('stage.four.component', 'stage_four_component_id', ondelete='cascade')
    byproduct_four_id = fields.One2many('stage.four.byproduct', 'stage_four_byproduct_id', ondelete='cascade')

    product_five_id = fields.One2many('stage.five.product', 'stage_five_product_id', ondelete='cascade')
    component_five_id = fields.One2many('stage.five.component', 'stage_five_component_id', ondelete='cascade')
    byproduct_five_id = fields.One2many('stage.five.byproduct', 'stage_five_byproduct_id', ondelete='cascade')

    product_six_id = fields.One2many('stage.six.product', 'stage_six_product_id', ondelete='cascade')
    component_six_id = fields.One2many('stage.six.component', 'stage_six_component_id', ondelete='cascade')
    byproduct_six_id = fields.One2many('stage.six.byproduct', 'stage_six_byproduct_id', ondelete='cascade')

    stage_readonly = fields.Boolean(compute="_compute_stage_readonly", store=True)
    # stage_button_invisible = fields.Boolean(compute="_compute_stage_button_invisible")
    stage_1_readonly = fields.Boolean(string='Stage 1 Readonly', default=False)
    stage_2_readonly = fields.Boolean(string='Stage 2 Readonly', default=False)
    stage_3_readonly = fields.Boolean(string='Stage 3 Readonly', default=False)
    stage_4_readonly = fields.Boolean(string='Stage 4 Readonly', default=False)
    stage_5_readonly = fields.Boolean(string='Stage 5 Readonly', default=False)
    stage_6_readonly = fields.Boolean(string='Stage 6 Readonly', default=False)

    #Pdf print action

    def action_print_report(self):
        return self.env.ref('stage.stage_report_action').report_action(self)

    def get_stage_data(self):
        """Prepare stage data for the report."""
        self.ensure_one()
        stage_data = []

        stage_number_to_word = {
            1: 'one',
            2: 'two',
            3: 'three',
            4: 'four',
            5: 'five',
            6: 'six',
        }

        form_view = self.env['ir.ui.view'].search([
            ('model', '=', 'stage.main'),
            ('type', '=', 'form'),
        ], limit=1)

        if form_view:
            # Parse the form view arch to extract page strings
            try:
                arch = etree.fromstring(form_view.arch)
                pages = arch.xpath("//page[@name]")

                for page in pages:
                    page_name = page.get('name')
                    page_string = page.get('string', f'Stage {page_name.split("_")[1]}')  # Default fallback
                    stage_number = int(page_name.split('_')[1])
                    stage_word = stage_number_to_word.get(stage_number, str(stage_number))

                    stage_info = {
                        'stage_name': page_string,  # Use the page string as the stage name
                        'products': self[f'product_{stage_word}_id'],
                        'components': self[f'component_{stage_word}_id'],
                        'byproducts': self[f'byproduct_{stage_word}_id'],
                    }
                    stage_data.append(stage_info)
            except Exception as e:
                _logger.error(f"Error parsing form view arch: {e}")
                # Fallback to default stage names if parsing fails
                for stage_number in range(1, 7):
                    stage_word = stage_number_to_word.get(stage_number, str(stage_number))
                    stage_info = {
                        'stage_name': f'Stage {stage_number}',
                        'products': self[f'product_{stage_word}_id'],
                        'components': self[f'component_{stage_word}_id'],
                        'byproducts': self[f'byproduct_{stage_word}_id'],
                    }
                    stage_data.append(stage_info)

        return stage_data

    

    # Mark previous stages as read-only once moved forward.
    @api.depends('stage_status')
    def _compute_stage_readonly(self):
        stage_order = ['stage_1', 'stage_2', 'stage_3', 'stage_4', 'stage_5', 'stage_6']
        for record in self:
            record.stage_1_readonly = record.stage_status != 'stage_1'
            record.stage_2_readonly = record.stage_status not in ['stage_1', 'stage_2']
            record.stage_3_readonly = record.stage_status not in ['stage_1', 'stage_2', 'stage_3']
            record.stage_4_readonly = record.stage_status not in ['stage_1', 'stage_2', 'stage_3', 'stage_4']
            record.stage_5_readonly = record.stage_status not in ['stage_1', 'stage_2', 'stage_3', 'stage_4', 'stage_5']
            record.stage_6_readonly = record.stage_status == 'stage_6'

    @api.onchange('product_one_id')
    def _onchange_product_stage_1(self):
        self._fetch_bom_data(self.product_one_id, 'stage_1')

    @api.onchange('product_two_id')
    def _onchange_product_stage_2(self):
        self._fetch_bom_data(self.product_two_id, 'stage_2')

    @api.onchange('product_three_id')
    def _onchange_product_stage_3(self):
        self._fetch_bom_data(self.product_three_id, 'stage_3')

    @api.onchange('product_four_id')
    def _onchange_product_stage_4(self):
        self._fetch_bom_data(self.product_four_id, 'stage_4')

    @api.onchange('product_five_id')
    def _onchange_product_stage_5(self):
        self._fetch_bom_data(self.product_five_id, 'stage_5')

    @api.onchange('product_six_id')
    def _onchange_product_stage_6(self):
        self._fetch_bom_data(self.product_six_id, 'stage_6')

    def _fetch_bom_data(self, produced_ids, stage):
        """Fetch BOM data and update components and by-products for the given stage."""
        self._clear_stage_data(stage)

        if not produced_ids:
            return

        current_product = produced_ids.product_id  # Get the selected product
        _logger.info(f"Fetching BOM for {stage} product: {current_product.name}")

        bom = self.env['mrp.bom'].search([
            ('product_tmpl_id', '=', current_product.product_tmpl_id.id),
            ('active', '=', True)
        ], limit=1)

        if bom:
            product_qty_from_bom = bom.product_qty
            produced_ids.write({'product_qty': product_qty_from_bom})
            current_product.product_qty = product_qty_from_bom

            _logger.info(f"Updated {current_product.name} quantity to {product_qty_from_bom} from BOM.")

            component_data = [(0, 0, {'product_id': line.product_id.id, 'product_qty': line.product_qty}) for line in
                              bom.bom_line_ids]
            by_product_data = [(0, 0, {'product_id': byproduct.product_id.id, 'product_qty': byproduct.product_qty}) for
                               byproduct in bom.byproduct_ids]

            # Assign to the correct stage
            stage_map = {
                'stage_1': ('component_one_id', 'byproduct_one_id'),
                'stage_2': ('component_two_id', 'byproduct_two_id'),
                'stage_3': ('component_three_id', 'byproduct_three_id'),
                'stage_4': ('component_four_id', 'byproduct_four_id'),
                'stage_5': ('component_five_id', 'byproduct_five_id'),
                'stage_6': ('component_six_id', 'byproduct_six_id'),
            }

            if stage in stage_map:
                component_field, byproduct_field = stage_map[stage]
                # Write the updated data back to the database
                self.write({
                    component_field: component_data,
                    byproduct_field: by_product_data,
                })

            _logger.info(f"Updated components and by-products for {stage}")
        else:
            _logger.warning(f"No BOM found for {current_product.name}")

    def _clear_stage_data(self, stage):
        """Clears existing components and by-products for a given stage before updating with BOM data."""
        stage_map = {
            'stage_1': ('component_one_id', 'byproduct_one_id'),
            'stage_2': ('component_two_id', 'byproduct_two_id'),
            'stage_3': ('component_three_id', 'byproduct_three_id'),
            'stage_4': ('component_four_id', 'byproduct_four_id'),
            'stage_5': ('component_five_id', 'byproduct_five_id'),
            'stage_6': ('component_six_id', 'byproduct_six_id'),
        }

        if stage in stage_map:
            component_field, byproduct_field = stage_map[stage]
            self.write({
                component_field: [(5, 0, 0)],  # Remove all existing records
                byproduct_field: [(5, 0, 0)],
            })
            _logger.info(f"Cleared existing components and by-products for {stage}.")


    def produce(self):
        self.ensure_one()

        if self.stage_status == 'stage_6':
            raise UserError("Production is complete! No further stages to process.")

        stage_order = ['stage_1', 'stage_2', 'stage_3', 'stage_4', 'stage_5', 'stage_6']
        current_index = stage_order.index(self.stage_status)

        if current_index < len(stage_order) - 1:
            self.stage_status = stage_order[current_index + 1]

        self._compute_stage_readonly()

        self.env.cr.commit()

    def confirm_stage(self):
        self.ensure_one()

        stage_map = {
            'stage_1': (self.product_one_id, self.component_one_id, self.byproduct_one_id),
            'stage_2': (self.product_two_id, self.component_two_id, self.byproduct_two_id),
            'stage_3': (self.product_three_id, self.component_three_id, self.byproduct_three_id),
            'stage_4': (self.product_four_id, self.component_four_id, self.byproduct_four_id),
            'stage_5': (self.product_five_id, self.component_five_id, self.byproduct_five_id),
            'stage_6': (self.product_six_id, self.component_six_id, self.byproduct_six_id),
        }

        products, components, byproducts = stage_map.get(self.stage_status, (False, False, False))

        if not products or not components:
            raise UserError("No products or components found for the current stage.")

        def get_location_by_name(location_name):
            location = self.env['stock.location'].search([('name', '=', location_name)], limit=1)
            if not location:
                raise UserError(f"Location '{location_name}' not found!")
            return location

        source_location_stock = get_location_by_name('Stock')
        location_production = get_location_by_name('Stock')

        for component in components:
            self._create_stock_move(
                product_id=component.product_id,
                quantity=component.product_qty,
                location_id=source_location_stock.id,
                location_dest_id=location_production.id,
            )

        for product in products:
            self._create_stock_move(
                product_id=product.product_id,
                quantity=product.product_qty,
                location_id=location_production.id,
                location_dest_id=source_location_stock.id,
            )

        for byproduct in byproducts:
            self._create_stock_move(
                product_id=byproduct.product_id,
                quantity=byproduct.product_qty,
                location_id=location_production.id,
                location_dest_id=source_location_stock.id,
            )

        stage_order = ['stage_1', 'stage_2', 'stage_3', 'stage_4', 'stage_5', 'stage_6']
        current_index = stage_order.index(self.stage_status)

        if current_index < len(stage_order) - 1:
            self.stage_status = stage_order[current_index + 1]

        self._compute_stage_readonly()

        self.env.cr.commit()

        _logger.info(f"Stage {self.stage_status} confirmed. Stock updated for products, components, and by-products.")

    def _create_stock_move(self, product_id, quantity, location_id, location_dest_id):
        stock_move = self.env['stock.move'].create({
            'product_id': product_id.id,
            'product_uom_qty': quantity,
            'product_uom': product_id.uom_id.id,
            'location_id': location_id,
            'location_dest_id': location_dest_id,
            'name': product_id.name,
            'state': 'draft',
        })

        stock_move._action_confirm()
        stock_move._action_assign()
        for move_line in stock_move.move_line_ids:
            move_line.qty_done = move_line.product_uom_qty
        stock_move._action_done()

        _logger.info(f"Stock move created: {stock_move.name} for product {product_id.name} with quantity {quantity}")