from flask import Flask, render_template, request, redirect, url_for, make_response, session, flash
import json
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_very_secret_key_for_this_hamster_kombat_clone_game'

# --- Game Configuration ---
# Upgrades for 'Earn' page (per-tap profit)
TAP_UPGRADES = {
    'tap_upgrade_2': {'name': '+2 Tap', 'cost': 500, 'per_tap_bonus': 2},
    'tap_upgrade_3': {'name': '+3 Tap', 'cost': 700, 'per_tap_bonus': 3},
    'tap_upgrade_5': {'name': '+5 Tap', 'cost': 1200, 'per_tap_bonus': 5},
    'tap_upgrade_10': {'name': '+10 Tap', 'cost': 5000, 'per_tap_bonus': 10},
}

# Upgrades for 'Members' page (tap limit / energy)
LIMIT_UPGRADES = {
    'limit_upgrade_2000': {'name': 'Tap Limit +2000', 'cost': 500, 'bonus_limit': 2000},
    'limit_upgrade_3000': {'name': 'Tap Limit +3000', 'cost': 1000, 'bonus_limit': 3000},
    'limit_upgrade_4000': {'name': 'Tap Limit +4000', 'cost': 2000, 'bonus_limit': 4000},
    'limit_upgrade_5000': {'name': 'Tap Limit +5000', 'cost': 2500, 'bonus_limit': 5000},
}

DEFAULT_TAP_LIMIT = 1000 # Initial tap limit
TAP_REGEN_RATE_PER_SECOND = 1 # Taps regenerated per second

# --- Helper Functions for Cookie Management ---
def get_game_data(request):
    """Retrieves game data from cookie, or initializes it."""
    try:
        data = json.loads(request.cookies.get('game_data', '{}'))
    except json.JSONDecodeError:
        data = {} # If cookie is corrupted, reset it

    # Default values for new or corrupted data
    return {
        'username': data.get('username'),
        'score': data.get('score', 0),
        'last_visit': data.get('last_visit', datetime.now().isoformat()),
        'claimed_daily_bonus_date': data.get('claimed_daily_bonus_date', None),
        'per_tap_bonus': data.get('per_tap_bonus', 1), # Default 1 point per tap
        'current_tap_limit': data.get('current_tap_limit', DEFAULT_TAP_LIMIT),
        'taps_left': data.get('taps_left', DEFAULT_TAP_LIMIT),
        'task_completed': data.get('task_completed', False), # For 'akalewold' task
        'purchased_tap_upgrades': data.get('purchased_tap_upgrades', []), # List of IDs
        'purchased_limit_upgrades': data.get('purchased_limit_upgrades', []) # List of IDs
    }

def save_game_data(response, data):
    """Saves game data to cookie."""
    response.set_cookie('game_data', json.dumps(data))
    return response

def calculate_passive_income_and_regen_taps(game_data):
    """Calculates passive income (profit_per_hour not implemented yet, so no income for now)
       and regenerates taps based on time elapsed."""
    
    last_visit_time = datetime.fromisoformat(game_data['last_visit'])
    current_time = datetime.now()
    
    time_elapsed_seconds = (current_time - last_visit_time).total_seconds()
    
    # Regenerate taps
    regenerated_taps
