def handDim(head_length):
    hand_length = round(0.75 * head_length, 2)
    hand_circumference = round(6.1537 * hand_length, 2)
    palm_length = round((0.23 * hand_circumference) + 5.57, 2)
    hand_breadth = round((0.32 * hand_circumference) + 1.88, 2)
    return (
    f"hand_length = {hand_length}",
    f"hand_circumference = {hand_circumference}",
    f"palm_length = {palm_length}",
    f"hand_breadth = {hand_breadth}"
)