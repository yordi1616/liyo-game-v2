# --- Routes ---

@app.route('/')
def home_redirect():
    game_data = get_game_data(request)
    if not game_data.get('username'):
        return redirect(url_for('login'))
    return redirect(url_for('game'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        if not username:
            flash("Please enter a username!")
            return render_template('login.html')
        
        game_data = get_game_data(request)
        game_data['username'] = username # Set username
        
        # Initialize default game state for new users if it's their first time
        if game_data.get('score') is None:
            game_data['score'] = 0
            game_data['per_tap_bonus'] = 1
            game_data['current_tap_limit'] = DEFAULT_TAP_LIMIT
            game_data['taps_left'] = DEFAULT_TAP_LIMIT
            game_data['task_completed'] = False
            game_data['purchased_tap_upgrades'] = []
            game_data['purchased_limit_upgrades'] = []
            
        # Update last visit time upon login
        game_data['last_visit'] = datetime.now().isoformat()

        response = make_response(redirect(url_for('game')))
        return save_game_data(response, game_data)

    return render_template('login.html')
