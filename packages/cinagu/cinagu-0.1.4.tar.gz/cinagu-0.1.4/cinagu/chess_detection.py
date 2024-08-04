# chess_detection.py

import chess.pgn


def detect_abnormal_moves(game):
    """
    Detect abnormal moves in a chess game.
    An abnormal move is identified based on custom logic which should be implemented here.

    Args:
        game (chess.pgn.Game): The chess game object parsed from PGN data.

    Returns:
        list: A list of moves that are identified as abnormal.
    """
    if game is None:
        raise ValueError("Game object is None, cannot detect moves.")

    board = game.board()
    abnormal_moves = []

    for move in game.mainline_moves():
        board.push(move)
        # Example logic for detecting abnormal moves
        # You need to replace this with your actual detection logic
        if board.is_checkmate() or board.is_check():
            abnormal_moves.append(move)

    return abnormal_moves


def detect_cheating_pattern(game):
    """
    Detect cheating patterns in a chess game based on abnormal moves.

    Args:
        game (chess.pgn.Game): The chess game object parsed from PGN data.

    Returns:
        bool: True if cheating patterns are detected, False otherwise.
    """
    if game is None:
        raise ValueError("Game object is None, cannot detect cheating pattern.")

    abnormal_moves = detect_abnormal_moves(game)

    # Example logic for detecting cheating patterns
    # Replace with your actual cheating detection logic
    return bool(abnormal_moves)
