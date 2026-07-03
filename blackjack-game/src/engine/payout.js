export const OUTCOMES = {
  BLACKJACK: "blackjack",
  WIN: "win",
  LOSS: "loss",
  PUSH: "push",
};

/**
 * Resolves a single player hand against the dealer's final hand.
 * `playerIsNatural`/`dealerIsNatural` should only be true for an original,
 * un-split two-card 21 — callers must not pass isBlackjack from a split hand.
 */
export function resolveHand({ playerTotal, playerBust, playerIsNatural, dealerTotal, dealerBust, dealerIsNatural, bet }) {
  if (playerBust) {
    return { outcome: OUTCOMES.LOSS, payout: -bet };
  }
  if (playerIsNatural && dealerIsNatural) {
    return { outcome: OUTCOMES.PUSH, payout: 0 };
  }
  if (playerIsNatural) {
    return { outcome: OUTCOMES.BLACKJACK, payout: bet * 1.5 };
  }
  if (dealerIsNatural) {
    return { outcome: OUTCOMES.LOSS, payout: -bet };
  }
  if (dealerBust) {
    return { outcome: OUTCOMES.WIN, payout: bet };
  }
  if (playerTotal > dealerTotal) {
    return { outcome: OUTCOMES.WIN, payout: bet };
  }
  if (playerTotal < dealerTotal) {
    return { outcome: OUTCOMES.LOSS, payout: -bet };
  }
  return { outcome: OUTCOMES.PUSH, payout: 0 };
}

export function resolveInsurance({ insuranceBet, dealerIsNatural }) {
  if (!insuranceBet) return 0;
  return dealerIsNatural ? insuranceBet * 2 : -insuranceBet;
}
