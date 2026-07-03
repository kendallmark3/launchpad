import { evaluateHand } from "./hand.js";

const DEALER_STAND_TOTAL = 17;

export function dealerShouldHit(cards) {
  const { total } = evaluateHand(cards);
  return total < DEALER_STAND_TOTAL;
}

export function playDealerHand(startingCards, drawCard) {
  let cards = startingCards.slice();
  while (dealerShouldHit(cards)) {
    cards = [...cards, drawCard()];
  }
  return cards;
}
