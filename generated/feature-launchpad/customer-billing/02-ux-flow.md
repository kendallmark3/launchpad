# UX Flow — customer-billing

## User Entry Point

### Account Owner

- Navigates to **Billing Dashboard** via a "Billing" or "Subscription" link in account settings menu.
- **Not specified:** Whether the entry point is labeled "Billing," "Subscription," "Plan & Billing," or another term.
- **Not specified:** Whether the entry point is available from other locations (e.g., in-app prompts when approaching usage limits).

### Support Rep

- Accesses a customer's **Billing Dashboard (Read-Only)** from an admin view.
- **Not specified:** The exact entry point within the admin interface (e.g., customer detail page, search, or dedicated billing lookup tool).

---

## Step-by-Step Journey

### Primary Journey (Account Owner upgrading or downgrading)

1. **Account Owner** clicks the billing/subscription link in account settings.
2. System loads **Billing Dashboard** screen (see Required Screens).
3. Account Owner reviews current plan, usage, and past invoices.
4. Account Owner clicks "Change plan" button.
5. System navigates to **Plan Comparison** screen showing available plans side by side.
6. Account Owner selects a different plan.
7. System displays **Change Plan Confirmation** screen with:
   - New plan name and price
   - Prorated cost (if any)
   - Effective date
8. Account Owner confirms the change.
9. System processes the plan change via `POST /billing/plan-change`.
10. System displays success confirmation (see Success States).

### Secondary Journey (Account Owner viewing invoices)

1. **Account Owner** lands on **Billing Dashboard**.
2. Account Owner scrolls to invoice list.
3. Account Owner clicks an invoice row.
4. System navigates to **Invoice Detail** screen.
5. Account Owner reviews invoice line items (details not specified).
6. Account Owner optionally downloads PDF via download button.
7. Account Owner returns to Billing Dashboard.

### Support Rep Journey (read-only)

1. **Support Rep** navigates to a customer's billing information from admin view.
2. System loads **Billing Dashboard (Read-Only)** with the same information an Account Owner sees.
3. Support Rep reviews current plan, usage, and invoices.
4. **Not specified:** Whether the Support Rep can access Invoice Detail screens or download PDFs.

---

## Decision Points

### On Billing Dashboard

- **View invoices:** Account Owner may click any invoice to see detail or download PDF.
- **Change plan:** Account Owner may click "Change plan" to compare and switch plans.
- **No action:** Account Owner may simply review information and leave.

### On Plan Comparison

- **Select a different plan:** Account Owner chooses a new plan (upgrade or downgrade).
- **Cancel/Go back:** Account Owner returns to Billing Dashboard without changing plan.
- **Not specified:** Whether the user can select their current plan (likely disabled or results in no-op).

### On Change Plan Confirmation

- **Confirm change:** Account Owner proceeds with the plan change.
- **Cancel/Go back:** Account Owner returns to Plan Comparison or Billing Dashboard without making the change.

---

## Alternate Paths

### Account Owner cancels during plan change

- From **Plan Comparison** or **Change Plan Confirmation**, Account Owner clicks "Cancel" or "Back."
- System returns to **Billing Dashboard** with no changes applied.

### Support Rep attempts to change a plan

- **Not specified:** Whether the UI explicitly disables the "Change plan" button for Support Reps or whether clicking it shows an error/message.
- Expected behavior: Support Rep should **not** be able to initiate or confirm a plan change.

### Account Owner on free or trial plan

- **Not specified:** Whether free/trial accounts have access to the Billing Dashboard or see a different starting state.
- **Not specified:** Whether usage limits and renewal dates apply to free/trial plans.

---

## Empty States

### No invoices yet

- Billing Dashboard invoice list shows:
  - **Not specified:** Message text (e.g., "No invoices yet" or "You'll see invoices here once your first payment is processed").
  - **Not specified:** Whether any call-to-action or help text is displayed.

### No usage recorded

- **Not specified:** How the usage display behaves when usage is zero (e.g., "0 / 10 seats used" or a distinct empty message).

### No available plans to compare

- **Not specified:** Whether a scenario exists where Plan Comparison would be empty (e.g., account locked or custom enterprise plan).

---

## Error States

### API failures

#### `GET /billing/summary` fails

- Billing Dashboard cannot load current plan, usage, or renewal date.
- **Not specified:** Error message text or retry mechanism.
- **Not specified:** Whether partial data (e.g., cached invoice list) is shown.

#### `GET /billing/invoices` fails

- Invoice list cannot load or paginate.
- **Not specified:** Error message text, retry mechanism, or fallback behavior.

#### `POST /billing/plan-change` fails

- Plan change cannot be processed after user confirms.
- **Not specified:** Error message text (e.g., "We couldn't process your plan change. Please try again or contact support.").
- **Not specified:** Whether the user remains on Change Plan Confirmation or is returned to Plan Comparison.
- **Not specified:** Whether the user can retry immediately.

### Invoice PDF download fails

- **Not specified:** Error handling when PDF download endpoint fails or times out.

### Permission denied

- **Support Rep** attempts an action restricted to Account Owners (e.g., clicking a non-disabled "Change plan" button).
- **Not specified:** Error message or inline prevention mechanism.

