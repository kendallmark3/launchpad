import { evaluateHand, isPair } from "../engine/hand.js";
import { getStrategyHint } from "../engine/strategy.js";

export function ActionControls({ hand, dealerUpCard, bankroll, playerHandCount, hintEnabled, actions }) {
  const { isBust } = evaluateHand(hand.cards);
  if (hand.done || isBust) return null;

  const canDouble = hand.cards.length === 2 && hand.bet <= bankroll;
  const canSplit = isPair(hand.cards) && hand.bet <= bankroll && playerHandCount === 1;

  const hint = hintEnabled
    ? getStrategyHint({ cards: hand.cards, dealerUpRank: dealerUpCard.rank, canDouble, canSplit })
    : null;

  return (
    <div className="action-controls">
      {hint && <div className="strategy-hint">Suggested: {hint}</div>}
      <div className="action-buttons">
        <button type="button" onClick={actions.hit}>
          Hit
        </button>
        <button type="button" onClick={actions.stand}>
          Stand
        </button>
        <button type="button" onClick={actions.double} disabled={!canDouble}>
          Double
        </button>
        <button type="button" onClick={actions.split} disabled={!canSplit}>
          Split
        </button>
      </div>
    </div>
  );
}
