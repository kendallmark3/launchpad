# UX Flow — blackjack-game

## User entry point

**Single entry point:**  
User navigates directly to the game URL in their browser. The Table / Play Screen loads immediately with:

- Starting bankroll displayed (e.g. 1000 chips)
- Empty dealer hand area
- Empty player hand area
- Betting panel visible and active
- Action buttons (Hit, Stand, Double, Split, Insurance) disabled/hidden until a hand is in play
- Strategy Hint toggle visible but inactive until hand is dealt
- Stats panel accessible (collapsed or sidebar, implementation not specified)

**Note:** The intent does not specify a landing page, tutorial, or menu screen separate from the table itself.

---

## Step-by-step journey

### Happy path (single hand, no split, player wins)

1. **Betting phase**  
   - Player sees chip controls (denominations not specified in intent)
   - Player selects chip value(s) and places bet in betting circle
   - Current bet amount displays
   - Player clicks "Confirm" or "Deal" button (exact label not specified)
   - System validates bet ≤ current bankroll

2. **Deal phase**  
   - Two cards dealt to player (both face up)
   - Two cards dealt to dealer (one face up, one face down)
   - Hand totals calculate and display for player hand
   - Soft/hard indicator shows if player has a soft total
   - Shoe indicator updates to reflect cards dealt

3. **Insurance offer (conditional)**  
   - **If** dealer's up-card is an Ace:
     - Insurance prompt appears
     - Player can bet up to half their original bet
     - Player confirms or declines
   - **Else:** skip to player action phase

4. **Player action phase**  
   - Available actions highlight based on game state:
     - **Hit** — always available until stand/bust
     - **Stand** — always available
     - **Double Down** — available only on first action, if bankroll ≥ current bet
     - **Split** — available only if first two cards are a pair, only on first action
   - Player selects action
   - Hand updates (new card dealt for Hit/Double, hand splits into two for Split)
   - Hand total recalculates, soft/hard indicator updates
   - Repeat until player stands or busts

5. **Dealer play phase**  
   - Dealer's face-down card reveals
   - Dealer hits automatically until reaching hard 17 or any 17+
   - Dealer stands on soft 17
   - No player input required

6. **Resolution phase**  
   - Round Result Overlay displays:
     - Outcome (Win / Loss / Push / Blackjack)
     - Payout amount (blackjack pays 3:2, regular win pays 1:1, push returns bet)
     - Updated bankroll
   - Session stats update in memory and local storage:
     - Hands played +1
     - Win/Loss/Push count increments
     - Win rate recalculates
     - Streak updates
     - Biggest single-hand win updates if applicable

7. **Next round**  
   - Player clicks "Play Again" (or equivalent button)
   - Table resets to betting phase
   - Bankroll reflects updated total
   - Previous hands clear
   - Shoe persists unless reshuffle threshold met

---

## Decision points

### 1. Insurance decision
- **Trigger:** Dealer shows Ace
- **Options:** Accept (bet up to half original bet) or Decline
- **Outcome:** If accepted and dealer has blackjack, insurance pays 2:1; otherwise insurance bet is lost

### 2. Player action selection
- **Trigger:** Player's turn after deal
- **Options:**
  - Hit (take another card)
  - Stand (end turn)
  - Double Down (double bet, take exactly one card, end turn) — first action only
  - Split (create two hands from pair, bet equal to original on second hand) — first action only, pairs only
- **Constraints:**
  - Double/Split require sufficient bankroll
  - Double/Split only available as first action
  - Split aces receive one card each and cannot hit again

### 3. Strategy Hint toggle
- **Trigger:** Player toggles Strategy Hint on
- **Outcome:** System displays recommended action (Hit/Stand/Double/Split) based on basic strategy for current hand vs. dealer up-card
- **Note:** Available during player action phase; does not auto-play

### 4. Bankroll reset
- **Trigger:** Player clicks reset control in Stats Panel
- **Outcome:** Bankroll resets to starting amount (e.g. 1000), all session stats clear
- **Note:** Intent does not specify a confirmation dialog; see Confirmation states section

---

## Alternate paths

### Path A: Player splits a pair
1. Player receives pair (e.g. two 8s)
2. Split button becomes available
3. Player clicks Split
4. Original hand splits into two separate hands
5. Second bet (equal to original) deducts from bankroll
6. Each hand receives one additional card
7. **If split aces:** each hand receives exactly one card, no further action allowed
8. **If split non-aces:** player acts on first hand (Hit/Stand/Double), then second hand
9. Dealer plays once after all player hands complete
10. Each hand resolves independently against dealer

**Constraint from intent:** "up to one split per hand" — no re-splitting.

### Path B: Player doubles down
1. Player acts on initial two-card hand
2. Double button available (if bankroll sufficient)
3. Player clicks Double
4. Bet doubles (deducts from bankroll)
5. Player receives exactly one additional card
6. Player's turn ends automatically
7. Dealer plays
8. Hand resolves with doubled payout/loss

