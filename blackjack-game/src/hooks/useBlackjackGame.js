import { useRef, useState } from "react";
import { createShoe, needsReshuffle } from "../engine/cards.js";
import { evaluateHand, isPair } from "../engine/hand.js";
import { playDealerHand } from "../engine/dealer.js";
import { resolveHand, resolveInsurance } from "../engine/payout.js";
import { usePersistentState } from "./usePersistentState.js";

const NUM_DECKS = 6;
const STARTING_BANKROLL = 1000;
const DEFAULT_STATS = {
  handsPlayed: 0,
  wins: 0,
  losses: 0,
  pushes: 0,
  blackjacks: 0,
  currentStreak: 0,
  biggestWin: 0,
};

function makeHand(cards) {
  return { cards, bet: 0, done: false, isSplitAces: false, isNatural: false };
}

export function useBlackjackGame() {
  const shoeRef = useRef(createShoe(NUM_DECKS));
  const [bankroll, setBankroll] = usePersistentState("blackjack.bankroll", STARTING_BANKROLL);
  const [stats, setStats] = usePersistentState("blackjack.stats", DEFAULT_STATS);
  const [hintEnabled, setHintEnabled] = usePersistentState("blackjack.hintEnabled", false);

  const [phase, setPhase] = useState("betting");
  const [bet, setBet] = useState(0);
  const [insuranceBet, setInsuranceBet] = useState(0);
  const [dealerCards, setDealerCards] = useState([]);
  const [dealerRevealed, setDealerRevealed] = useState(false);
  const [playerHands, setPlayerHands] = useState([]);
  const [activeHandIndex, setActiveHandIndex] = useState(0);
  const [roundResult, setRoundResult] = useState(null);

  function drawCard() {
    if (shoeRef.current.length === 0) {
      shoeRef.current = createShoe(NUM_DECKS);
    }
    return shoeRef.current.pop();
  }

  function addToBet(amount) {
    setBet((current) => Math.min(current + amount, bankroll));
  }

  function clearBet() {
    setBet(0);
  }

  function deal() {
    if (bet <= 0 || bet > bankroll) return;
    if (needsReshuffle(shoeRef.current, NUM_DECKS)) {
      shoeRef.current = createShoe(NUM_DECKS);
    }

    setBankroll((current) => current - bet);
    const playerCards = [drawCard(), drawCard()];
    const dealer = [drawCard(), drawCard()];
    const hand = makeHand(playerCards);
    hand.bet = bet;
    hand.isNatural = evaluateHand(playerCards).isBlackjack;

    setDealerCards(dealer);
    setDealerRevealed(false);
    setPlayerHands([hand]);
    setActiveHandIndex(0);
    setInsuranceBet(0);
    setRoundResult(null);

    const dealerUpRank = dealer[0].rank;
    if (dealerUpRank === "A") {
      setPhase("insurance");
    } else if (evaluateHand(dealer).isBlackjack || hand.isNatural) {
      resolveRound([hand], dealer, 0);
    } else {
      setPhase("player-turn");
    }
  }

  function takeInsurance(amount) {
    const dealerIsNatural = evaluateHand(dealerCards).isBlackjack;
    setInsuranceBet(amount);
    setBankroll((current) => current - amount);
    settleInsuranceAndContinue(amount, dealerIsNatural);
  }

  function declineInsurance() {
    const dealerIsNatural = evaluateHand(dealerCards).isBlackjack;
    settleInsuranceAndContinue(0, dealerIsNatural);
  }

  function settleInsuranceAndContinue(amount, dealerIsNatural) {
    if (dealerIsNatural || playerHands[0]?.isNatural) {
      resolveRound(playerHands, dealerCards, amount);
    } else {
      setPhase("player-turn");
    }
  }

  function updateActiveHand(updater) {
    setPlayerHands((hands) => hands.map((h, i) => (i === activeHandIndex ? updater(h) : h)));
  }

  function advanceOrResolve(nextHands) {
    const nextIndex = nextHands.findIndex((h, i) => i > activeHandIndex && !h.done);
    if (nextIndex !== -1) {
      setActiveHandIndex(nextIndex);
      return;
    }
    if (nextHands.every((h) => h.done)) {
      resolveRound(nextHands, dealerCards, insuranceBet);
    }
  }

  function hit() {
    if (phase !== "player-turn") return;
    const card = drawCard();
    const next = playerHands.map((h, i) => {
      if (i !== activeHandIndex) return h;
      const cards = [...h.cards, card];
      const { isBust, total } = evaluateHand(cards);
      return { ...h, cards, done: isBust || total === 21 };
    });
    setPlayerHands(next);
    advanceOrResolve(next);
  }

  function stand() {
    if (phase !== "player-turn") return;
    const next = playerHands.map((h, i) => (i === activeHandIndex ? { ...h, done: true } : h));
    setPlayerHands(next);
    advanceOrResolve(next);
  }

  function double() {
    if (phase !== "player-turn") return;
    const hand = playerHands[activeHandIndex];
    if (hand.cards.length !== 2 || hand.bet > bankroll) return;
    setBankroll((current) => current - hand.bet);
    const card = drawCard();
    const next = playerHands.map((h, i) =>
      i === activeHandIndex ? { ...h, cards: [...h.cards, card], bet: h.bet * 2, done: true } : h
    );
    setPlayerHands(next);
    advanceOrResolve(next);
  }

  function split() {
    if (phase !== "player-turn") return;
    const hand = playerHands[activeHandIndex];
    if (!isPair(hand.cards) || hand.bet > bankroll || playerHands.length > 1) return;

    setBankroll((current) => current - hand.bet);
    const isAces = hand.cards[0].rank === "A";
    const firstCard = drawCard();
    const secondCard = drawCard();
    const handA = { cards: [hand.cards[0], firstCard], bet: hand.bet, done: isAces, isSplitAces: isAces, isNatural: false };
    const handB = { cards: [hand.cards[1], secondCard], bet: hand.bet, done: isAces, isSplitAces: isAces, isNatural: false };

    setPlayerHands([handA, handB]);
    setActiveHandIndex(0);

    if (isAces) {
      resolveRound([handA, handB], dealerCards, insuranceBet);
    }
  }

  function resolveRound(hands, dealer, insurance) {
    setPhase("dealer-turn");
    setDealerRevealed(true);

    const finalDealerCards = playDealerHand(dealer, drawCard);
    setDealerCards(finalDealerCards);

    const dealerEval = evaluateHand(finalDealerCards);
    const dealerIsNatural = dealer.length === 2 && evaluateHand(dealer).isBlackjack;

    const handResults = hands.map((hand) => {
      const playerEval = evaluateHand(hand.cards);
      const result = resolveHand({
        playerTotal: playerEval.total,
        playerBust: playerEval.isBust,
        playerIsNatural: hand.isNatural && !hand.isSplitAces,
        dealerTotal: dealerEval.total,
        dealerBust: dealerEval.isBust,
        dealerIsNatural,
        bet: hand.bet,
      });
      return { ...result, hand };
    });

    const insurancePayout = resolveInsurance({ insuranceBet: insurance, dealerIsNatural });
    const totalPayout = handResults.reduce((sum, r) => sum + r.payout, 0) + insurancePayout;

    setBankroll((current) => current + hands.reduce((s, h) => s + h.bet, 0) + insurance + totalPayout);

    setStats((current) => {
      let { handsPlayed, wins, losses, pushes, blackjacks, currentStreak, biggestWin } = current;
      for (const r of handResults) {
        handsPlayed += 1;
        if (r.outcome === "win") {
          wins += 1;
          currentStreak += 1;
        } else if (r.outcome === "blackjack") {
          wins += 1;
          blackjacks += 1;
          currentStreak += 1;
        } else if (r.outcome === "loss") {
          losses += 1;
          currentStreak = 0;
        } else {
          pushes += 1;
        }
      }
      biggestWin = Math.max(biggestWin, totalPayout);
      return { handsPlayed, wins, losses, pushes, blackjacks, currentStreak, biggestWin };
    });

    setPlayerHands(hands);
    setRoundResult({ handResults, insurancePayout, dealerCards: finalDealerCards });
    setPhase("result");
  }

  function playAgain() {
    setPhase("betting");
    setBet(0);
    setInsuranceBet(0);
    setPlayerHands([]);
    setDealerCards([]);
    setDealerRevealed(false);
    setRoundResult(null);
  }

  function resetBankroll() {
    setBankroll(STARTING_BANKROLL);
    setStats(DEFAULT_STATS);
  }

  return {
    phase,
    bankroll,
    stats,
    hintEnabled,
    setHintEnabled,
    bet,
    insuranceBet,
    dealerCards,
    dealerRevealed,
    playerHands,
    activeHandIndex,
    roundResult,
    actions: {
      addToBet,
      clearBet,
      deal,
      takeInsurance,
      declineInsurance,
      hit,
      stand,
      double,
      split,
      playAgain,
      resetBankroll,
    },
  };
}
