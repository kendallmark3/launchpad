# Feature Intent

## Business Goal

Give users an engaging, casino-style blackjack game they can play in the browser for free, with
enough depth (betting, splits, doubling, insurance, and strategy assistance) to be genuinely
replayable rather than a bare-bones "deal cards, hit or stand" demo.

## User Personas

- **Casual Player** — wants a quick, fun round of blackjack with realistic rules and a sense of
  progression (bankroll going up or down over a session).
- **Learning Player** — wants to practice basic strategy and understand whether their plays were
  statistically correct, without real-money risk.

## User Journey

1. Player lands on the table with a starting bankroll and an empty betting circle.
2. Player selects a bet amount using chip controls and confirms.
3. Player and dealer are each dealt two cards (one dealer card face down); the shoe is a
   multi-deck shuffle that only reshuffles when it runs low, not every hand.
4. If the dealer's up-card is an Ace, the player is offered insurance before play continues.
5. Player acts on their hand: Hit, Stand, Double Down (first action only), or Split (if the first
   two cards are a pair) — with a running total and soft/hard hand indicator shown.
6. If the player wants help, they can toggle "Strategy Hint" to see the statistically recommended
   action for their current hand against the dealer's up-card.
7. Once the player stands, busts, or finishes all split hands, the dealer reveals their hidden
   card and plays according to fixed dealer rules (hit until 17, including stand on soft 17).
8. Round resolves: win, loss, push, or blackjack (paid 3:2), and the bankroll updates.
9. Session stats update (hands played, win/loss/push counts, win rate, current streak, biggest
   single-hand win) and persist across page reloads.
10. Player starts another round, or resets their bankroll/stats from a settings control if they
    want a clean slate.

## Required Screens

- Table / Play Screen (dealer hand, player hand(s), shoe indicator, bankroll, bet controls, action
  buttons, strategy hint toggle)
- Betting Screen/Panel (chip selection, current bet, confirm)
- Round Result Overlay (win/loss/push/blackjack outcome, payout, "Play Again")
- Stats Panel (hands played, win rate, streak, biggest win, reset-bankroll control)

## Functional Requirements

- Standard 52-card deck logic across a 6-deck shoe, cryptographically-fine (not casino-grade)
  shuffle; reshuffle automatically once the shoe drops below ~25% of its cards.
- Deal, hit, stand, double down (first action only, one additional card, bet doubled), and split
  pairs (up to one split per hand; split aces receive exactly one card each and cannot re-hit).
- Insurance side bet (up to half the original bet) offered only when the dealer's up-card is an
  Ace; pays 2:1 if the dealer has blackjack.
- Dealer plays a fixed strategy with no player input: hit until hard 17 or any 17+, stand on soft
  17.
- Blackjack (ace + ten-value card on the first two cards) pays 3:2 unless the dealer also has
  blackjack (push).
- Bankroll starts at a fixed amount (e.g. 1000 chips) and updates after every round; player cannot
  bet more than their current bankroll.
- "Strategy Hint" toggle shows the basic-strategy-table-recommended action (Hit / Stand / Double /
  Split) for the player's current hand vs. the dealer's up-card.
- Session stats (hands played, wins, losses, pushes, current streak, biggest win) persist in the
  browser (e.g. local storage) across reloads; a "reset" control clears bankroll and stats back to
  defaults.
- Clear visual/textual feedback for hand totals, including distinguishing "soft" totals (hand
  containing an ace counted as 11).

## Non-Functional Requirements

- Runs entirely client-side; no backend, no account system, no real-money handling of any kind.
- Playable on both desktop and mobile-width viewports.
- Card deal/flip actions should feel responsive (short, non-blocking animations, not artificial
  delays that make the game feel sluggish).
- No externally loaded fonts, images, or scripts — self-contained bundle.

## Design Constraints

- Must not involve real money, payment processing, or any account/login system — this is a free,
  local-only game.
- Should look and feel like a casino table (felt-green background, card suits/ranks legible at a
  glance) without requiring any licensed/proprietary card art — simple drawn/CSS-based cards are
  fine.
- Must clearly label this as being for entertainment only if any betting language could be
  mistaken for real-money gambling.

## API / Data Requirements

- No external API calls or backend of any kind.
- All game state (shoe, hands, bankroll) lives in client-side memory for the duration of a round.
- Bankroll and session stats persist via browser local storage only; no server-side data storage.

## Acceptance Criteria

- A player can complete a full round end-to-end: bet, get dealt cards, act on their hand (hit,
  stand, double, split, insurance where applicable), see the dealer play out, and see the correct
  payout applied to their bankroll.
- Hand values (including soft totals and bust detection) are calculated correctly in all cases,
  including after splits.
- The dealer always follows fixed rules (hit until 17+, stand on soft 17) with no manual
  intervention.
- Strategy Hint, when enabled, recommends an action consistent with standard basic strategy for
  the player's hand and the dealer's up-card.
- Stats and bankroll survive a page reload and can be reset on demand.
- A player cannot bet more chips than they currently have.

## Validation Expectations

- Unit tests for hand-value calculation (hard/soft totals, bust detection, blackjack detection)
  covering multi-ace hands.
- Unit tests for the dealer's fixed play-out logic (hits until 17+, stands on soft 17).
- Unit tests for payout resolution across win / loss / push / blackjack / insurance-paid /
  insurance-lost outcomes.
- Unit tests for split handling, including split aces receiving exactly one card.
- Manual smoke test playing at least one full round through the UI in a browser.

## Out of Scope

- Multiplayer or any form of matching with other real players.
- Real-money betting, deposits, withdrawals, or payment integration of any kind.
- Card counting detection/prevention (the Strategy Hint feature is intentionally counting-blind —
  basic strategy only, not count-adjusted deviations).
- Server-side persistence, accounts, or leaderboards.
