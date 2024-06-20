import json
import logging
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import azure.functions as func
import tempfile
import os

# Constants for probability, consequence maps snf colours
PROBABILITY_MAP = {
    "Almost Certain": 4,
    "Probable": 3,
    "Possible": 2,
    "Improbable": 1,
    "Rare": 0
}

CONSEQUENCE_MAP = {
    "Minor": 0,
    "Moderate": 1,
    "Major": 2,
    "Extreme": 3
}

RED = "#FF0000"
YELLOW = "#FFFF00"
GREEN = "#90EE90"
BLUE = "#00FFFF"
ORANGE = "#FFA500"

COLOUR_MAP = [
    [BLUE, BLUE, GREEN, YELLOW],
    [BLUE, GREEN, GREEN, YELLOW],
    [BLUE, GREEN, YELLOW, RED],
    [BLUE, GREEN, YELLOW, RED],
    [GREEN, YELLOW, RED, RED]
]

TREND_COLOURS = {
    "Decreasing": GREEN,
    "Stable": BLUE,
    "Increasing": ORANGE,
    "Surging": RED
}

X_AXIS_DESC = "Consequence"
Y_AXIS_DESC = "Likelihood"
IMAGE_TITLE = "Risk Matrix"

def create_risk_matrix(data):
    """Creates a risk matrix and trends from input data."""
    risk_matrix = [[[] for _ in range(4)] for _ in range(5)]
    risk_trends = {}

    for item in data:
        prob = PROBABILITY_MAP.get(item["Probability"], -1)
        cons = CONSEQUENCE_MAP.get(item["Consequence"], -1)
        if prob != -1 and cons != -1:
            risk_matrix[prob][cons].append(item["ID"])
            risk_trends[item["ID"]] = item["Risk Trend"]
    return risk_matrix, risk_trends

def draw_risk_matrix(ax, risk_matrix, risk_trends):
    """Draws the risk matrix on the given Axes object."""
    for i in range(5):
        for j in range(4):
            rect = patches.Rectangle((j, i), 1, 1, linewidth=1, edgecolor='black', facecolor=COLOUR_MAP[i][j])
            ax.add_patch(rect)
            ids = risk_matrix[i][j]
            for k, id_val in enumerate(ids):
                trend_color = TREND_COLOURS.get(risk_trends[id_val], 'white')
                ax.text(j + 0.5, i + 0.5, str(id_val), ha='center', va='center', fontsize=12, color='black', bbox=dict(facecolor=trend_color, edgecolor='black', boxstyle='circle'))

def format_risk_matrix(ax):
    """Formats the risk matrix plot."""
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

    ax.set_xlabel(X_AXIS_DESC, fontsize=14, labelpad=20)
    ax.set_ylabel(Y_AXIS_DESC, fontsize=14, labelpad=70)

    plt.title(IMAGE_TITLE, fontsize=16, pad=20)

    plt.gca().invert_yaxis()
    
def generate_risk_matrix_fixed_axes(data, output_file):
    """Generates a risk matrix plot and saves it to a file."""
    try:
        risk_matrix, risk_trends = create_risk_matrix(data)
        fig, ax = plt.subplots(figsize=(12, 9))
        draw_risk_matrix(ax, risk_matrix, risk_trends)
        format_risk_matrix(ax)
        plt.savefig(output_file)
        plt.close()
    except Exception as e:
        logging.error(f"Error in generate_risk_matrix_fixed_axes: {e}")
        raise

def main(req: func.HttpRequest) -> func.HttpResponse:
    """Azure Function entry point."""
    logging.info('Python HTTP trigger function processed a request.')

    try:
        req_body = req.get_json()
        #logging.info("Received JSON body: %s", req_body)
    except ValueError as e:
        logging.error(f"Invalid JSON input: {e}")
        return func.HttpResponse(
             f"Invalid JSON input: {e}",
             status_code=400
        )

    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
        output_file = temp_file.name
    try:
        generate_risk_matrix_fixed_axes(req_body, output_file)
        with open(output_file, "rb") as image_file:
            logging.info("Generated risk matrix successfully")
            return func.HttpResponse(image_file.read(), mimetype="image/png")
    except Exception as e:
        logging.error(f"Error generating risk matrix: {e}")
        return func.HttpResponse(
             f"Error generating risk matrix: {e}",
             status_code=500
        )
    finally:
        try:
            os.remove(output_file)
        except Exception as e:
            logging.error(f"Error deleting temporary file: {e}")
