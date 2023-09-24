#!/bin/python3

import json
import os


def go_back_in_subset_stack(
    sorted_integers: list[int],
    subset_stack: list[int],
    remaining_target: int,
) -> tuple[int, int]:
    last_index = subset_stack.pop()
    return last_index + 1, remaining_target + sorted_integers[last_index]


def set_of_subset_with_target_sum(
    sorted_integers: list[int], target: int
) -> list[list[int]]:
    """Returns the set of subsets in `sorted_integers` that sum up to `target`.

    Args:
        sorted_integers: Ascending sorted list of non-negative integers.
        target: Non-negative integer.

    Returns:
        A list of combinations that sum up to the target (indexes instead of values).
    """
    matching_subsets: list[list[int]] = []
    curr_index, remaining_target = 0, target
    subset_stack: list[int] = []

    while True:
        if remaining_target == 0:
            matching_subsets.append(subset_stack.copy())

        if remaining_target == 0 or curr_index >= len(sorted_integers):
            if len(subset_stack) < 1:
                break
            curr_index, remaining_target = go_back_in_subset_stack(
                sorted_integers, subset_stack, remaining_target
            )
            continue

        if sorted_integers[curr_index] > remaining_target:
            if len(subset_stack) < 1:
                break
            curr_val = sorted_integers[curr_index]
            last_val = sorted_integers[subset_stack[-1]]
            curr_index, remaining_target = go_back_in_subset_stack(
                sorted_integers, subset_stack, remaining_target
            )
            # In case the current integer overshoots and has the same value as the
            # last integer in the stack, then the next useful value cannot be less
            # than the remaining target (actually has to be equal).
            if curr_val == last_val:
                while (
                    curr_index < len(sorted_integers)
                    and sorted_integers[curr_index] < remaining_target
                ):
                    curr_index += 1
            continue

        remaining_target -= sorted_integers[curr_index]
        subset_stack.append(curr_index)
        curr_index += 1

    return matching_subsets


if __name__ == "__main__":
    inp: dict
    with open(os.environ["INPUT_PATH"], "r") as f:
        inp = json.load(f)

    out = set_of_subset_with_target_sum(sorted(inp["integers"]), inp["target"])

    with open(os.environ["OUTPUT_PATH"], "w") as f:
        json.dump(out, f, indent=2)