### Path C: Player busts
1. Player hits and hand total exceeds 21
2. Hand marked as bust
3. Player loses bet immediately
4. **If split hand:** other hand(s) continue
5. **If only/last hand:** dealer does **not** play (intent does not explicitly state this, but standard blackjack rules apply; clarification needed if dealer should reveal anyway)
6. Round resolves

**Intent ambiguity:** Does dealer reveal hole card if all player hands bust? Not specified.

### Path D: Dealer has blackjack (with insurance offered)
1. Dealer shows Ace
2. Insurance offered
3. Player accepts or declines
4. Dealer reveals blackjack (10-value hole card)
5. **If player has blackjack:** push (no money changes hands, insurance loses if taken)
6. **If player does not have blackjack:** player loses original bet, insurance pays 2:1 if taken
7. Round ends, no player actions occur

### Path E: Both player and dealer have blackjack
1. Both dealt blackjack on initial deal
2. Result: Push
3. Original bet returned
4. No 3:2 payout

### Path F: Shoe reshuffle
1. After a hand completes, shoe drops below ~25% of cards remaining
2. Shoe automatically reshuffles (all 6 decks)
3. Shoe indicator updates
4. Next hand deals from fresh shoe
5. **Note:** Reshuffle happens between hands, not mid-hand

### Path G: Player bankroll reaches zero
1. Player loses final bet
2. Bankroll = 0
3. **Intent does not specify:** What happens next?
   - Can player reset bankroll immediately?
   - Is there a "game over" state?
   - Is betting panel disabled?

**Unspecified behavior.**

---

## Empty states

### 1. Start of session (first visit)
- **Bankroll:** Default starting amount (e.g. 1000 chips)
- **Stats panel:** All stats at zero (hands played: 0, wins: 0, losses: 0, pushes: 0, win rate: —, streak: 0, biggest win: 0)
- **Table:** No cards, no bet, betting panel active

### 2. Bankroll depleted
**Intent does not specify empty state handling when bankroll = 0.**  
Possible interpretations (not specified):
- Betting panel disabled, prompt to reset bankroll
- Automatic bankroll reset
- Game over message

**Unspecified.**

### 3. No prior session stats (cleared local storage)
- Same as first visit
- Stats panel shows zeros/defaults

---

## Error states

**Intent does not explicitly enumerate error states.** Inferred from constraints:

### 1. Insufficient bankroll for bet
- **Trigger:** Player attempts to confirm bet > current bankroll
- **Behavior (not specified):** Likely one of:
  - Bet confirmation button disabled until bet ≤ bankroll
  - Error message on confirm attempt
  - Bet amount auto-capped to bankroll

**Unspecified.**

### 2. Insufficient bankroll for Double Down
- **Trigger:** Player clicks Double when bankroll < current bet amount
- **Behavior (not specified):** Likely Double button is disabled preemptively

**Unspecified.**

### 3. Insufficient bankroll for Split
- **Trigger:** Player clicks Split when bankroll < current bet amount
- **Behavior (not specified):** Likely Split button is disabled preemptively

**Unspecified.**

### 4. Insufficient bankroll for Insurance
- **Trigger:** Player attempts insurance bet > available bankroll or > half original bet
- **Behavior:** Not specified

**Unspecified.**

### 5. Local storage failure
- **Trigger:** Browser blocks local storage, or storage quota exceeded
- **Behavior:** Not specified; stats/bankroll persistence fails
- **Fallback:** Not specified (session-only stats? error message?)

**Unspecified.**

### 6. Game state corruption
- **Trigger:** Invalid state due to implementation bug (e.g. hand total miscalculation)
- **Behavior:** Not specified

**Unspecified.**

---

## Confirmation states

**Intent does not specify confirmation dialogs.** Inferred likely confirmations:

### 1. Bet confirmation
- **Trigger:** Player finishes selecting chips
- **UI (not specified):** Likely a "Confirm Bet" or "Deal" button
- **Visual feedback:** Button state change, bet locked in

### 2. Insurance acceptance
- **Trigger:** Player chooses to take insurance
- **UI (not specified):** Accept/Decline buttons or similar
- **Feedback:** Insurance bet amount displays, deducts from bankroll

### 3. Bankroll/stats reset
- **Intent does not specify whether reset requires confirmation.**  
Recommended (but unspecified): Confirmation dialog to prevent accidental reset.

**Unspecified whether confirmation is required.**

---

## Success states

### 1. Round win
- **Round Result Overlay displays:**
  - "You Win!" or similar message
  - Payout amount (original bet × 1)
  - Updated bankroll
  - "Play Again" button
- **Stats update:**
  - Wins +1
  - Hands played +1
  - Win rate recalculates
  - Positive streak increments (or resets if prior round was not a win)
  - Biggest win updates if this payout > previous record

### 2. Blackjack win
- **Round Result Overlay displays:**
  - "Blackjack!" or similar message
  - Payout amount (original bet × 1.5, i.e. 3:2)
  - Updated bankroll
  - "Play Again" button
