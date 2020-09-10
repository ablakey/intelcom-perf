"""
TODO
"""
import argparse
import json
from collections import Counter
from datetime import datetime
from pathlib import Path

import matplotlib.pyplot as plt

TIMESTAMP_FORMAT = "%a, %d %b %Y %H:%M:%S %z"


def calculate_timings(delivery):
    """Calculate metadata about each delivery including:
    - Time in seconds to deliver (from first email)
    - Number of deliveries total between emails
    - Seconds per delivery
    """
    start = datetime.strptime(delivery["start_date"], TIMESTAMP_FORMAT)
    end = datetime.strptime(delivery["end_date"], TIMESTAMP_FORMAT)
    delta = (end - start).seconds

    delivery_count = delivery["delivery_num"] - delivery["current_delivery"]

    return {
        "delivery_time": delta,
        "delivery_count": delivery_count,
        "individual_delivery_seconds": delta / delivery_count,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument("input", help="Input .json file created from get_intelcom_metadata.py", type=Path)
    args = parser.parse_args()

    with open(args.input, "r") as f:
        deliveries = json.load(f)

    driver_names = Counter([d["driver_name"] for d in deliveries.values()])
    delivery_timings = [calculate_timings(v) for v in deliveries.values()]

    # Build histogram and show mean.
    data = [d["delivery_time"] / 60 for d in delivery_timings]
    mean = sum(data) / len(data)
    plt.hist(data, edgecolor="k")
    plt.axvline(mean, color="k", linestyle="dashed", linewidth=1)
    min_ylim, max_ylim = plt.ylim()
    plt.text(mean * 1.4, max_ylim * 0.9, "Mean: {:.0f} minutes".format(mean))
    plt.title(f"Histogram of {len(data)} deliveries between first and final email")
    plt.xlabel("Delivery Time (minutes)")
    plt.show()

    # Build Time for each delivery histogram.
    data = [d["individual_delivery_seconds"] for d in delivery_timings]
    data = [d for d in data if d < 300]  # Hack to remove a few extraneous data points.

    mean = sum(data) / len(data)
    plt.hist(data, edgecolor="k")
    plt.axvline(mean, color="k", linestyle="dashed", linewidth=1)
    min_ylim, max_ylim = plt.ylim()
    plt.text(mean * 1.1, max_ylim * 0.9, "Mean: {:.0f} seconds".format(mean))
    plt.title(f"Histogram of {len(data)} times per individual delivery")
    plt.xlabel("Time per delivery (seconds)")
    plt.show()

    # Build histogram for delivery count
    data = [d["delivery_count"] for d in delivery_timings]
    mean = sum(data) / len(data)
    plt.hist(data, edgecolor="k")
    plt.axvline(mean, color="k", linestyle="dashed", linewidth=1)
    min_ylim, max_ylim = plt.ylim()
    plt.text(mean * 1.4, max_ylim * 0.9, "Mean: {:.0f}".format(mean))
    plt.title(f"Histogram of {len(data)} reported deliveries until my delivery")
    plt.xlabel("Delivery count")
    plt.show()
