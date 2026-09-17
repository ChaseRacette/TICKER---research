"""Lab 08: Microsoft P/E peer comparison using frozen sourced inputs.

Run from the repository root:
    python models\msft_pe_comps.py
"""

from statistics import median


# =============================================================================
# EDITABLE INPUTS — September 1, 2026 closing prices; USD per share.
# EPS is the latest annual GAAP diluted EPS public on that comparison date.
# =============================================================================
target = {
    "ticker": "MSFT",
    "name": "Microsoft Corporation",
    "price": 501.02,
    "diluted_eps": 17.95,  # FY ended June 30, 2026; released July 29, 2026
}

peers = [
    {
        "ticker": "ORCL",
        "name": "Oracle Corporation",
        "price": 141.32,
        "diluted_eps": 5.83,  # FY ended May 31, 2026; released June 10, 2026
    },
    {
        "ticker": "GOOGL",
        "name": "Alphabet Inc. Class A",
        "price": 335.02,
        "diluted_eps": 10.81,  # FY ended December 31, 2025; filed February 2026
    },
]
# =============================================================================


def positive_number(value):
    """Return True only for numeric values greater than zero."""
    return isinstance(value, (int, float)) and value > 0


def implied_price(peer_pe):
    """Return the target implied price, or None when target EPS is unusable."""
    return peer_pe * target["diluted_eps"] if positive_number(target["diluted_eps"]) else None


def display_price(label, price):
    if price is None:
        print(f"{label}: not meaningful")
    else:
        print(f"{label}: ${price:,.2f}")


target_ticker = target["ticker"].upper()
seen = set()
eligible_peers = []
for peer in peers:
    ticker = peer["ticker"].upper()
    if ticker == target_ticker:
        print(f"Excluded target from peer set: {peer['ticker']}")
    elif ticker in seen:
        print(f"Excluded duplicate peer: {peer['ticker']}")
    else:
        seen.add(ticker)
        eligible_peers.append(peer)

print("Microsoft P/E comparable-company analysis")
print(f"Comparison date: September 1, 2026")
print(f"Target: {target['name']} ({target['ticker']})")
display_price("Target closing price", target["price"])

print("\nPeer P/E multiples")
valid_peers = []
for peer in eligible_peers:
    if not positive_number(peer["price"]) or not positive_number(peer["diluted_eps"]):
        print(f"{peer['name']} ({peer['ticker']}): not meaningful")
        continue
    peer_pe = peer["price"] / peer["diluted_eps"]
    valid_peers.append({**peer, "pe": peer_pe})
    print(f"{peer['name']} ({peer['ticker']}): {peer_pe:.6f}x")

if not valid_peers:
    print("\nNo usable peers: no peer-implied estimate.")
else:
    multiples = [peer["pe"] for peer in valid_peers]
    minimum_pe = min(multiples)
    median_pe = median(multiples)
    maximum_pe = max(multiples)
    full_peer_estimate = implied_price(median_pe)

    print("\nPeer P/E summary")
    print(f"Minimum P/E: {minimum_pe:.6f}x")
    print(f"Median P/E: {median_pe:.6f}x")
    print(f"Maximum P/E: {maximum_pe:.6f}x")

    print("\nMSFT implied prices")
    if len(valid_peers) == 1:
        print("Reference estimate only: one valid peer, so no range.")
        display_price("Reference estimate", full_peer_estimate)
    else:
        display_price("Minimum peer P/E implied price", implied_price(minimum_pe))
        display_price("Median peer P/E implied price", full_peer_estimate)
        display_price("Maximum peer P/E implied price", implied_price(maximum_pe))

    print("\nLeave-one-peer-out analysis")
    for removed_peer in valid_peers:
        remaining = [peer for peer in valid_peers if peer["ticker"] != removed_peer["ticker"]]
        if not remaining:
            print(f"Remove {removed_peer['ticker']}: no estimate; no valid peers remain.")
            continue
        remaining_estimate = implied_price(median([peer["pe"] for peer in remaining]))
        if remaining_estimate is None or full_peer_estimate is None:
            print(f"Remove {removed_peer['ticker']}: remaining estimate not meaningful.")
        else:
            kind = "reference estimate; one valid peer remains" if len(remaining) == 1 else "median-implied price"
            print(
                f"Remove {removed_peer['ticker']}: {kind} ${remaining_estimate:,.2f}; "
                f"change from full-peer median estimate ${remaining_estimate - full_peer_estimate:,.2f}"
            )

print("\nNote: This P/E comparison does not add cash or subtract debt.")
