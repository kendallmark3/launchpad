import { cardValue } from "./cards.js";

export function evaluateHand(cards) {
  let total = cards.reduce((sum, card) => sum + cardValue(card.rank), 0);
  let softAces = cards.filter((card) => card.rank === "A").length;

  while (total > 21 && softAces > 0) {
    total -= 10;
    softAces -= 1;
  }

  const soft = softAces > 0;
  const isBust = total > 21;
  const isBlackjack = cards.length === 2 && total === 21;

  return { total, soft, isBust, isBlackjack };
}

export function isPair(cards) {
  return cards.length === 2 && cardValue(cards[0].rank) === cardValue(cards[1].rank);
}
