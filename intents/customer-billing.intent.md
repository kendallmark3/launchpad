# Feature Intent

> Sample fixture intent file, used as the running example throughout `intent.md`
> (Sections 2 and 6) and as a smoke-test input for `feature_launchpad`. Not a real
> product requirement.

## Business Goal

Reduce support tickets related to billing by letting customers view their current
plan, usage, and invoices, and self-serve an upgrade or downgrade without contacting
support.

## User Personas

- **Account Owner** — the paying customer; can view and change the subscription plan.
- **Support Rep** — internal user; needs read-only visibility into a customer's billing
  state to answer questions, but cannot change the plan on the customer's behalf.

## User Journey

1. Account Owner navigates to the billing dashboard from account settings.
2. They see their current plan, usage against plan limits, and a list of past invoices.
3. They choose "Change plan" and compare available plans.
4. They confirm the change and see a confirmation with the new billing amount and
   effective date.

## Required Screens

- Billing Dashboard (current plan, usage summary, invoice list)
- Plan Comparison (available plans side by side)
- Change Plan Confirmation
- Invoice Detail

## Functional Requirements

- Display the customer's current plan name, price, and renewal date.
- Display usage against plan limits (e.g. seats used / seats included).
- List invoices with date, amount, and status; allow downloading a PDF per invoice.
- Allow switching to any other available plan; show prorated cost before confirming.
- Support reps can view (but not edit) a customer's billing dashboard from an admin
  view.

## Non-Functional Requirements

- Billing dashboard must load within 2 seconds for accounts with up to 5 years of
  invoice history.
- All billing data must be encrypted at rest and in transit.
- Screens must meet WCAG 2.1 AA accessibility standards.

## Design Constraints

- Must reuse the existing design system's table and card components.
- Must work within the existing account settings navigation shell.

## API / Data Requirements

- Requires a `GET /billing/summary` endpoint returning current plan, usage, and
  renewal date.
- Requires a `GET /billing/invoices` endpoint (paginated) returning invoice records.
- Requires a `POST /billing/plan-change` endpoint accepting a target plan ID and
  returning the prorated cost and effective date.

## Acceptance Criteria

- An Account Owner can view their current plan and usage without contacting support.
- An Account Owner can change plans and see a confirmation with the correct prorated
  cost.
- A Support Rep can view (read-only) a customer's billing dashboard from the admin
  view.

## Validation Expectations

- Unit tests for prorated-cost calculation across upgrade and downgrade paths.
- Smoke test confirming the billing dashboard renders for an account with zero
  invoices (empty state).

## Out of Scope

- Payment method management (adding/removing credit cards) — handled by an existing,
  separate flow.
- Annual vs. monthly billing cycle changes.
