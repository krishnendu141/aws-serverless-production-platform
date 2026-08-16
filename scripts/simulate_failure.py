#!/usr/bin/env python3
"""Simulate failure scenarios locally against the test harness.
Usage examples:
  python scripts/simulate_failure.py --scenario lambda-error
"""
import argparse

SCENARIOS = ['lambda-error','bedrock-error','queue-backlog','duplicate-event','sla-breach','downstream-timeout']


def run_scenario(name):
    if name not in SCENARIOS:
        raise SystemExit('Unknown scenario')
    print('Simulating', name)
    # For safety: this script only prints actions. Real simulation tools should be used in controlled environments.

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--scenario', required=True)
    args = p.parse_args()
    run_scenario(args.scenario)
