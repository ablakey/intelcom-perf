#!/usr/bin/python3
"""
Read a .mbox file containing intelcom "on the way" and "delivered" emails.
Outputs a .json file of metadata about each order. Omits orders that lack both
a start and end date.
"""


import argparse
import json
import re
from collections import defaultdict
from mailbox import mbox, mboxMessage
from pathlib import Path

delivery_id_pattern = re.compile(r"INTLCMA([^\s]+)")
delivery_num_pattern = re.compile(r"you are delivery number ([0-9]+)")
current_delivery_pattern = re.compile(r"is currently completing delivery number ([0-9]+)")
driver_name_pattern = re.compile(r"by our driver ([^\s.]+)")


def get_email_body(email: mboxMessage):
    if email.is_multipart():
        body = "".join(part.as_string() for part in email.get_payload())
    else:
        body = email.get_payload().as_string()

    # ham handedly strip HTML and newlines.
    body = re.sub("<[^<]+?>", "", body)
    return body.replace("=\n", "").replace("\n", " ")  # TODO re.sub


def parse_second_email(email: mboxMessage):
    """Parse the common elements from either email.

    start_date in format: Wed, 21 Aug 2019 13:03:28 +0000.
    """
    return {
        "delivery_id": delivery_id_pattern.search(email["subject"]).group(1),
        "end_date": email["date"],
    }


def parse_first_email(email: mboxMessage):
    """Parse the "On the way!" email.

    Driver names need to be lowercased because some emails reports name in ALLCAPS.
    start_date in format: Wed, 21 Aug 2019 13:03:28 +0000.
    """

    body = get_email_body(email)

    return {
        "start_date": email["date"],
        "current_delivery": int(current_delivery_pattern.search(body).group(1)),
        "delivery_num": int(delivery_num_pattern.search(body).group(1)),
        "delivery_id": delivery_id_pattern.search(email["subject"]).group(1),
        "driver_name": driver_name_pattern.search(body).group(1).lower(),
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument("input", help="Input .mbox file from Google Takeout", type=Path)
    parser.add_argument("output", help="Output .json file path.", type=Path)
    args = parser.parse_args()
    opened_mailbox = mbox(args.input)

    deliveries = defaultdict(dict)

    for email in opened_mailbox:
        if "on the way" in email["subject"]:
            parsed_email = parse_first_email(email)
        else:
            parsed_email = parse_second_email(email)

        deliveries[parsed_email["delivery_id"]].update(parsed_email)

    # Scrub any incomplete delivery entries.
    for d in list(deliveries.values()):
        if "start_date" not in d or "end_date" not in d:
            print(
                f"{d['delivery_id']} start: {d.get('start_date', '?')} end: {d.get('end_date', '?')} is incomplete. "
                "Omitting."
            )
            deliveries.pop(d["delivery_id"])

    with open(args.output, "w") as f:
        json.dump(deliveries, f, indent=4)

    print(f"Wrote {len(deliveries)} deliveries to {args.output.absolute()}.")
