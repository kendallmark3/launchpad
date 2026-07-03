import { useBlackjackGame } from "./hooks/useBlackjackGame.js";
import { Hand } from "./components/Hand.jsx";
import { BettingPanel } from "./components/BettingPanel.jsx";
import { InsurancePanel } from "./components/InsurancePanel.jsx";
import { ActionControls } from "./components/ActionControls.jsx";
import { StatsPanel } from "./components/StatsPanel.jsx";
import { ResultOverlay } from "./components/ResultOverlay.jsx";
import "./App.css";

function App() {
  const game = useBlackjackGame();
  const {
    phase,
    bankroll,
    stats,
    hintEnabled,
    setHintEnabled,
    bet,
    dealerCards,
    dealerRevealed,
    playerHands,
    activeHandIndex,
    roundResult,
    actions,
  } = game;

  const hideDealerHole = phase !== "betting" && !dealerRevealed && dealerCards.length > 0;

  return (
    <div className="table-felt">
      <header className="table-header">
        <h1>Blackjack</h1>
        <span className="entertainment-note">For entertainment only &mdash; no real money involved.</span>
      </header>

      <section className="dealer-area">
        {dealerCards.length > 0 && <Hand cards={dealerCards} hideSecondCard={hideDealerHole} label="Dealer" />}
      </section>

      <section className="player-area">
        {playerHands.map((hand, i) => (
          <Hand
            key={i}
            cards={hand.cards}
            bet={hand.bet}
            label={playerHands.length > 1 ? `Hand ${i + 1}` : "You"}
            active={phase === "player-turn" && i === activeHandIndex}
          />
        ))}
      </section>

      {phase === "player-turn" && (
        <ActionControls
          hand={playerHands[activeHandIndex]}
          dealerUpCard={dealerCards[0]}
          bankroll={bankroll}
          playerHandCount={playerHands.length}
          hintEnabled={hintEnabled}
          actions={actions}
        />
      )}

      {phase === "insurance" && (
        <InsurancePanel bet={bet} bankroll={bankroll} onTakeInsurance={actions.takeInsurance} onDecline={actions.declineInsurance} />
      )}

      {phase === "betting" && (
        <BettingPanel bankroll={bankroll} bet={bet} onAddChip={actions.addToBet} onClearBet={actions.clearBet} onDeal={actions.deal} />
      )}

      {phase === "result" && <ResultOverlay roundResult={roundResult} onPlayAgain={actions.playAgain} />}

      <StatsPanel stats={stats} hintEnabled={hintEnabled} onToggleHint={setHintEnabled} onReset={actions.resetBankroll} />
    </div>
  );
}

export default App;
