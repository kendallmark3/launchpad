import { cardValue } from "./cards.js";
import { evaluateHand } from "./hand.js";

export const ACTIONS = { HIT: "Hit", STAND: "Stand", DOUBLE: "Double", SPLIT: "Split" };

// Dealer up-card columns, in order, for every table below: 2 3 4 5 6 7 8 9 10 A
const DEALER_COLUMNS = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11];

const H = ACTIONS.HIT;
const S = ACTIONS.STAND;
const D = ACTIONS.DOUBLE;
const P = ACTIONS.SPLIT;

// Hard totals 8-16 (5-7 are always Hit, 17-21 are always Stand, so only the
// decision range needs a table).
const HARD_STRATEGY = {
  8: [H, H, H, H, H, H, H, H, H, H],
  9: [H, D, D, D, D, H, H, H, H, H],
  10: [D, D, D, D, D, D, D, D, H, H],
  11: [D, D, D, D, D, D, D, D, D, H],
  12: [H, H, S, S, S, H, H, H, H, H],
  13: [S, S, S, S, S, H, H, H, H, H],
  14: [S, S, S, S, S, H, H, H, H, H],
  15: [S, S, S, S, S, H, H, H, H, H],
  16: [S, S, S, S, S, H, H, H, H, H],
};

// Soft totals 13-19 (soft 20/21 always Stand). Keyed by the non-ace card's
// value (soft 13 = A,2 ... soft 19 = A,8).
const SOFT_STRATEGY = {
  13: [H, H, H, D, D, H, H, H, H, H],
  14: [H, H, H, D, D, H, H, H, H, H],
  15: [H, H, D, D, D, H, H, H, H, H],
  16: [H, H, D, D, D, H, H, H, H, H],
  17: [H, D, D, D, D, H, H, H, H, H],
  18: [S, D, D, D, D, S, S, H, H, H],
  19: [S, S, S, S, D, S, S, S, S, S],
};

// Pair value 2-10 (10 covers any ten-value pair), 11 = Ace pair.
const PAIR_STRATEGY = {
  2: [P, P, P, P, P, P, H, H, H, H],
  3: [P, P, P, P, P, P, H, H, H, H],
  4: [H, H, H, P, P, H, H, H, H, H],
  5: [D, D, D, D, D, D, D, D, H, H],
  6: [P, P, P, P, P, H, H, H, H, H],
  7: [P, P, P, P, P, P, H, H, H, H],
  8: [P, P, P, P, P, P, P, P, P, P],
  9: [P, P, P, P, P, S, P, P, S, S],
  10: [S, S, S, S, S, S, S, S, S, S],
  11: [P, P, P, P, P, P, P, P, P, P],
};

function lookup(table, key, dealerUpValue) {
  const row = table[key];
  if (!row) return null;
  const index = DEALER_COLUMNS.indexOf(dealerUpValue);
  return index === -1 ? null : row[index];
}

/**
 * Returns the basic-strategy-recommended action for the player's current
 * hand against the dealer's up card. Falls back to Hit/Stand when the table
 * recommends Double/Split but the game state doesn't currently allow it.
 */
export function getStrategyHint({ cards, dealerUpRank, canDouble, canSplit }) {
  const dealerUpValue = cardValue(dealerUpRank);
  const { total, soft } = evaluateHand(cards);

  if (canSplit && cards.length === 2 && cardValue(cards[0].rank) === cardValue(cards[1].rank)) {
    const pairValue = cardValue(cards[0].rank);
    const action = lookup(PAIR_STRATEGY, pairValue, dealerUpValue);
    if (action === P) return P;
    if (action && action !== H) {
      return resolveFallback(action, canDouble);
    }
  }

  if (soft && total >= 13 && total <= 19) {
    const action = lookup(SOFT_STRATEGY, total, dealerUpValue) ?? S;
    return resolveFallback(action, canDouble);
  }

  if (total >= 17) return S;
  if (total <= 7) return H;

  const action = lookup(HARD_STRATEGY, total, dealerUpValue) ?? H;
  return resolveFallback(action, canDouble);
}

function resolveFallback(action, canDouble) {
  if (action === D && !canDouble) return H;
  return action;
}
