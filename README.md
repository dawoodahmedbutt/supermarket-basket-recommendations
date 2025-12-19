# Market Basket Analysis Tool (Task 2)

## Overview
A Python-based tool to analyse supermarket transaction data using Graph Theory. It identifies product bundles, calculates cross-sell probabilities, and visualizes relationships to provide strategic merchandising insights.

## Features
* **Graph Structure:** Weighted Adjacency List for efficient transaction modeling.
* **Algorithms:** Bubble Sort (Ranking), BFS (Niche Discovery), Confidence Calculation.
* **Visualisation:** Global network plots and targeted "Ego Graphs" for top 10 volume drivers.

## Usage
1. Install dependencies: `pip install networkx matplotlib`
2. Run the tool: `python3 main.py`
3. Run tests: `python3 -m unittest discover tests`