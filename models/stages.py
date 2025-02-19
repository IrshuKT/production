from odoo import models, fields, api


class StageOneProduct(models.Model):
    _name = 'stage.one.product'
    _description = 'stage on products'

    product_id = fields.Many2one('product.product', 'Product', ondelete='cascade')
    product_lot = fields.Char('LOT')
    product_qty = fields.Float('QTY')
    product_type = fields.Char('TYPE')
    stage_one_product_id = fields.Many2one('stage.main', ondelete='cascade', string='Product')


class StageOneComponent(models.Model):
    _name = 'stage.one.component'
    _description = 'stage on component'

    product_id = fields.Many2one('product.product', 'Component', ondelete='cascade')
    product_lot = fields.Char('LOT')
    product_qty = fields.Float('QTY')
    product_type = fields.Float('Nos')
    stage_one_component_id = fields.Many2one('stage.main', ondelete='cascade', string='Component')


class StageOneByProduct(models.Model):
    _name = 'stage.one.byproduct'
    _description = 'stage on by product'

    product_id = fields.Many2one('product.product', 'By Product', ondelete='cascade')
    product_lot = fields.Char('LOT')
    product_qty = fields.Float('QTY')
    product_type = fields.Float('TYPE')
    stage_one_byproduct_id = fields.Many2one('stage.main', ondelete='cascade', string='By Product')


class StageTwoProduct(models.Model):
    _name = 'stage.two.product'
    _description = 'stage two products'

    product_id = fields.Many2one('product.product', 'Product', ondelete='cascade')
    product_lot = fields.Char('LOT')
    product_qty = fields.Float('QTY')
    product_type = fields.Char('TYPE')
    stage_two_product_id = fields.Many2one('stage.main', ondelete='cascade')


class StageTwoComponent(models.Model):
    _name = 'stage.two.component'
    _description = 'stage two component'

    product_id = fields.Many2one('product.product', 'Component', ondelete='cascade')
    product_lot = fields.Char('LOT')
    product_qty = fields.Float('QTY')
    product_type = fields.Float('Nos')
    stage_two_component_id = fields.Many2one('stage.main', ondelete='cascade')


class StageTwoByProduct(models.Model):
    _name = 'stage.two.byproduct'
    _description = 'stage two by product'

    product_id = fields.Many2one('product.product', 'By Product', ondelete='cascade')
    product_lot = fields.Char('LOT')
    product_qty = fields.Float('QTY')
    product_type = fields.Float('TYPE')
    stage_two_byproduct_id = fields.Many2one('stage.main', ondelete='cascade')


class StageThreeProduct(models.Model):
    _name = 'stage.three.product'
    _description = 'stage three products'

    product_id = fields.Many2one('product.product', 'Product', ondelete='cascade')
    product_lot = fields.Char('LOT')
    product_qty = fields.Float('QTY')
    product_type = fields.Char('TYPE')
    stage_three_product_id = fields.Many2one('stage.main', ondelete='cascade')


class StageThreeComponent(models.Model):
    _name = 'stage.three.component'
    _description = 'stage three component'

    product_id = fields.Many2one('product.product', 'Component', ondelete='cascade')
    product_lot = fields.Char('LOT')
    product_qty = fields.Float('QTY')
    product_type = fields.Float('Nos')
    stage_three_component_id = fields.Many2one('stage.main', ondelete='cascade')


class StageThreeByProduct(models.Model):
    _name = 'stage.three.byproduct'
    _description = 'stage three by product'

    product_id = fields.Many2one('product.product', 'By Product', ondelete='cascade')
    product_lot = fields.Char('LOT')
    product_qty = fields.Float('QTY')
    product_type = fields.Float('TYPE')
    stage_three_byproduct_id = fields.Many2one('stage.main', ondelete='cascade')


class StageFourProduct(models.Model):
    _name = 'stage.four.product'
    _description = 'stage four products'

    product_id = fields.Many2one('product.product', 'Product', ondelete='cascade')
    product_lot = fields.Char('LOT')
    product_qty = fields.Float('QTY')
    product_type = fields.Char('TYPE')
    stage_four_product_id = fields.Many2one('stage.main', ondelete='cascade')


class StageFourComponent(models.Model):
    _name = 'stage.four.component'
    _description = 'stage four component'

    product_id = fields.Many2one('product.product', 'Component', ondelete='cascade')
    product_lot = fields.Char('LOT')
    product_qty = fields.Float('QTY')
    product_type = fields.Float('Nos')
    stage_four_component_id = fields.Many2one('stage.main', ondelete='cascade')


class StageFourByProduct(models.Model):
    _name = 'stage.four.byproduct'
    _description = 'stage four by product'

    product_id = fields.Many2one('product.product', 'By Product', ondelete='cascade')
    product_lot = fields.Char('LOT')
    product_qty = fields.Float('QTY')
    product_type = fields.Float('TYPE')
    stage_four_byproduct_id = fields.Many2one('stage.main', ondelete='cascade')


class StageFiveProduct(models.Model):
    _name = 'stage.five.product'
    _description = 'stage five products'

    product_id = fields.Many2one('product.product', 'Product', ondelete='cascade')
    product_lot = fields.Char('LOT')
    product_qty = fields.Float('QTY')
    product_type = fields.Char('TYPE')
    stage_five_product_id = fields.Many2one('stage.main', ondelete='cascade')


class StageFiveComponent(models.Model):
    _name = 'stage.five.component'
    _description = 'stage five component'

    product_id = fields.Many2one('product.product', 'Component', ondelete='cascade')
    product_lot = fields.Char('LOT')
    product_qty = fields.Float('QTY')
    product_type = fields.Float('Nos')
    stage_five_component_id = fields.Many2one('stage.main', ondelete='cascade')


class StageFiveByProduct(models.Model):
    _name = 'stage.five.byproduct'
    _description = 'stage five by product'

    product_id = fields.Many2one('product.product', 'By Product', ondelete='cascade')
    product_lot = fields.Char('LOT')
    product_qty = fields.Float('QTY')
    product_type = fields.Float('TYPE')
    stage_five_byproduct_id = fields.Many2one('stage.main', ondelete='cascade')


class StageSixProduct(models.Model):
    _name = 'stage.six.product'
    _description = 'stage six products'

    product_id = fields.Many2one('product.product', 'Product', ondelete='cascade')
    product_lot = fields.Char('LOT')
    product_qty = fields.Float('QTY')
    product_type = fields.Char('TYPE')
    stage_six_product_id = fields.Many2one('stage.main', ondelete='cascade')


class StageSixComponent(models.Model):
    _name = 'stage.six.component'
    _description = 'stage six component'

    product_id = fields.Many2one('product.product', 'Component', ondelete='cascade')
    product_lot = fields.Char('LOT')
    product_qty = fields.Float('QTY')
    product_type = fields.Float('Nos')
    stage_six_component_id = fields.Many2one('stage.main', ondelete='cascade')


class StageSixByProduct(models.Model):
    _name = 'stage.six.byproduct'
    _description = 'stage six by product'

    product_id = fields.Many2one('product.product', 'By Product', ondelete='cascade')
    product_lot = fields.Char('LOT')
    product_qty = fields.Float('QTY')
    product_type = fields.Float('TYPE')
    stage_six_byproduct_id = fields.Many2one('stage.main', ondelete='cascade')
