import { describe, expect, it, beforeEach } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import App from "./App.jsx";

describe("App", () => {
  beforeEach(() => {
    window.localStorage.clear();
  });

  it("lets a player place a bet and deal a round", () => {
    render(<App />);

    expect(screen.getByText(/Bankroll: 1000/)).toBeInTheDocument();

    fireEvent.click(screen.getByRole("button", { name: "25" }));
    expect(screen.getByText(/Bet:/).textContent).toContain("25");

    fireEvent.click(screen.getByRole("button", { name: "Deal" }));

    expect(screen.getByText("Dealer")).toBeInTheDocument();
    expect(screen.getByText("You")).toBeInTheDocument();
  });

  it("clear resets the bet to zero", () => {
    render(<App />);

    fireEvent.click(screen.getByRole("button", { name: "100" }));
    fireEvent.click(screen.getByRole("button", { name: "Clear" }));

    expect(screen.getByText(/Bet:/).textContent).toContain("0");
  });

  it("disables chips that would exceed the bankroll", () => {
    render(<App />);

    for (let i = 0; i < 2; i++) fireEvent.click(screen.getByRole("button", { name: "500" }));

    expect(screen.getByRole("button", { name: "500" })).toBeDisabled();
  });
});
