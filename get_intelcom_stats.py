#!/usr/bin/python3

import argparse
import mailbox
import re
from collections import defaultdict
from datetime import datetime
from pathlib import Path

delivery_id_pattern = re.compile(r"INTLCMA([^\s]+)")


def parse_common_elements(email: mailbox.mboxMessage):
    return {
        "delivery_id": delivery_id_pattern.search(email["subject"]).group(1),
        "date": datetime.strptime(email["date"], "%a, %d %b %Y %H:%M:%S %z"),
    }


def parse_first_email(email: mailbox.mboxMessage):
    """Parse an "On the way!" email."""
    return {**parse_common_elements(email)}


def parse_second_email(email: mailbox.mboxMessage):
    """Parse an "Delivered!" email."""
    return {**parse_common_elements(email)}


def main():
    parser = argparse.ArgumentParser(
        "Calculate statistics about Intelcom deliveries given Intelcom emails in a .mbox file."
    )

    parser.add_argument("mbox_file", type=Path)
    args = parser.parse_args()
    mbox = mailbox.mbox(args.mbox_file)

    deliveries = defaultdict(dict)

    for email in mbox:
        parsed_email = parse_first_email(email) if "on the way" in email["subject"] else parse_second_email(email)
        deliveries[parsed_email["delivery_id"]].update(parsed_email)


if __name__ == "__main__":
    main()
