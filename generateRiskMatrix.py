#!/usr/bin/env python3

import json
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import sys

def generate_risk_matrix_fixed_axes(json_file, output_file):
    with open(json_file, 'r') as file:
        data = json.load(file)

    probability_map = {
        "Almost Certain": 4,
        "Probable": 3,
        "Possible": 2,
        "Improbable": 1,
        "Rare": 0
    }

    consequence_map = {
        "Minor": 0,
        "Moderate": 1,
        "Major": 2,
        "Extreme": 3
    }

    risk_matrix = [[[] for _ in range(4)] for _ in range(5)]
    risk_trends = {}

    for item in data:
        prob = probability_map.get(item["Probability"], -1)
        cons = consequence_map.get(item["Consequence"], -1)
        if prob != -1 and cons != -1:
            risk_matrix[prob][cons].append(item["ID"])
            risk_trends[item["ID"]] = item["Risk Trend"]

    fig, ax = plt.subplots(figsize=(12, 9))

    red = "#FF0000"
    yellow = "#FFFF00"
    green = "#90EE90"
    blue = "#00FFFF"
    orange = "#FFA500"

    color_map = [
        [blue, blue, green, yellow],
        [blue, green, green, yellow],
        [blue, green, yellow, red],
        [blue, green, yellow, red],
        [green, yellow, red, red]
    ]

    trend_colors = {
        "Decreasing": green,
        "Stable": blue,
        "Increasing": orange,
        "Surging": red
    }

    for i in range(5):
        for j in range(4):
            rect = patches.Rectangle((j, i), 1, 1, linewidth=1, edgecolor='black', facecolor=color_map[i][j])
            ax.add_patch(rect)
            ids = risk_matrix[i][j]
            for k, id_val in enumerate(ids):
                trend_color = trend_colors.get(risk_trends[id_val], 'white')
                ax.text(j + 0.5, i + 0.5, str(id_val), ha='center', va='center', fontsize=12, color='black', bbox=dict(facecolor=trend_color, edgecolor='black', boxstyle='circle'))

    ax.set_xticks([0.5, 1.5, 2.5, 3.5])
    ax.set_xticklabels([])
    ax.set_yticks([0.5, 1.5, 2.5, 3.5, 4.5])
    ax.set_yticklabels([])

    for i, label in enumerate(["Minor", "Moderate", "Major", "Extreme"]):
        ax.text(i + 0.5, 5.2, label, ha='center', va='center', fontsize=12, color='black')
    
    for i, label in enumerate(["Rare", "Improbable", "Possible", "Probable", "Almost Certain"]):
        ax.text(-0.05, i + 0.5, label, ha='right', va='center', fontsize=12, color='black', rotation=0)

    ax.set_xlim(0, 4)
    ax.set_ylim(0, 5)
    ax.set_xticks(range(5))
    ax.set_yticks(range(6))
    ax.grid(True, which='both', color='black', linestyle='-', linewidth=0.5)

    ax.xaxis.set_major_formatter(plt.NullFormatter())
    ax.yaxis.set_major_formatter(plt.NullFormatter())

    ax.set_xlabel("Consequence", fontsize=14, labelpad=20)
    ax.set_ylabel("Likelihood", fontsize=14, labelpad=70)

    plt.title("Risk Matrix", fontsize=16, pad=20)

    plt.gca().invert_yaxis()
    plt.savefig(output_file)
    plt.close()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: ./generateRiskMatrix.py <path_to_json_file> <output_image_file>")
        sys.exit(1)

    json_file = sys.argv[1]
    output_file = sys.argv[2]
    generate_risk_matrix_fixed_axes(json_file, output_file)
