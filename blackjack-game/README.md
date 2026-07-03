# Blackjack

A client-only, browser-playable blackjack game — built from
[`intents/blackjack-game.intent.md`](../intents/blackjack-game.intent.md) at the repo root.
This is a standalone Vite + React app; it has no relationship to `feature_launchpad`'s Python
stdlib-only constraints, which apply to the launchpad tool itself, not to features it specs out.

## Rules implemented

- 6-deck shoe, reshuffled automatically once it drops below ~25% of its cards.
- Hit, Stand, Double Down (first action only), Split (one split per hand; split aces get exactly
  one card each and can't be hit again).
- Insurance (up to half the bet) when the dealer shows an Ace; pays 2:1.
- Dealer stands on all 17s (including soft 17). Blackjack pays 3:2.
- Starting bankroll of 1000 chips; bankroll and session stats (hands played, win rate, streak,
  biggest win) persist in `localStorage` across reloads, with a reset control.
- Optional "Strategy hint" toggle, backed by a standard basic-strategy table
  (`src/engine/strategy.js`), recommending Hit/Stand/Double/Split for the current hand.

This is for entertainment only — no real money, accounts, or backend of any kind.

## Run it

```bash
npm install
npm run dev
```

Then open the printed `http://localhost:.../` URL.

## Test

```bash
npm test
```

41 tests (Vitest + React Testing Library) cover hand evaluation (including multi-ace and bust
cases), dealer play-out, payout resolution (win/loss/push/blackjack/insurance), the basic-strategy
table, and a betting/dealing smoke test through the UI.

## Build

```bash
npm run build
```
