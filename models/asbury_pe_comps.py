"""Lab 07: Comparable-company P/E policy and implied-price range.

Run from the repository root:
    python models\asbury_pe_comps.py
"""

from statistics import median


# =============================================================================
# EDITABLE CASE INPUTS
# Prices are December 31, 2024 closes. EPS is FY2024 total GAAP diluted EPS.
# =============================================================================
target = {
    "ticker": "ABG",
    "name": "Asbury Automotive Group",
    "price": 243.03,
    "diluted_eps": 21.50,
}

peers = [
    {"ticker": "AN", "name": "AutoNation", "price": 169.84, "diluted_eps": 16.92},
    {"ticker": "GPI", "name": "Group 1 Automotive", "price": 421.48, "diluted_eps": 36.81},
]
# =============================================================================


def is_positive_number(value):
    """Return True only for numeric values greater than zero."""
    return isinstance(value, (int, float)) and value > 0


def implied_price(peer_multiple, target_eps):
    """Return an implied target price, or None if target EPS is unusable."""
    if not is_positive_number(target_eps):
        return None
    return peer_multiple * target_eps


def print_price(label, value):
    """Print a price, explicitly labeling an unavailable calculation."""
    if value is None:
        print(f"{label}: not meaningful")
    else:
        print(f"{label}: ${value:,.2f}")


target_ticker = target["ticker"].upper()
deduplicated_peers = []
seen_tickers = set()

for peer in peers:
    peer_ticker = peer["ticker"].upper()
    if peer_ticker == target_ticker:
        print(f"Excluded target from peers: {peer['ticker']}")
        continue
    if peer_ticker in seen_tickers:
        print(f"Excluded duplicate peer: {peer['ticker']}")
        continue
    seen_tickers.add(peer_ticker)
    deduplicated_peers.append(peer)

print("P/E comparable-company analysis")
print(f"Target: {target['name']} ({target['ticker']})")
if is_positive_number(target["price"]):
    print(f"Target reference price: ${target['price']:,.2f}")
else:
    print("Target reference price: not meaningful")

if not is_positive_number(target["diluted_eps"]):
    print("Target diluted EPS: not meaningful")

print("\nPeer P/E multiples")
valid_peers = []
for peer in deduplicated_peers:
    if not is_positive_number(peer["price"]) or not is_positive_number(peer["diluted_eps"]):
        print(f"{peer['name']} ({peer['ticker']}): not meaningful")
        continue

    peer_multiple = peer["price"] / peer["diluted_eps"]
    valid_peers.append({**peer, "pe": peer_multiple})
    print(f"{peer['name']} ({peer['ticker']}): {peer_multiple:.6f}x")

if not valid_peers:
    print("\nNo usable peers: no peer-implied estimate.")
else:
    peer_multiples = [peer["pe"] for peer in valid_peers]
    minimum_multiple = min(peer_multiples)
    median_multiple = median(peer_multiples)
    maximum_multiple = max(peer_multiples)

    print("\nPeer P/E summary")
    print(f"Minimum P/E: {minimum_multiple:.6f}x")
    print(f"Median P/E: {median_multiple:.6f}x")
    print(f"Maximum P/E: {maximum_multiple:.6f}x")

    print("\nAsbury implied prices")
    if len(valid_peers) == 1:
        print("Reference estimate only: one valid peer, so no range.")
        print_price("Reference estimate", implied_price(median_multiple, target["diluted_eps"]))
    else:
        print_price("Minimum peer P/E implied price", implied_price(minimum_multiple, target["diluted_eps"]))
        print_price("Median peer P/E implied price", implied_price(median_multiple, target["diluted_eps"]))
        print_price("Maximum peer P/E implied price", implied_price(maximum_multiple, target["diluted_eps"]))

    full_peer_estimate = implied_price(median_multiple, target["diluted_eps"])
    print("\nLeave-one-peer-out analysis")
    for removed_peer in valid_peers:
        remaining_peers = [peer for peer in valid_peers if peer["ticker"] != removed_peer["ticker"]]
        if not remaining_peers:
            print(f"Remove {removed_peer['ticker']}: no estimate; no valid peers remain.")
            continue

        remaining_median = median([peer["pe"] for peer in remaining_peers])
        remaining_estimate = implied_price(remaining_median, target["diluted_eps"])
        if remaining_estimate is None or full_peer_estimate is None:
            print(f"Remove {removed_peer['ticker']}: remaining estimate not meaningful.")
        else:
            dollar_change = remaining_estimate - full_peer_estimate
            range_note = "reference estimate; one valid peer remains" if len(remaining_peers) == 1 else "median-implied price"
            print(
                f"Remove {removed_peer['ticker']}: {range_note} ${remaining_estimate:,.2f}; "
                f"change from full-peer median estimate ${dollar_change:,.2f}"
            )

print("\nNote: This P/E comparison does not add cash or subtract debt.")
