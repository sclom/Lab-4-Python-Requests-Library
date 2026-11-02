import sys
import json
import logging
from pathlib import Path

import requests

def get_card_value(val_str):
    mapping = {
        "ACE": 14,
        "KING": 13,
        "QUEEN": 12,
        "JACK": 11,
        "10": 10,
        "9": 9,
        "8": 8,
        "7": 7,
        "6": 6,
        "5": 5,
        "4": 4,
        "3": 3,
        "2": 2,
    }
    return mapping.get(val_str.upper(), 0)

def main():
    repo_dir = Path(__file__).resolve().parents[1]
    data_dir = repo_dir / "data"
    log_dir = repo_dir / "logs"
    data_dir.mkdir(parents=True, exist_ok=True)
    log_dir.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        filename=log_dir / "lab4.log",
        level=logging.INFO,
        format="%(message)s",
    )

    deck_url = "https://www.deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1"
    try:
        response = requests.get(deck_url, timeout=10)
        response.raise_for_status()
        deck_data = response.json()
        deck_id = deck_data.get("deck_id") if isinstance(deck_data, dict) else None
        if not deck_id:
            logging.error("LAB4_ERR")
            sys.exit(1)
        logging.info("LAB4_DECK_CREATE_OK")
    except (requests.Timeout, requests.RequestException, ValueError):
        logging.error("LAB4_ERR")
        sys.exit(1)
    try:
        user_input = input("Enter the number of players (at least 2): ").strip()
        num_players = int(user_input) 
        if num_players < 2:
            logging.error("LAB4_ERR")
            print("Error: Number of players must be at least 2")
            sys.exit(1)
    except EOFError:
        logging.error("LAB4_ERR")
        sys.exit(1)
    except ValueError:
        logging.error("LAB4_ERR")
        print("Error: Invalid input. Please enter an integer.")
        sys.exit(1)

    players = [f"Player {i+1}" for i in range(num_players)]
    active_players = players.copy()

    rounds_history = []
    round_num = 1
    winner = None
    while len(active_players) > 1:
        draw_url = f"https://www.deckofcardsapi.com/api/deck/{deck_id}/draw/?count={len(active_players)}"
        try:
            draw_resp = requests.get(draw_url, timeout=10)
            draw_resp.raise_for_status()
            draw_data = draw_resp.json()
        except (requests.Timeout, requests.RequestException, ValueError):
            logging.error("LAB4_ERR")
            sys.exit(1)
        logging.info("LAB4_DRAW_OK")
        cards_drawn = draw_data.get('cards', [])
        if len(cards_drawn) != len(active_players):
            logging.error("LAB4_ERR")
            print("Error: The API did not return one card per active player.")
            sys.exit(1)
        current_round_results = {}
        max_val = -1
        round_winner_candidates = []
        for idx, player in enumerate(active_players):
            card = cards_drawn[idx]
            val_str = card.get('value')
            val = get_card_value(val_str)
            suit = card.get('suit')
            current_round_results[player] = {
                'card': f"{val_str} of {suit}",
                'value': val,
                'raw_card': card
            }

            if val > max_val:
                max_val = val
                round_winner_candidates = [player]
            elif val == max_val:
                round_winner_candidates.append(player)
        round_record = {
            "round": round_num,
            "is_tie_breaker": round_num > 1,
            "results": current_round_results,
            "max_value": max_val,
            "winners_of_round": round_winner_candidates,
            "raw_response": draw_data,
        }
        rounds_history.append(round_record)
        with open(data_dir / "high_card_rounds.json", 'w', encoding='utf-8') as f:
            json.dump(rounds_history, f, indent=2)

        if len(round_winner_candidates) > 1:
            logging.info("LAB4_TIE_ROUND")
            active_players = round_winner_candidates
            round_num += 1
        else:
            winner = round_winner_candidates[0]
            break
    summary_lines = []
    summary_lines.append("=== High Card Game Summary ===")
    for r in rounds_history:
        summary_lines.append(f"\nRound {r['round']} (Tie-Breaker: {r['is_tie_breaker']})")
        for p, info in r['results'].items():
            summary_lines.append(f" - {p}: {info['card']} (Value: {info['value']})")
        summary_lines.append(f"  Round Winner(s): {', '.join(r['winners_of_round'])}")   
    summary_lines.append(f"\nFinal Winner: {winner}")
    print("\n".join(summary_lines))
    with open(data_dir / "high_card_result.txt", 'w', encoding='utf-8') as f:
        f.write("\n".join(summary_lines))

    logging.info("LAB4_GAME_END")
if __name__ == "__main__":
    main()