- **Stats update:** Same as regular win, with higher payout

### 3. Push
- **Round Result Overlay displays:**
  - "Push" or "Tie" message
  - Original bet returned (no profit/loss)
  - Bankroll unchanged
  - "Play Again" button
- **Stats update:**
  - Pushes +1
  - Hands played +1
  - Streak resets (not specified whether push breaks streak; assumed yes)

### 4. Insurance win (dealer has blackjack, player took insurance)
- **Insurance bet pays 2:1**
- **If player also has blackjack:** push on main bet + insurance win = net profit from insurance
- **If player does not have blackjack:** main bet lost, insurance win offsets half the loss
- **Display (not specified):** Likely separate or combined message showing insurance payout

### 5. Successful split hand resolution
- **Each split hand resolves independently**
- **Round Result Overlay (not specified):** May show combined result or per-hand result
- **Stats (not specified):** Likely counts as one hand played, with outcome based on net result across both hands

**Unspecified how split hands affect stats (one hand or two?).**

### 6. Successful Double Down win
- **Payout:** (original bet × 2) × 1 = 2× profit on win
- **Display:** Round Result Overlay shows doubled payout
- **Stats:** Same as regular win

### 7. Bankroll/stats reset success
- **Trigger:** Player confirms reset (if confirmation exists)
- **Outcome:**
  - Bankroll resets to starting amount
  - All stats reset to zero
  - Local storage updates
- **Visual feedback (not specified):** Likely stats panel updates immediately, possible toast/message

---

## Required screens

**Based on intent "Screens" section:**

### 1. Table / Play Screen
**Primary screen; always visible.**

**Must display:**
- Dealer hand area (cards, total)
- Player hand area(s) (cards, total, soft/hard indicator)
- Shoe indicator (cards remaining or reshuffle threshold)
- Bankroll (current chip total)
- Bet controls (chip selection, current bet display)
- Action buttons:
  - Hit
  - Stand
  - Double Down (conditional)
  - Split (conditional)
  - Insurance (conditional, appears only when dealer shows Ace)
- Strategy Hint toggle
- Access to Stats Panel (button/icon/tab)

**States of this screen:**
- **Betting phase:** Bet controls active, action buttons hidden/disabled
- **Play phase:** Bet controls disabled, action buttons visible/active based on game state
- **Dealer play phase:** All player controls disabled, dealer hand animates
- **Resolution phase:** Overlaid by Round Result, or inline result display (not specified)

### 2. Betting Screen/Panel
**Intent lists this as a separate screen, but also describes it as part of Table / Play Screen.**

**Interpretation:** Likely a panel/section within the Table / Play Screen, active during betting phase.

**Must display:**
- Chip selection controls (denominations not specified)
- Current bet amount
- Confirm button (label not specified: "Confirm Bet," "Deal," etc.)

**State transitions:**
- Active when round begins or after "Play Again"
- Disabled/hidden once bet confirmed and cards dealt

### 3. Round Result Overlay
**Appears after round resolves.**

**Must display:**
- Outcome message (Win / Loss / Push / Blackjack / Bust)
- Payout amount (or loss amount, or "Bet Returned" for push)
- Updated bankroll
- "Play Again" button (or equivalent to start next round)

**Behavior (not specified):**
- Modal overlay, or inline message?
- Dismissible by clicking outside, or only via "Play Again"?

**Unspecified.**

### 4. Stats Panel
**Accessible from Table / Play Screen.**

**Must display:**
- Hands played (total count)
- Win rate (percentage; formula not specified: wins / hands, or wins / (wins + losses)?)
- Current streak (type not specified: win streak? win/loss streak? pushed hands break streak?)
- Biggest single-hand win (chip amount)
- Win count
- Loss count
- Push count
- Reset-bankroll control (button)

**Behavior (not specified):**
- Always visible sidebar?
- Collapsible panel?
- Modal opened by button?

**Unspecified.**

---

## Screen transitions

### 1. Load → Table / Play Screen (Betting Phase)
- **Trigger:** User navigates to game URL
- **Transition:** Immediate load (no splash screen specified)
- **State:** Betting panel active, bankroll and stats loaded from local storage (or defaults)

### 2. Betting Phase → Deal Phase
- **Trigger:** Player confirms bet
- **Transition (not specified):** Likely brief animation as cards deal
- **State:** Bet controls disable, cards appear, action buttons enable

### 3. Deal Phase → Insurance Prompt (conditional)
- **Trigger:** Dealer up-card is Ace
- **Transition:** Insurance prompt appears (modal? inline?)
- **State:** Player actions paused until insurance decision made

### 4. Deal Phase / Insurance → Player Action Phase
- **Trigger:** Insurance resolved or skipped
- **Transition:** Action buttons activate
- **State:** Player can select Hit/Stand/Double/Split

### 5. Player Action Phase → Dealer Play Phase
- **Trigger:** Player stands, busts, or completes all split hands
- **Transition (not specified):** Likely brief