### Session timeout or authentication error

- **Not specified:** Behavior if user session expires while on Billing Dashboard or mid-plan-change.

---

## Confirmation States

### Before confirming plan change

- **Change Plan Confirmation** screen displays:
  - Selected plan name and price
  - Prorated cost (or $0.00 if none)
  - Effective date of the change
  - Explicit "Confirm" and "Cancel" actions
- **Not specified:** Whether current plan is shown for comparison on this screen.
- **Not specified:** Whether any additional terms, policies, or impact on features are displayed.

### Invoice download confirmation

- **Not specified:** Whether clicking "Download PDF" triggers an immediate download or shows a confirmation/loading state.

---

## Success States

### Plan change successful

- After `POST /billing/plan-change` succeeds, system shows:
  - **Not specified:** Whether success is shown as a modal, toast, inline message, or dedicated success screen.
  - **Not specified:** Exact message text (e.g., "Your plan has been changed to [Plan Name]. Changes take effect on [Date].").
- User is returned to **Billing Dashboard** showing the updated plan.
- **Not specified:** Whether the new plan is reflected immediately or marked as "effective [future date]."

### Invoice PDF downloaded

- **Not specified:** Success feedback mechanism (e.g., browser download notification only, or in-app toast message).

---

## Required Screens

### 1. Billing Dashboard

**Audience:** Account Owner (read/write), Support Rep (read-only)

**Content:**

- **Current plan section:**
  - Plan name
  - Price (with billing cycle if applicable)
  - Renewal date
- **Usage summary section:**
  - Usage against plan limits (e.g., "8 / 10 seats used")
  - **Not specified:** Format when multiple usage dimensions exist (e.g., seats + storage).
- **Invoice list section:**
  - Paginated table/list of invoices
  - Columns: Date, Amount, Status (e.g., Paid, Pending, Failed)
  - Action: Click row to view detail; download PDF per invoice
- **Change plan button** (visible/enabled only for Account Owner)

**Not specified:**

- Whether usage summary shows graphs, progress bars, or plain text.
- Whether invoices default to showing the most recent first.
- Pagination controls (e.g., page numbers, infinite scroll, "Load more").

### 2. Plan Comparison

**Audience:** Account Owner only

**Content:**

- Side-by-side display of available plans
- **Not specified:** Which plan attributes are shown (e.g., price, limits, features).
- **Not specified:** Whether the current plan is visually highlighted or badged.
- Selection mechanism (e.g., radio buttons, "Select" button per plan).
- "Cancel" or "Back" action to return to Billing Dashboard.

**Not specified:**

- Whether plans are shown in a fixed order (e.g., ascending price).
- How many plans are typically available.

### 3. Change Plan Confirmation

**Audience:** Account Owner only

**Content:**

- New plan name and price
- Prorated cost
- Effective date
- "Confirm" button
- "Cancel" or "Back" button

**Not specified:**

- Whether this is a modal overlay or full-page screen.

### 4. Invoice Detail

**Audience:** Account Owner (and possibly Support Rep, not specified)

**Content:**

- Invoice metadata: date, amount, status
- **Not specified:** Line items, taxes, payment method used, billing address.
- "Download PDF" button
- "Back" or close action to return to Billing Dashboard

**Not specified:**

- Full layout and detail level of invoice information.

---

## Screen Transitions

### From Billing Dashboard

- **To Plan Comparison:** User clicks "Change plan."
- **To Invoice Detail:** User clicks an invoice row.

### From Plan Comparison

- **To Change Plan Confirmation:** User selects a plan.
- **Back to Billing Dashboard:** User clicks "Cancel" or "Back."

### From Change Plan Confirmation

- **To Billing Dashboard (with success state):** User clicks "Confirm" and `POST /billing/plan-change` succeeds.
- **Back to Plan Comparison** (or stays on Confirmation): User clicks "Cancel," or an error occurs.
  - **Not specified:** Exact destination after cancel or error.

### From Invoice Detail

- **Back to Billing Dashboard:** User clicks "Back" or close button.

### On error (any screen)

- **Not specified:** Whether user is transitioned to an error screen or shown inline/modal error with option to retry or return.

---

## User Permissions or Roles

### Account Owner

- **Can:**
  - View Billing Dashboard (current plan, usage, invoices)
  - Navigate to Plan Comparison
  - Change plan (upgrade or downgrade)
  - View Invoice Detail
  - Download invoice PDFs
- **Cannot:**
  - Manage payment methods (out of scope)
  - Change billing cycle (out of scope)

### Support Rep

- **Can:**
  - View Billing Dashboard (read-only) for any customer from admin view
  - **Not specified:** View Invoice Detail or download PDFs
- **Cannot:**
  - Change a customer's plan
  - **Not specified:** Whether Support Rep can initiate any write actions in the billing context

### Not specified

- Whether other user roles exist (e.g., Account Admin, Billing Admin, Team Member).
- Whether multiple Account Owners can exist per account and if permissions differ.
- Authentication or authorization mechanism (e.g., OAuth, session-based).
- How the system distinguishes an Account Owner from other users (e.g., role flag, account ownership field).

---

**End of UX Flow**
