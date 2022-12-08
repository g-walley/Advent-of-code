from pathlib import Path
import pandas as pd


def pt1(input_path: Path):
    """part 1"""
    forest: pd.DataFrame = pd.read_csv(input_path, delim_whitespace=True, header=None)

    middle_trees = forest.iloc[1:-1, 1:-1]
    visible_trees = forest.size - middle_trees.size
    for row in range(1, forest.shape[1] - 1):
        for col in range(1, forest.shape[1] - 1):
            tree_height = forest.iat[row, col]

            trees_to_left = forest.iloc[row, 0:col]
            if max(trees_to_left) < tree_height:
                visible_trees += 1
                continue

            trees_to_right = forest.iloc[row, col + 1 :]
            if max(trees_to_right) < tree_height:
                visible_trees += 1
                continue

            trees_above = forest.iloc[0:row, col]
            if max(trees_above) < tree_height:
                visible_trees += 1
                continue

            trees_below = forest.iloc[row + 1 :, col]
            if max(trees_below) < tree_height:
                visible_trees += 1
                continue
    return visible_trees


def pt2(input_path):
    """part 2"""
    forest: pd.DataFrame = pd.read_csv(input_path, delim_whitespace=True, header=None)

    max_score = 0
    for row in range(1, forest.shape[0] - 1):
        for col in range(1, forest.shape[1] - 1):
            tree_height = forest.iat[row, col]
            right_score = 0
            left_score = 0
            above_score = 0
            below_score = 0

            trees_to_left = forest.iloc[row, 0:col]
            max_tree_height = trees_to_left.max()
            if max_tree_height < tree_height:
                left_score = trees_to_left.size
            elif trees_to_left.min() >= tree_height:
                left_score = 1
            else:
                max_tree_loc = trees_to_left.idxmax()
                while True:
                    trees_to_left = forest.iloc[row, max_tree_loc + 1 : col]
                    if trees_to_left.size < 1:
                        left_score = abs(max_tree_loc - col)
                        break
                    m_height = trees_to_left.max()
                    if m_height < tree_height:
                        left_score = abs(max_tree_loc - col)
                        break
                    max_tree_loc = trees_to_left.idxmax()
                    left_score = abs(max_tree_loc - col)

            trees_to_right = forest.iloc[row, col + 1 :]
            max_tree_height = trees_to_right.max()
            if max_tree_height < tree_height:
                right_score = trees_to_right.size
            elif trees_to_right.min() >= tree_height:
                right_score = 1
            else:
                max_tree_loc = trees_to_right.idxmax()
                while True:
                    trees_to_right = forest.iloc[row, col + 1 : max_tree_loc]
                    if trees_to_right.size < 1:
                        right_score = abs(max_tree_loc - col)
                        break
                    m_height = trees_to_right.max()

                    if m_height < tree_height:
                        right_score = abs(max_tree_loc - col)
                        break
                    max_tree_loc = trees_to_right.idxmax()
                    right_score = abs(max_tree_loc - col)

            trees_above = forest.iloc[0:row, col]
            max_tree_height = trees_above.max()
            if max_tree_height < tree_height:
                above_score = trees_above.size
            elif trees_above.min() >= tree_height:
                above_score = 1
            else:
                max_tree_loc = trees_above.idxmax()
                while True:
                    trees_above = forest.iloc[max_tree_loc + 1 : row, col]
                    if trees_above.size < 1:
                        above_score = abs(max_tree_loc - row)
                        break
                    m_height = trees_above.max()

                    if m_height < tree_height:
                        above_score = abs(max_tree_loc - row)
                        break

                    max_tree_loc = trees_above.idxmax()
                    above_score = abs(max_tree_loc - row)

            trees_below = forest.iloc[row + 1 :, col]
            max_tree_height = trees_below.max()
            if max_tree_height < tree_height:
                below_score = trees_below.size
            elif trees_below.min() >= tree_height:
                below_score = 1
            else:
                max_tree_loc = trees_below.idxmax()
                while True:
                    trees_below = forest.iloc[row + 1 : max_tree_loc, col]
                    if trees_below.size < 1:
                        below_score = abs(max_tree_loc - row)
                        break
                    m_height = trees_below.max()

                    if m_height < tree_height:
                        below_score = abs(max_tree_loc - row)
                        break

                    max_tree_loc = trees_below.idxmax()
                    below_score = abs(max_tree_loc - row)

            score = left_score * right_score * above_score * below_score

            assert all(
                [above_score, below_score, right_score, left_score]
            ), f"{above_score, below_score, right_score, left_score}"
            if score > max_score:
                max_score = score

    return max_score
