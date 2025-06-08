from odoo import fields, models, api
import logging
from pytz import UTC
from odoo.osv import expression

class ResPartner(models.Model):
    _inherit = 'res.partner'

    # Define a selection field for member state with three options: Draft, Approved, Black List
    member_state = fields.Selection(
        [('draft', 'Draft'), ('approved', 'Approved'), ('black_list', 'Black List')],
        string='Field State',
        default='draft' 
    )
    
    arabic_fullname = fields.Char(string=" ", placeholder='ادخل اسم العضو')
    first_arabic = fields.Char(string="First Name")
    second_arabic = fields.Char(string="Second Name")
    renew_date = fields.Datetime(string="Last Renewal Date")

    # Method to set the member state to 'Approved'
    def action_set_approved(self):
        self.write({'member_state': 'approved'})

    # Method to set the member state to 'Black List'
    def action_set_blacklisted(self):
        self.write({'member_state': 'black_list'})

    # Method to set the member state to 'Draft'
    def action_set_draft(self):
        self.write({'member_state': 'draft'})

    # Onchange method triggered when arabic_fullname is modified
    @api.onchange('arabic_fullname')
    def _onchange_arabic_fullname(self):
        if self.arabic_fullname:
            # Split the full name by spaces to separate first and second names
            parts = self.arabic_fullname.split()
            if len(parts) >= 2:
                # Assign first part to first_arabic and second part to second_arabic
                self.first_arabic = parts[0]
                self.second_arabic = parts[1]
            elif len(parts) == 1:
                # If only one part, assign it to first_arabic and clear second_arabic
                self.first_arabic = parts[0]
                self.second_arabic = False

    # Override the _search method to implement custom contact search logic based on user groups
    @api.model
    def _search(self, args, offset=0, limit=None, order=None, count=False, access_rights_uid=None):
        # Check if the user belongs to the 'View All Members' group
        if self.env.user.has_group('membership_managment.group_view_all_member'):
            # No restrictions applied; users can access all partners
            pass
        # Check if the user belongs to the 'Approved Partners Only' group
        elif self.env.user.has_group('membership_managment.group_approved_partners_only'):
            # Restrict search to only partners with 'approved' member_state
            approved_domain = [('member_state', '=', 'approved')]
            args = expression.AND([args or [], approved_domain])
        else:
            # If user is in neither group, restrict access to no records
            args = expression.AND([args or [], [('id', '=', False)]])
        # Call the parent _search method with the modified args
        return super(ResPartner, self)._search(
            args, offset=offset, limit=limit, order=order, count=count, access_rights_uid=access_rights_uid
        )


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    # Override the action_confirm method to save the date 
    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        
        # Update the renew_date of the partner when the sale order is confirmed
        for order in self:
            # Check if the sale order has a template, a partner, and a date_order
            if self.sale_order_template_id and self.partner_id and order.date_order:
                # Update the partner's renew_date with the sale order's date_order
                order.partner_id.write({'renew_date': order.date_order})
                
        return res