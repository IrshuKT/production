from odoo import models, fields, api, exceptions
from odoo.exceptions import UserError, ValidationError
import logging
_logger = logging.getLogger(__name__)


class StageMain(models.Model):
    _name = 'stage.main'
    _description = 'Main Entry Display'

    voucher_no = fields.Char('Voucher Number')
    remarks = fields.Text('Remarks')
    stage_status = fields.Selection([
        ('stage_1', 'STAGE 1'), ('stage_2', 'STAGE 2')
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

    @api.onchange('product_one_id')
    def _onchange_product_stage_1(self):
        """Fetch BoM when selecting a product in Stage 1."""
        self._fetch_bom_data(self.product_one_id, 'stage_1')

    @api.onchange('product_two_id')
    def _onchange_product_stage_2(self):
        """Fetch BoM when selecting a product in Stage 2."""
        self._fetch_bom_data(self.product_two_id, 'stage_2')

    @api.onchange('product_three_id')
    def _onchange_product_stage_3(self):
        """Fetch BoM when selecting a product in Stage 3."""
        self._fetch_bom_data(self.product_three_id, 'stage_3')

    @api.onchange('product_four_ids')
    def _onchange_product_stage_4(self):
        """Fetch BoM when selecting a product in Stage 3."""
        self._fetch_bom_data(self.product_four_id, 'stage_4')

    @api.onchange('product_five_ids')
    def _onchange_product_stage_5(self):
        """Fetch BoM when selecting a product in Stage 3."""
        self._fetch_bom_data(self.product_five_id, 'stage_5')

    @api.onchange('product_six_ids')
    def _onchange_product_stage_6(self):
        """Fetch BoM when selecting a product in Stage 3."""
        self._fetch_bom_data(self.product_six_id, 'stage_6')

    def _fetch_bom_data(self, produced_ids, stage):
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

        if not bom:
            _logger.warning(f"No BOM found for {current_product.name}")
            return

        component_data = [(0, 0, {'product_id': line.product_id.id, 'product_qty': line.product_qty}) for line in bom.bom_line_ids]
        by_product_data = [(0, 0, {'product_id': byproduct.product_id.id, 'product_qty': byproduct.product_qty}) for byproduct in
                           bom.byproduct_ids]

        # Assign to the correct stage
        if stage == 'stage_1':
            self.component_one_id = component_data
            self.byproduct_one_id = by_product_data
        elif stage == 'stage_2':
            self.component_two_id = component_data
            self.byproduct_two_id = by_product_data
        elif stage == 'stage_3':
            self.component_three_ids = component_data
            self.byproduct_three_ids = by_product_data
        elif stage == 'stage_4':
            self.component_four_ids = component_data
            self.byproduct_four_ids = by_product_data
        elif stage == 'stage_5':
            self.component_five_ids = component_data
            self.byproduct_five_ids = by_product_data
        elif stage == 'stage_6':
            self.component_six_ids = component_data
            self.byproduct_six_ids = by_product_data

        _logger.info(f"Updated components and by-products for {stage}")

    def _clear_stage_data(self, stage):
        """Clears previous data before updating new BoM details."""
        if stage == 'stage_1':
            self.component_ids = [(5, 0, 0)]
            self.by_product_ids = [(5, 0, 0)]
        elif stage == 'stage_2':
            self.component_two_ids = [(5, 0, 0)]
            self.by_product_two_ids = [(5, 0, 0)]
        elif stage == 'stage_3':
            self.component_three_ids = [(5, 0, 0)]
            self.by_product_three_ids = [(5, 0, 0)]
        elif stage == 'stage_4':
            self.component_four_ids = [(5, 0, 0)]
            self.by_product_four_ids = [(5, 0, 0)]
        elif stage == 'stage_5':
            self.component_five_ids = [(5, 0, 0)]
            self.by_product_five_ids = [(5, 0, 0)]
        elif stage == 'stage_6':
            self.component_six_ids = [(5, 0, 0)]
            self.by_product_six_ids = [(5, 0, 0)]

    def create_bom(self):
        """Create a BoM from the selected components, by-products, and working hours for the current stage."""
        if not self.product_id:
            raise UserError("Please select a product.")

        # Determine the current stage components and by-products
        if self.stage_status == 'stage_1':
            components = self.component_ids
            byproducts = self.by_product_ids
        elif self.stage_status == 'stage_2':
            components = self.component_two_ids
            byproducts = self.by_product_two_ids
        elif self.stage_status == 'stage_3':
            components = self.component_three_ids
            byproducts = self.by_product_three_ids
        elif self.stage_status == 'stage_4':
            components = self.component_four_ids
            byproducts = self.by_product_four_ids
        elif self.stage_status == 'stage_5':
            components = self.component_five_ids
            byproducts = self.by_product_five_ids
        elif self.stage_status == 'stage_6':
            components = self.component_six_ids
            byproducts = self.by_product_six_ids
        else:
            raise UserError("Invalid stage status.")

        if not components or not byproducts:
            raise UserError("Please select components and by-products for the current stage.")

        # Create BoM
        bom = self.env['mrp.bom'].create({
            'product_tmpl_id': self.product_id.product_tmpl_id.id,
            'product_qty': self.qty,
            'type': 'normal',
        })

        # Add components to BoM lines
        for component in components:
            self.env['mrp.bom.line'].create({
                'bom_id': bom.id,
                'product_id': component.name.id,
                'product_qty': component.qty,
            })

        # Add by-products to BoM byproducts
        for byproduct in byproducts:
            self.env['mrp.bom.byproduct'].create({
                'bom_id': bom.id,
                'product_id': byproduct.name.id,
                'product_qty': byproduct.qty,
            })

        # Log working hours and labour names
        self.stage_one_ids = [(0, 0, {
            'start_time': fields.Datetime.now(),
            'end_time': fields.Datetime.now(),
            'employee_ids': [(6, 0, self.labour_ids.ids)],
            'machine_name': 'Custom Machine',
            'working_hours': self.working_hours,
        })]

        _logger.info(f"BoM created for product: {self.product_id.name} in stage: {self.stage_status}")

    def _get_product_id(self, vals):
        """Determine the product_id based on the current stage."""
        if self.stage_status == 'stage_1' and 'product_one_id' in vals:
            produced_ids = vals.get('produced_ids', [])
            if produced_ids:
                return produced_ids[0][2].get('name')  # Fetch product_id from produced_ids
        elif self.stage_status == 'stage_2' and 'product_two_id' in vals:
            produced_two_ids = vals.get('produced_two_ids', [])
            if produced_two_ids:
                return produced_two_ids[0][2].get('name')  # Fetch product_id from produced_two_ids
        elif self.stage_status == 'stage_3' and 'product_three_id' in vals:
            produced_three_ids = vals.get('product_three_id', [])
            if produced_three_ids:
                return produced_three_ids[0][2].get('name')  # Fetch product_id from produced_three_ids
        # Repeat for other stages (stage_4, stage_5, stage_6)...

        # If no product_id is found, return None
        return None

    @api.model
    def create(self, vals):
        """Override create method to ensure product_id is set."""
        _logger.info(f"Creating record with values: {vals}")

        # Fetch product_id based on the current stage
        product_id = self._get_product_id(vals)
        if not product_id:
            raise ValidationError("Product is required to create a production stage.")

        # Ensure product_id is set in vals
        vals['product_id'] = product_id

        return super(StageMain, self).create(vals)

    def write(self, vals):
        """Override write method to ensure product_id is set."""
        _logger.info(f"Updating record with values: {vals}")

        # Fetch product_id based on the current stage
        product_id = self._get_product_id(vals)
        if 'product_id' in vals and not vals['product_id']:
            if not product_id:
                raise ValidationError("Product is required to update a production stage.")
            vals['product_id'] = product_id

        return super(StageMain, self).write(vals)