# -*- coding: utf-8 -*-

import logging
from odoo import api, fields, models, _

_logger = logging.getLogger(__name__)

class SaleSubscription(models.Model):
    """
    Extends the sale.subscription model to align with CreativeFlow's specific
    requirements, such as linking to users and auto-granting credits.
    """
    _inherit = 'sale.subscription'

    cf_linked_user_id = fields.Many2one(
        comodel_name='res.users',
        string="CreativeFlow User",
        compute='_compute_cf_linked_user_id',
        store=True,
        readonly=True,
        help="The CreativeFlow platform user associated with this Odoo subscription. Typically linked via partner's email or external ID."
    )

    cf_subscription_tier_product = fields.Selection(
        related='template_id.product_id.cf_subscription_tier_provided',
        string="CF Tier (from Product)",
        readonly=True,
        store=True,
    )

    cf_initial_credits_on_period_start = fields.Float(
        string="Initial Credits per Period",
        related='template_id.product_id.cf_credits_granted_on_period_start',
        help="Number of credits to grant the user at the start of each subscription period (e.g., monthly Pro credits). Fetched from the subscription product.",
        readonly=True
    )

    cf_payment_provider_subscription_id = fields.Char(
        string="Payment Provider Subscription ID",
        copy=False,
        help="Subscription ID from external payment provider (e.g., Stripe, PayPal) for reconciliation."
    )

    @api.depends('partner_id', 'partner_id.user_ids', 'partner_id.email')
    def _compute_cf_linked_user_id(self):
        """
        Attempts to find a res.users record linked to the subscription's partner.
        The logic prioritizes direct user links on the partner, then email.
        """
        for sub in self:
            user = self.env['res.users']
            if sub.partner_id:
                # Priority 1: Partner has one linked user
                if len(sub.partner_id.user_ids) == 1:
                    user = sub.partner_id.user_ids
                # Priority 2: Search by partner_id on users model
                else:
                    user = self.env['res.users'].search([('partner_id', '=', sub.partner_id.id)], limit=1)
                # Priority 3: Search by email if still not found
                if not user and sub.partner_id.email:
                    user = self.env['res.users'].search([('login', '=', sub.partner_id.email)], limit=1)

            sub.cf_linked_user_id = user

    def _recurring_create_invoice(self, automatic=False, auto_commit=False):
        """
        Extend the invoice creation to grant credits after a successful payment.
        The actual credit grant happens after the invoice is confirmed paid.
        """
        invoices = super(SaleSubscription, self)._recurring_create_invoice(automatic, auto_commit)
        # We hook into the payment process, this is a placeholder for where the logic could be triggered.
        # A more robust way is to observe the invoice state changing to 'paid'.
        # Let's add the logic to the `_handle_subscription_payment` method which is more appropriate
        return invoices

    def _handle_subscription_payment(self, invoices):
        """
        This is a conceptual method that would be called after a successful payment.
        Odoo's `sale_subscription` doesn't have a direct hook like this, so we often
        override `_do_payment` or observe `account.move` state changes.
        For this implementation, we will assume this logic is called post-payment.
        Let's override `_do_payment` as it is a more direct approach.
        """
        # This method is illustrative. See the override of _do_payment below.
        pass

    def _do_payment(self, payment_token, invoice):
        """
        Override the payment processing method to grant credits upon success.
        """
        res = super(SaleSubscription, self)._do_payment(payment_token, invoice)
        # res is a boolean in standard sale_subscription _do_payment, indicating success
        if res:
            for sub in self:
                # Check if the invoice is paid
                if invoice.payment_state in ('paid', 'in_payment'):
                    if sub.cf_linked_user_id and sub.cf_initial_credits_on_period_start > 0:
                        _logger.info(f"Granting {sub.cf_initial_credits_on_period_start} credits to user {sub.cf_linked_user_id.name} for subscription {sub.code}.")
                        sub.cf_linked_user_id.action_credit_credits(
                            amount_to_credit=sub.cf_initial_credits_on_period_start,
                            action_type='purchase',
                            description=f"Monthly credits for subscription {sub.code}",
                            external_reference_model='sale.subscription',
                            external_reference_id=sub.id
                        )
        return res

    @api.model
    def _cron_update_user_subscription_tier(self):
        """
        A cron job can be set up to periodically sync the subscription tier to the user,
        as state changes might not always be triggered by methods we can easily override.
        """
        for sub in self.search([('cf_linked_user_id', '!=', False)]):
            sub._update_user_tier()


    def _update_user_tier(self):
        """
        Updates the linked user's subscription tier based on the subscription's state.
        """
        self.ensure_one()
        if self.cf_linked_user_id:
            new_tier = 'free' # Default to free if subscription is closed/inactive
            if self.in_progress:
                new_tier = self.cf_subscription_tier_product or 'free'

            if self.cf_linked_user_id.cf_subscription_tier != new_tier:
                self.cf_linked_user_id.write({'cf_subscription_tier': new_tier})
                _logger.info(f"Updated subscription tier for user {self.cf_linked_user_id.name} to '{new_tier}' from subscription {self.code}.")


    def set_close(self, *args, **kwargs):
        """
        When a subscription is closed, update the user's tier.
        """
        res = super(SaleSubscription, self).set_close(*args, **kwargs)
        for sub in self:
            sub._update_user_tier()
        return res

    def set_open(self, *args, **kwargs):
        """
        When a subscription is started or re-opened, update the user's tier.
        """
        res = super(SaleSubscription, self).set_open(*args, **kwargs)
        for sub in self:
            sub._update_user_tier()
        return res