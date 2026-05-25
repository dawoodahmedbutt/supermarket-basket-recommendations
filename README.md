# Market Basket Analysis — Graph-Based Product Recommendations

A Python CLI tool that models supermarket transaction data as a weighted undirected graph to discover product bundles, score cross-sell confidence, and surface niche item recommendations.

## What it does

The tool answers four analytical questions about co-purchase behaviour:

| Question | Method |
|---|---|
| Top co-purchased product pairs | Weighted edge ranking via Bubble Sort |
| Items most frequently bought alongside a given item | Adjacency list lookup + Bubble Sort |
| Strategic cross-sell opportunities | Confidence scoring `P(B\|A)` with commodity filtering |
| Hidden (indirect) product relationships | Breadth-First Search across 2 hops, hub-filtered |

The graph is built from raw transaction records grouped by `(Member_number, Date)` — each unique shopping trip becomes one transaction, and each pair of items in that trip gets an edge increment.

## Tech stack

| Layer | Library |
|---|---|
| Core data structure | Python standard library (`collections`, `itertools`) |
| Graph algorithms | Custom implementation (BFS, Bubble Sort, Confidence) |
| Graph rendering | `networkx` |
| Plot output | `matplotlib` |

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python main.py
```

To change the item used for Q2 and Q4 analysis, edit `TARGET_ITEM` at the top of [main.py](main.py).

**Run tests:**

```bash
python -m unittest discover tests
```

## Output

Running `main.py` prints analytical results to the terminal and generates two sets of visualisations:

**Global network** — all product pairs with ≥ 50 co-purchases. Node size reflects item frequency; edge width reflects co-purchase count.

![Global co-purchase network](market_graph_global.png)

**Ego graphs** — one per top-10 volume driver, showing its 15 strongest product links. The central node (gold) is the driver; neighbours (blue) are its most common companions.

| Rank | Item | Sample ego graph |
|---|---|---|
| 1 | whole milk | ![Whole milk ego graph](<report_images/rank_1_whole milk.png>) |
| 2 | other vegetables | ![Other vegetables ego graph](<report_images/rank_2_other vegetables.png>) |
| 3 | rolls/buns | ![Rolls/buns ego graph](report_images/rank_3_rolls_buns.png) |

## Project structure

```
market-basket-analysis/
├── data/
│   └── Supermarket_dataset_PAI.csv   # Raw transaction records (Member_number, Date, itemDescription)
├── src/
│   ├── loader.py            # CSV ingestion — groups rows into transactions by (member, date)
│   ├── data_structure.py    # MarketBasketGraph — weighted adjacency list
│   ├── algorithms.py        # MarketBasketAnalyser — ranking, BFS, confidence, cross-sell logic
│   └── visualisation.py     # GraphVisualiser — global network and ego graph plots
├── tests/
│   ├── test_structure.py    # Graph node/edge/frequency behaviour
│   ├── test_algorithm.py    # Bundle ranking, BFS, confidence, top-N
│   ├── test_loader.py       # Transaction grouping and error handling
│   └── test_main.py         # Smoke test for full pipeline execution
├── report_images/           # Generated ego graph PNGs (top 10 items)
├── market_graph_global.png  # Generated global network plot
├── requirements.txt
└── main.py                  # Entry point
```

## Key design decisions

- **Custom data structure over a library graph:** The weighted adjacency list (`defaultdict` of `defaultdict`) was implemented from scratch to demonstrate graph fundamentals rather than delegating to NetworkX for storage.
- **Bubble Sort for ranking:** Used deliberately as a demonstration of algorithmic implementation; the sort is on small result sets so performance is not a concern.
- **Commodity filtering for cross-sells:** High-frequency items like `whole milk` appear as the top partner for almost every driver. Filtering them out as promotion *targets* surfaces actionable, non-obvious pairings.
- **Hub filtering in BFS:** `whole milk`, `other vegetables`, and a few other mega-hubs connect to nearly everything in the graph. Excluding them from BFS results prevents every niche query from returning the same items.
