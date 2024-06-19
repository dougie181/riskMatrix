import json
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def generate_risk_matrix(json_file):
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

    color_map = [
        ["#00FFFF", "#00FFFF", "#00FFFF", "#FFFF00"],
        ["#00FFFF", "#00FFFF", "#FFFF00", "#FFFF00"],
        ["#00FFFF", "#00FFFF", "#FFFF00", "#FF0000"],
        ["#00FFFF", "#FFFF00", "#FF0000", "#FF0000"],
        ["#00FFFF", "#FFFF00", "#FF0000", "#FF0000"]
    ]

    for i in range(5):
        for j in range(4):
            rect = patches.Rectangle((j, i), 1, 1, linewidth=1, edgecolor='black', facecolor=color_map[i][j])
            ax.add_patch(rect)
            ids = risk_matrix[i][j]
            for k, id_val in enumerate(ids):
                ax.text(j + 0.5, i + 0.7 - k*0.3, str(id_val), ha='center', va='center', fontsize=12, color='black', bbox=dict(facecolor='white', edgecolor='black', boxstyle='circle'))

    ax.set_xticks([0.5, 1.5, 2.5, 3.5])
    ax.set_xticklabels(["Minor", "Moderate", "Major", "Extreme"], fontsize=12)
    ax.set_yticks([0.5, 1.5, 2.5, 3.5, 4.5])
    ax.set_yticklabels(["Rare", "Improbable", "Possible", "Probable", "Almost Certain"], fontsize=12)

    ax.set_xlabel("Consequence", fontsize=14)
    ax.set_ylabel("Probability", fontsize=14)
    ax.set_title("Risk Matrix", fontsize=16)
    plt.gca().invert_yaxis()
    plt.grid(True, which='both', color='black', linestyle='-', linewidth=0.5)
    plt.show()

# Usage
generate_risk_matrix('./risk_data.json')
