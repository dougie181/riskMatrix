#!/usr/bin/env python3

import json
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import sys

def showRiskMatrix(json_file):
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

    for item in data:
        prob = probability_map.get(item["Probability"], -1)
        cons = consequence_map.get(item["Consequence"], -1)
        if prob != -1 and cons != -1:
            risk_matrix[prob][cons].append(item["ID"])

    fig, ax = plt.subplots(figsize=(12, 9))

    red = "#FF0000"
    yellow = "#FFFF00"
    green = "#90EE90"
    blue = "#00FFFF"

    color_map = [
        [blue, blue, green, yellow],
        [blue, green, green, yellow],
        [blue, green, yellow, red],
        [blue,green,yellow,red],
        [green, yellow, red, red]
    ]

    for i in range(5):
        for j in range(4):
            rect = patches.Rectangle((j, i), 1, 1, linewidth=1, edgecolor='black', facecolor=color_map[i][j])
            ax.add_patch(rect)
            ids = risk_matrix[i][j]
            for k, id_val in enumerate(ids):
                ax.text(j + 0.5, i + 0.5, str(id_val), ha='center', va='center', fontsize=12, color='black', bbox=dict(facecolor='white', edgecolor='black', boxstyle='circle'))

    ax.set_xticks([0.5, 1.5, 2.5, 3.5])
    ax.set_xticklabels([])
    ax.set_yticks([0.5, 1.5, 2.5, 3.5, 4.5])
    ax.set_yticklabels([])

    # Add labels to the middle of each column and row
    for i, label in enumerate(["Minor", "Moderate", "Major", "Extreme"]):
        ax.text(i + 0.5, 5.2, label, ha='center', va='center', fontsize=12, color='black')
    
    for i, label in enumerate(["Rare", "Improbable", "Possible", "Probable", "Almost Certain"]):
        ax.text(-0.05, i + 0.5, label, ha='right', va='center', fontsize=12, color='black', rotation=0)

    ax.set_xlim(0, 4)
    ax.set_ylim(0, 5)
    ax.set_xticks(range(5))
    ax.set_yticks(range(6))
    ax.grid(True, which='both', color='black', linestyle='-', linewidth=0.5)

    # Only show the grid lines that divide the cells
    ax.xaxis.set_major_formatter(plt.NullFormatter())
    ax.yaxis.set_major_formatter(plt.NullFormatter())

    # Adding axis titles
    ax.set_xlabel("Consequence", fontsize=14, labelpad=20)
    ax.set_ylabel("Likelihood", fontsize=14, labelpad=70)

    # Adjust position of y-axis label and axis title
    #ax.yaxis.set_label_coords(-0.2, 0.5)

    # Positioning the title
    plt.title("Risk Matrix", fontsize=16, pad=20)

    plt.gca().invert_yaxis()
    plt.show()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: ./showRiskMatrix.py <path_to_json_file>")
        sys.exit(1)

    json_file = sys.argv[1]
    showRiskMatrix(json_file)
