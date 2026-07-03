import { describe, expect, it } from "vitest";
import { ACTIONS, getStrategyHint } from "./strategy.js";

const card = (rank, suit = "♠") => ({ rank, suit, id: `${rank}${suit}` });

describe("getStrategyHint", () => {
  it("always splits a pair of aces", () => {
    const action = getStrategyHint({
      cards: [card("A"), card("A")],
      dealerUpRank: "6",
      canDouble: true,
      canSplit: true,
    });
    expect(action).toBe(ACTIONS.SPLIT);
  });

  it("always splits a pair of 8s, even against a strong dealer up card", () => {
    const action = getStrategyHint({
      cards: [card("8"), card("8")],
      dealerUpRank: "10",
      canDouble: true,
      canSplit: true,
    });
    expect(action).toBe(ACTIONS.SPLIT);
  });

  it("never splits a pair of 10-value cards", () => {
    const action = getStrategyHint({
      cards: [card("K"), card("Q")],
      dealerUpRank: "6",
      canDouble: true,
      canSplit: true,
    });
    expect(action).toBe(ACTIONS.STAND);
  });

  it("doubles hard 11 against a weak dealer up card", () => {
    const action = getStrategyHint({
      cards: [card("6"), card("5")],
      dealerUpRank: "6",
      canDouble: true,
      canSplit: false,
    });
    expect(action).toBe(ACTIONS.DOUBLE);
  });

  it("falls back to Hit when double is recommended but unavailable", () => {
    const action = getStrategyHint({
      cards: [card("6"), card("5")],
      dealerUpRank: "6",
      canDouble: false,
      canSplit: false,
    });
    expect(action).toBe(ACTIONS.HIT);
  });

  it("hits a hard 16 against a dealer 10", () => {
    const action = getStrategyHint({
      cards: [card("10"), card("6")],
      dealerUpRank: "10",
      canDouble: true,
      canSplit: false,
    });
    expect(action).toBe(ACTIONS.HIT);
  });

  it("stands on a hard 16 against a dealer 6", () => {
    const action = getStrategyHint({
      cards: [card("10"), card("6")],
      dealerUpRank: "6",
      canDouble: true,
      canSplit: false,
    });
    expect(action).toBe(ACTIONS.STAND);
  });

  it("always stands on hard 17 or higher", () => {
    const action = getStrategyHint({
      cards: [card("10"), card("7")],
      dealerUpRank: "A",
      canDouble: true,
      canSplit: false,
    });
    expect(action).toBe(ACTIONS.STAND);
  });

  it("hits soft 18 against a dealer 9", () => {
    const action = getStrategyHint({
      cards: [card("A"), card("7")],
      dealerUpRank: "9",
      canDouble: true,
      canSplit: false,
    });
    expect(action).toBe(ACTIONS.HIT);
  });

  it("stands on soft 18 against a dealer 8", () => {
    const action = getStrategyHint({
      cards: [card("A"), card("7")],
      dealerUpRank: "8",
      canDouble: true,
      canSplit: false,
    });
    expect(action).toBe(ACTIONS.STAND);
  });

  it("always stands on soft 20", () => {
    const action = getStrategyHint({
      cards: [card("A"), card("9")],
      dealerUpRank: "6",
      canDouble: true,
      canSplit: false,
    });
    expect(action).toBe(ACTIONS.STAND);
  });
});
