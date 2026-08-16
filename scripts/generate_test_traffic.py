#!/usr/bin/env python3
"""Generate synthetic test requests for TelcoFlow Nexus.
This script emits sample JSON to stdout or to a file for safe local testing.
"""
import argparse
import json
import random
from pathlib import Path

SAMPLES = [
    'examples/requests/network-outage.json',
    'examples/requests/billing.json'
]


def load_sample(path):
    return json.loads(Path(path).read_text())


def main(count, out):
    out_path = Path(out) if out else None
    items = []
    for i in range(count):
        sample = load_sample(random.choice(SAMPLES))
        sample['request_id'] = f'req-{i}'
        items.append(sample)
    if out_path:
        out_path.write_text('\n'.join(json.dumps(x) for x in items))
        print(f'Wrote {len(items)} items to {out_path}')
    else:
        for x in items:
            print(json.dumps(x))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--count', type=int, default=10)
    parser.add_argument('--out', help='output file')
    args = parser.parse_args()
    main(args.count, args.out)
