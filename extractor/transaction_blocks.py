import re

# Transaction start:
# Serial number + Transaction ID (e.g. "1 S3604")
START_PATTERN = re.compile(r"^\d+\s+[A-Z]\d+")


def extract_transaction_blocks(lines):
    """
    Groups lines into transaction blocks.
    A block starts ONLY when we see:
    <serial number> <transaction id>
    """

    blocks = []
    current_block = []

    for line in lines:
        if START_PATTERN.match(line):
            # New transaction begins
            if current_block:
                blocks.append(current_block)
            current_block = [line]
        else:
            if current_block:
                current_block.append(line)

    if current_block:
        blocks.append(current_block)

    return blocks
