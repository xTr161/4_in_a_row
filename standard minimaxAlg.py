import math


def minimax(current_depth: int, node_index: int, is_maximum: bool, scores: list, target_depth: int) -> int:
    # base case
    if current_depth == target_depth:
        return scores[node_index]
    if is_maximum:
        return max(minimax(current_depth + 1, node_index * 2, False, scores, target_depth),
                   minimax(current_depth + 1, node_index * 2 + 1, False, scores, target_depth))
    else:
        return max(minimax(current_depth + 1, node_index * 2, True, scores, target_depth),
                   minimax(current_depth + 1, node_index * 2 + 1, True, scores, target_depth))


# Driver code
scores_list = [3, 5, 2, 9, 12, 5, 23, 23]

treeDepth = math.log(len(scores_list), 2)

print("The optimal value is : ", end="")
print(minimax(0, 0, True, scores_list, int(treeDepth)))
