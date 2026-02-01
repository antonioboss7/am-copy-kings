
# ==================== HTML TEMPLATES (CONTINUED) ====================

DASHBOARD_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>AM Copy Kings - Dashboard</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', Arial; background: #0a0a0f; color: #fff; }
        .sidebar { width: 250px; background: #151520; height: 100vh; position: fixed; border-right: 1px solid rgba(255,215,0,0.1); }
        .logo { padding: 30px; text-align: center; border-bottom: 1px solid rgba(255,215,0,0.1); }
        .logo h1 { color: #ffd700; font-size: 24px; }
        .nav { padding: 20px 0; }
        .nav a { display: block; padding: 15px 30px; color: #888; text-decoration: none; transition: all 0.3s; }
        .nav a:hover, .nav a.active { background: rgba(255,215,0,0.1); color: #ffd700; border-left: 3px solid #ffd700; }
        .main { margin-left: 250px; padding: 30px; }
        .header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px; }
        .stats { display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin-bottom: 30px; }
        .stat-card { background: linear-gradient(135deg, #1a1a2e, #16213e); padding: 25px; border-radius: 15px; border: 1px solid rgba(255,215,0,0.1); }
        .stat-card h3 { color: #888; font-size: 14px; margin-bottom: 10px; text-transform: uppercase; }
        .stat-card .value { font-size: 32px; font-weight: bold; color: #ffd700; }
        .stat-card .positive { color: #00d084; }
        .stat-card .negative { color: #ff4757; }
        .section { background: #151520; border-radius: 15px; padding: 25px; margin-bottom: 20px; border: 1px solid rgba(255,215,0,0.1); }
        .section h2 { color: #ffd700; margin-bottom: 20px; display: flex; align-items: center; gap: 10px; }
        table { width: 100%; border-collapse: collapse; }
        th { text-align: left; padding: 15px; color: #888; border-bottom: 1px solid rgba(255,215,0,0.1); }
        td { padding: 15px; border-bottom: 1px solid rgba(255,255,255,0.05); }
        .badge { padding: 5px 12px; border-radius: 20px; font-size: 12px; font-weight: bold; }
        .badge-success { background: rgba(0,208,132,0.2); color: #00d084; }
        .badge-warning { background: rgba(255,170,0,0.2); color: #ffaa00; }
        .badge-danger { background: rgba(255,71,87,0.2); color: #ff4757; }
        .btn { padding: 10px 20px; border-radius: 8px; text-decoration: none; display: inline-block; font-weight: bold; }
        .btn-primary { background: linear-gradient(135deg, #ffd700, #ffaa00); color: #0a0a0f; }
        .btn-secondary { background: rgba(255,255,255,0.1); color: #fff; }
        .user-menu { display: flex; align-items: center; gap: 15px; }
        .plan-badge { background: linear-gradient(135deg, #ffd700, #ffaa00); color: #0a0a0f; padding: 5px 15px; border-radius: 20px; font-size: 12px; font-weight: bold; }
        .flash { background: rgba(255,71,87,0.2); border: 1px solid #ff4757; color: #ff4757; padding: 15px; border-radius: 10px; margin-bottom: 20px; }
    </style>
</head>
<body>
    <div class="sidebar">
        <div class="logo">
            <h1>👑 AM Copy Kings</h1>
            <p style="color: #666; font-size: 12px; margin-top: 5px;">Enterprise</p>
        </div>
        <div class="nav">
            <a href="/dashboard" class="active">📊 Dashboard</a>
            <a href="/accounts">💼 Accounts</a>
            <a href="/trades">📈 Trades</a>
            <a href="/api-keys">🔑 API Keys</a>
            <a href="/logout" style="margin-top: 50px; color: #ff4757;">🚪 Logout</a>
        </div>
    </div>
    
    <div class="main">
        <div class="header">
            <div>
                <h2 style="font-size: 28px;">Welcome back, {{ user.username }}!</h2>
                <p style="color: #666; margin-top: 5px;">Here's your trading overview</p>
            </div>
            <div class="user-menu">
                <span class="plan-badge">{{ user.subscription_plan.upper() }}</span>
                <a href="/accounts/add" class="btn btn-primary">+ Add Account</a>
            </div>
        </div>
        
        {% with messages = get_flashed_messages() %}
            {% if messages %}
                {% for message in messages %}
                    <div class="flash">{{ message }}</div>
                {% endfor %}
            {% endif %}
        {% endwith %}
        
        <div class="stats">
            <div class="stat-card">
                <h3>Total P&L</h3>
                <div class="value {% if total_pnl >= 0 %}positive{% else %}negative{% endif %}">
                    ${{ "%.2f"|format(total_pnl) }}
                </div>
            </div>
            <div class="stat-card">
                <h3>Total Trades</h3>
                <div class="value">{{ total_trades }}</div>
            </div>
            <div class="stat-card">
                <h3>Win Rate</h3>
                <div class="value {% if win_rate >= 50 %}positive{% else %}negative{% endif %}">{{ "%.1f"|format(win_rate) }}%</div>
            </div>
            <div class="stat-card">
                <h3>Active Accounts</h3>
                <div class="value">{{ accounts|length }}</div>
            </div>
        </div>
        
        <div class="section">
            <h2>🔴 Open Trades</h2>
            {% if trades %}
            <table>
                <thead>
                    <tr>
                        <th>Symbol</th>
                        <th>Action</th>
                        <th>Entry Price</th>
                        <th>Stop Loss</th>
                        <th>Take Profit</th>
                        <th>R:R Ratio</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody>
                    {% for trade in trades %}
                    <tr>
                        <td><strong>{{ trade.symbol }}</strong></td>
                        <td>
                            <span class="badge {% if trade.action == 'BUY' %}badge-success{% else %}badge-danger{% endif %}">
                                {{ trade.action }}
                            </span>
                        </td>
                        <td>${{ "%.5f"|format(trade.entry_price) if trade.entry_price else 'N/A' }}</td>
                        <td>${{ "%.5f"|format(trade.stop_loss) if trade.stop_loss else 'N/A' }}</td>
                        <td>${{ "%.5f"|format(trade.take_profit) if trade.take_profit else 'N/A' }}</td>
                        <td>{{ trade.risk_reward_ratio }}:1</td>
                        <td><span class="badge badge-warning">OPEN</span></td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
            {% else %}
            <p style="color: #666; text-align: center; padding: 40px;">No open trades. Start trading to see data here.</p>
            {% endif %}
        </div>
        
        <div class="section">
            <h2>💼 Your Accounts</h2>
            <table>
                <thead>
                    <tr>
                        <th>Account Name</th>
                        <th>Type</th>
                        <th>Platform</th>
                        <th>Current Equity</th>
                        <th>Total P&L</th>
                        <th>Win Rate</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody>
                    {% for account in accounts %}
                    <tr>
                        <td><strong>{{ account.account_name }}</strong></td>
                        <td><span class="badge {% if account.account_type == 'master' %}badge-success{% else %}badge-warning{% endif %}">{{ account.account_type.upper() }}</span></td>
                        <td>{{ account.platform }}</td>
                        <td>${{ "%.2f"|format(account.current_equity) }}</td>
                        <td class="{% if account.total_pnl >= 0 %}positive{% else %}negative{% endif %}">${{ "%.2f"|format(account.total_pnl) }}</td>
                        <td>{{ "%.1f"|format((account.winning_trades / account.total_trades * 100) if account.total_trades > 0 else 0) }}%</td>
                        <td>
                            <span class="badge {% if account.is_active %}badge-success{% else %}badge-danger{% endif %}">
                                {{ 'Active' if account.is_active else 'Inactive' }}
                            </span>
                        </td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>
</body>
</html>
"""

ACCOUNTS_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>AM Copy Kings - Accounts</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', Arial; background: #0a0a0f; color: #fff; }
        .sidebar { width: 250px; background: #151520; height: 100vh; position: fixed; border-right: 1px solid rgba(255,215,0,0.1); }
        .logo { padding: 30px; text-align: center; border-bottom: 1px solid rgba(255,215,0,0.1); }
        .logo h1 { color: #ffd700; font-size: 24px; }
        .nav { padding: 20px 0; }
        .nav a { display: block; padding: 15px 30px; color: #888; text-decoration: none; transition: all 0.3s; }
        .nav a:hover, .nav a.active { background: rgba(255,215,0,0.1); color: #ffd700; border-left: 3px solid #ffd700; }
        .main { margin-left: 250px; padding: 30px; }
        .header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px; }
        .btn { padding: 12px 25px; border-radius: 8px; text-decoration: none; display: inline-block; font-weight: bold; }
        .btn-primary { background: linear-gradient(135deg, #ffd700, #ffaa00); color: #0a0a0f; }
        .accounts-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(350px, 1fr)); gap: 20px; }
        .account-card { background: linear-gradient(135deg, #1a1a2e, #16213e); border-radius: 15px; padding: 25px; border: 1px solid rgba(255,215,0,0.1); }
        .account-header { display: flex; justify-content: space-between; align-items: start; margin-bottom: 20px; }
        .account-type { padding: 5px 12px; border-radius: 20px; font-size: 12px; font-weight: bold; }
        .type-master { background: rgba(0,208,132,0.2); color: #00d084; }
        .type-slave { background: rgba(255,170,0,0.2); color: #ffaa00; }
        .account-stats { display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px; margin: 20px 0; }
        .stat { background: rgba(0,0,0,0.2); padding: 15px; border-radius: 10px; }
        .stat-label { color: #888; font-size: 12px; margin-bottom: 5px; }
        .stat-value { font-size: 20px; font-weight: bold; color: #ffd700; }
        .settings { margin-top: 20px; padding-top: 20px; border-top: 1px solid rgba(255,255,255,0.1); }
        .setting-row { display: flex; justify-content: space-between; margin: 10px 0; color: #888; font-size: 14px; }
        .flash { background: rgba(255,71,87,0.2); border: 1px solid #ff4757; color: #ff4757; padding: 15px; border-radius: 10px; margin-bottom: 20px; }
    </style>
</head>
<body>
    <div class="sidebar">
        <div class="logo">
            <h1>👑 AM Copy Kings</h1>
        </div>
        <div class="nav">
            <a href="/dashboard">📊 Dashboard</a>
            <a href="/accounts" class="active">💼 Accounts</a>
            <a href="/trades">📈 Trades</a>
            <a href="/api-keys">🔑 API Keys</a>
            <a href="/logout" style="margin-top: 50px; color: #ff4757;">🚪 Logout</a>
        </div>
    </div>
    
    <div class="main">
        <div class="header">
            <h2 style="font-size: 28px;">Trading Accounts</h2>
            <a href="/accounts/add" class="btn btn-primary">+ Add New Account</a>
        </div>
        
        {% with messages = get_flashed_messages() %}
            {% if messages %}
                {% for message in messages %}
                    <div class="flash">{{ message }}</div>
                {% endfor %}
            {% endif %}
        {% endwith %}
        
        <div class="accounts-grid">
            {% for account in accounts %}
            <div class="account-card">
                <div class="account-header">
                    <div>
                        <h3 style="font-size: 20px; margin-bottom: 5px;">{{ account.account_name }}</h3>
                        <p style="color: #666; font-size: 14px;">{{ account.platform }} • {{ account.broker or 'Unknown Broker' }}</p>
                    </div>
                    <span class="account-type {% if account.account_type == 'master' %}type-master{% else %}type-slave{% endif %}">
                        {{ account.account_type.upper() }}
                    </span>
                </div>
                
                <div class="account-stats">
                    <div class="stat">
                        <div class="stat-label">Current Equity</div>
                        <div class="stat-value">${{ "%.2f"|format(account.current_equity) }}</div>
                    </div>
                    <div class="stat">
                        <div class="stat-label">Total P&L</div>
                        <div class="stat-value {% if account.total_pnl >= 0 %}text-green{% else %}text-red{% endif %}">
                            ${{ "%.2f"|format(account.total_pnl) }}
                        </div>
                    </div>
                    <div class="stat">
                        <div class="stat-label">Total Trades</div>
                        <div class="stat-value">{{ account.total_trades }}</div>
                    </div>
                    <div class="stat">
                        <div class="stat-label">Win Rate</div>
                        <div class="stat-value">{{ "%.1f"|format((account.winning_trades / account.total_trades * 100) if account.total_trades > 0 else 0) }}%</div>
                    </div>
                </div>
                
                <div class="settings">
                    <div class="setting-row">
                        <span>Risk Multiplier:</span>
                        <strong>{{ account.risk_multiplier }}x</strong>
                    </div>
                    <div class="setting-row">
                        <span>Risk Per Trade:</span>
                        <strong>{{ account.risk_percent_per_trade }}%</strong>
                    </div>
                    <div class="setting-row">
                        <span>Min R:R Filter:</span>
                        <strong>{{ account.min_risk_reward_ratio }}:1 {% if account.use_rr_filter %}(Active){% endif %}</strong>
                    </div>
                    <div class="setting-row">
                        <span>Status:</span>
                        <strong style="color: {% if account.is_active %}#00d084{% else %}#ff4757{% endif %};">
                            {{ 'Active' if account.is_active else 'Inactive' }}
                        </strong>
                    </div>
                </div>
            </div>
            {% endfor %}
        </div>
    </div>
</body>
</html>
"""

ADD_ACCOUNT_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>AM Copy Kings - Add Account</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', Arial; background: #0a0a0f; color: #fff; }
        .sidebar { width: 250px; background: #151520; height: 100vh; position: fixed; border-right: 1px solid rgba(255,215,0,0.1); }
        .logo { padding: 30px; text-align: center; border-bottom: 1px solid rgba(255,215,0,0.1); }
        .logo h1 { color: #ffd700; font-size: 24px; }
        .nav { padding: 20px 0; }
        .nav a { display: block; padding: 15px 30px; color: #888; text-decoration: none; transition: all 0.3s; }
        .nav a:hover, .nav a.active { background: rgba(255,215,0,0.1); color: #ffd700; border-left: 3px solid #ffd700; }
        .main { margin-left: 250px; padding: 30px; }
        .form-container { max-width: 600px; background: #151520; padding: 40px; border-radius: 15px; border: 1px solid rgba(255,215,0,0.1); }
        .form-group { margin-bottom: 25px; }
        label { display: block; margin-bottom: 8px; color: #888; font-size: 14px; }
        input, select { width: 100%; padding: 12px; border: 1px solid rgba(255,215,0,0.2); border-radius: 8px; background: #0a0a0f; color: #fff; font-size: 16px; }
        input:focus, select:focus { outline: none; border-color: #ffd700; }
        .checkbox-group { display: flex; align-items: center; gap: 10px; }
        .checkbox-group input { width: auto; }
        .btn { padding: 15px 30px; border-radius: 8px; text-decoration: none; display: inline-block; font-weight: bold; border: none; cursor: pointer; font-size: 16px; }
        .btn-primary { background: linear-gradient(135deg, #ffd700, #ffaa00); color: #0a0a0f; }
        .btn-secondary { background: rgba(255,255,255,0.1); color: #fff; margin-left: 10px; }
        .section-title { color: #ffd700; margin: 30px 0 20px 0; padding-bottom: 10px; border-bottom: 1px solid rgba(255,215,0,0.2); }
    </style>
</head>
<body>
    <div class="sidebar">
        <div class="logo">
            <h1>👑 AM Copy Kings</h1>
        </div>
        <div class="nav">
            <a href="/dashboard">📊 Dashboard</a>
            <a href="/accounts" class="active">💼 Accounts</a>
            <a href="/trades">📈 Trades</a>
            <a href="/api-keys">🔑 API Keys</a>
            <a href="/logout" style="margin-top: 50px; color: #ff4757;">🚪 Logout</a>
        </div>
    </div>
    
    <div class="main">
        <h2 style="font-size: 28px; margin-bottom: 30px;">Add New Trading Account</h2>
        
        <div class="form-container">
            <form method="POST">
                <h3 class="section-title">Account Information</h3>
                
                <div class="form-group">
                    <label>Account Name</label>
                    <input type="text" name="account_name" placeholder="My Master Account" required>
                </div>
                
                <div class="form-group">
                    <label>Account Type</label>
                    <select name="account_type" required>
                        <option value="master">Master (Signal Provider)</option>
                        <option value="slave">Slave (Copy Receiver)</option>
                    </select>
                </div>
                
                <div class="form-group">
                    <label>Platform</label>
                    <select name="platform" required>
                        <option value="MT4">MetaTrader 4</option>
                        <option value="MT5">MetaTrader 5</option>
                        <option value="cTrader">cTrader</option>
                        <option value="TradingView">TradingView</option>
                    </select>
                </div>
                
                <div class="form-group">
                    <label>Broker Name</label>
                    <input type="text" name="broker" placeholder="e.g., IC Markets">
                </div>
                
                <div class="form-group">
                    <label>Starting Equity ($)</label>
                    <input type="number" step="0.01" name="equity" value="10000" required>
                </div>
                
                <h3 class="section-title">Risk Management Settings</h3>
                
                <div class="form-group">
                    <label>Risk Multiplier</label>
                    <input type="number" step="0.1" name="risk_multiplier" value="1.0" required>
                    <small style="color: #666;">Multiply master lot size by this value (e.g., 0.5 for half size)</small>
                </div>
                
                <div class="form-group">
                    <label>Risk Percent Per Trade (%)</label>
                    <input type="number" step="0.1" name="risk_percent" value="2.0" required>
                </div>
                
                <div class="form-group">
                    <label>Minimum Risk:Reward Ratio</label>
                    <input type="number" step="0.1" name="min_rr" value="1.0" required>
                    <small style="color: #666;">Skip trades with R:R below this value</small>
                </div>
                
                <div class="form-group checkbox-group">
                    <input type="checkbox" name="use_rr_filter" id="use_rr_filter">
                    <label for="use_rr_filter" style="margin: 0;">Enable Risk:Reward Filter</label>
                </div>
                
                <div style="margin-top: 30px;">
                    <button type="submit" class="btn btn-primary">Create Account</button>
                    <a href="/accounts" class="btn btn-secondary">Cancel</a>
                </div>
            </form>
        </div>
    </div>
</body>
</html>
"""

TRADES_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>AM Copy Kings - Trade History</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', Arial; background: #0a0a0f; color: #fff; }
        .sidebar { width: 250px; background: #151520; height: 100vh; position: fixed; border-right: 1px solid rgba(255,215,0,0.1); }
        .logo { padding: 30px; text-align: center; border-bottom: 1px solid rgba(255,215,0,0.1); }
        .logo h1 { color: #ffd700; font-size: 24px; }
        .nav { padding: 20px 0; }
        .nav a { display: block; padding: 15px 30px; color: #888; text-decoration: none; transition: all 0.3s; }
        .nav a:hover, .nav a.active { background: rgba(255,215,0,0.1); color: #ffd700; border-left: 3px solid #ffd700; }
        .main { margin-left: 250px; padding: 30px; }
        .header { margin-bottom: 30px; }
        .filters { display: flex; gap: 15px; margin-bottom: 20px; }
        .filter-btn { padding: 10px 20px; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,215,0,0.2); border-radius: 8px; color: #fff; cursor: pointer; }
        .filter-btn.active { background: rgba(255,215,0,0.2); border-color: #ffd700; }
        .trades-table { background: #151520; border-radius: 15px; overflow: hidden; border: 1px solid rgba(255,215,0,0.1); }
        table { width: 100%; border-collapse: collapse; }
        th { text-align: left; padding: 20px; background: rgba(255,215,0,0.05); color: #ffd700; font-weight: 600; }
        td { padding: 20px; border-bottom: 1px solid rgba(255,255,255,0.05); }
        tr:hover { background: rgba(255,255,255,0.02); }
        .badge { padding: 5px 12px; border-radius: 20px; font-size: 12px; font-weight: bold; }
        .badge-buy { background: rgba(0,208,132,0.2); color: #00d084; }
        .badge-sell { background: rgba(255,71,87,0.2); color: #ff4757; }
        .badge-open { background: rgba(255,170,0,0.2); color: #ffaa00; }
        .badge-closed { background: rgba(100,100,100,0.2); color: #888; }
        .profit { color: #00d084; font-weight: bold; }
        .loss { color: #ff4757; font-weight: bold; }
    </style>
</head>
<body>
    <div class="sidebar">
        <div class="logo">
            <h1>👑 AM Copy Kings</h1>
        </div>
        <div class="nav">
            <a href="/dashboard">📊 Dashboard</a>
            <a href="/accounts">💼 Accounts</a>
            <a href="/trades" class="active">📈 Trades</a>
            <a href="/api-keys">🔑 API Keys</a>
            <a href="/logout" style="margin-top: 50px; color: #ff4757;">🚪 Logout</a>
        </div>
    </div>
    
    <div class="main">
        <div class="header">
            <h2 style="font-size: 28px;">Trade History</h2>
            <p style="color: #666; margin-top: 5px;">View all your trading activity</p>
        </div>
        
        <div class="filters">
            <button class="filter-btn active">All Trades</button>
            <button class="filter-btn">Open Only</button>
            <button class="filter-btn">Closed Only</button>
            <button class="filter-btn">Profitable</button>
            <button class="filter-btn">Losses</button>
        </div>
        
        <div class="trades-table">
            <table>
                <thead>
                    <tr>
                        <th>Date</th>
                        <th>Symbol</th>
                        <th>Action</th>
                        <th>Entry Price</th>
                        <th>Exit Price</th>
                        <th>Stop Loss</th>
                        <th>Take Profit</th>
                        <th>R:R</th>
                        <th>P&L</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody>
                    {% for trade in trades %}
                    <tr>
                        <td>{{ trade.opened_at.strftime('%Y-%m-%d %H:%M') }}</td>
                        <td><strong>{{ trade.symbol }}</strong></td>
                        <td>
                            <span class="badge {% if trade.action == 'BUY' %}badge-buy{% else %}badge-sell{% endif %}">
                                {{ trade.action }}
                            </span>
                        </td>
                        <td>${{ "%.5f"|format(trade.entry_price) if trade.entry_price else '-' }}</td>
                        <td>${{ "%.5f"|format(trade.exit_price) if trade.exit_price else '-' }}</td>
                        <td>${{ "%.5f"|format(trade.stop_loss) if trade.stop_loss else '-' }}</td>
                        <td>${{ "%.5f"|format(trade.take_profit) if trade.take_profit else '-' }}</td>
                        <td>{{ trade.risk_reward_ratio }}:1</td>
                        <td class="{% if trade.profit_loss > 0 %}profit{% elif trade.profit_loss < 0 %}loss{% endif %}">
                            {% if trade.profit_loss != 0 %}${{ "%.2f"|format(trade.profit_loss) }}{% else %}-{% endif %}
                        </td>
                        <td>
                            <span class="badge badge-{{ trade.status }}">{{ trade.status.upper() }}</span>
                        </td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>
</body>
</html>
"""

API_KEYS_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>AM Copy Kings - API Keys</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', Arial; background: #0a0a0f; color: #fff; }
        .sidebar { width: 250px; background: #151520; height: 100vh; position: fixed; border-right: 1px solid rgba(255,215,0,0.1); }
        .logo { padding: 30px; text-align: center; border-bottom: 1px solid rgba(255,215,0,0.1); }
        .logo h1 { color: #ffd700; font-size: 24px; }
        .nav { padding: 20px 0; }
        .nav a { display: block; padding: 15px 30px; color: #888; text-decoration: none; transition: all 0.3s; }
        .nav a:hover, .nav a.active { background: rgba(255,215,0,0.1); color: #ffd700; border-left: 3px solid #ffd700; }
        .main { margin-left: 250px; padding: 30px; }
        .header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px; }
        .btn { padding: 12px 25px; border-radius: 8px; text-decoration: none; display: inline-block; font-weight: bold; border: none; cursor: pointer; }
        .btn-primary { background: linear-gradient(135deg, #ffd700, #ffaa00); color: #0a0a0f; }
        .key-card { background: #151520; border-radius: 15px; padding: 25px; margin-bottom: 20px; border: 1px solid rgba(255,215,0,0.1); }
        .key-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; }
        .key-name { font-size: 18px; font-weight: bold; }
        .key-value { background: #0a0a0f; padding: 15px; border-radius: 8px; font-family: monospace; color: #ffd700; word-break: break-all; margin: 15px 0; border: 1px solid rgba(255,215,0,0.2); }
        .key-meta { display: flex; gap: 20px; color: #666; font-size: 14px; margin-top: 15px; }
        .status-active { color: #00d084; }
        .status-inactive { color: #ff4757; }
        .warning-box { background: rgba(255,170,0,0.1); border: 1px solid rgba(255,170,0,0.3); padding: 20px; border-radius: 10px; margin-bottom: 30px; }
        .warning-box h3 { color: #ffaa00; margin-bottom: 10px; }
        code { background: rgba(255,215,0,0.1); padding: 2px 6px; border-radius: 4px; color: #ffd700; }
    </style>
</head>
<body>
    <div class="sidebar">
        <div class="logo">
            <h1>👑 AM Copy Kings</h1>
        </div>
        <div class="nav">
            <a href="/dashboard">📊 Dashboard</a>
            <a href="/accounts">💼 Accounts</a>
            <a href="/trades">📈 Trades</a>
            <a href="/api-keys" class="active">🔑 API Keys</a>
            <a href="/logout" style="margin-top: 50px; color: #ff4757;">🚪 Logout</a>
        </div>
    </div>
    
    <div class="main">
        <div class="header">
            <div>
                <h2 style="font-size: 28px;">API Keys</h2>
                <p style="color: #666; margin-top: 5px;">Manage webhook integration keys</p>
            </div>
            <form method="POST" action="/api-keys/generate" style="display: flex; gap: 10px;">
                <input type="text" name="key_name" placeholder="Key name (e.g., TradingView)" style="padding: 12px; border-radius: 8px; border: 1px solid rgba(255,215,0,0.2); background: #0a0a0f; color: #fff;">
                <button type="submit" class="btn btn-primary">Generate New Key</button>
            </form>
        </div>
        
        <div class="warning-box">
            <h3>⚠️ Webhook Integration</h3>
            <p>Use this endpoint to send trades from TradingView or other platforms:</p>
            <p style="margin-top: 10px; font-family: monospace; color: #ffd700;">
                POST https://yourdomain.com/webhook/<code>YOUR_API_KEY</code>
            </p>
        </div>
        
        {% for key in keys %}
        <div class="key-card">
            <div class="key-header">
                <span class="key-name">{{ key.key_name }}</span>
                <span class="{% if key.is_active %}status-active{% else %}status-inactive{% endif %}">
                    ● {{ 'Active' if key.is_active else 'Inactive' }}
                </span>
            </div>
            <div class="key-value">{{ key.api_key }}</div>
            <div class="key-meta">
                <span>Created: {{ key.created_at.strftime('%Y-%m-%d') }}</span>
                <span>Uses: Unlimited</span>
            </div>
        </div>
        {% endfor %}
    </div>
</body>
</html>
"""

# ==================== ADDITIONAL ROUTES ====================

@app.route('/accounts/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_account(id):
    account = TradingAccount.query.get_or_404(id)
    if account.user_id != current_user.id:
        flash('Unauthorized')
        return redirect('/accounts')
    
    if request.method == 'POST':
        account.account_name = request.form.get('account_name')
        account.risk_multiplier = float(request.form.get('risk_multiplier', 1.0))
        account.risk_percent_per_trade = float(request.form.get('risk_percent', 2.0))
        account.min_risk_reward_ratio = float(request.form.get('min_rr', 1.0))
        account.use_rr_filter = bool(request.form.get('use_rr_filter'))
        account.is_active = bool(request.form.get('is_active'))
        
        db.session.commit()
        flash('Account updated!')
        return redirect('/accounts')
    
    return render_template_string(EDIT_ACCOUNT_HTML, account=account)

@app.route('/accounts/toggle/<int:id>')
@login_required
def toggle_account(id):
    account = TradingAccount.query.get_or_404(id)
    if account.user_id != current_user.id:
        flash('Unauthorized')
        return redirect('/accounts')
    
    account.is_active = not account.is_active
    db.session.commit()
    flash(f'Account {"activated" if account.is_active else "deactivated"}!')
    return redirect('/accounts')

@app.route('/webhook-test')
@login_required
def webhook_test():
    """Test page for webhook integration"""
    return render_template_string(WEBHOOK_TEST_HTML, user=current_user)

# ==================== MISSING TEMPLATES ====================

EDIT_ACCOUNT_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Edit Account - AM Copy Kings</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', Arial; background: #0a0a0f; color: #fff; }
        .sidebar { width: 250px; background: #151520; height: 100vh; position: fixed; }
        .main { margin-left: 250px; padding: 30px; }
        .form-container { max-width: 600px; background: #151520; padding: 40px; border-radius: 15px; border: 1px solid rgba(255,215,0,0.1); }
        .form-group { margin-bottom: 25px; }
        label { display: block; margin-bottom: 8px; color: #888; }
        input, select { width: 100%; padding: 12px; border: 1px solid rgba(255,215,0,0.2); border-radius: 8px; background: #0a0a0f; color: #fff; }
        .btn { padding: 15px 30px; border-radius: 8px; border: none; cursor: pointer; font-weight: bold; }
        .btn-primary { background: linear-gradient(135deg, #ffd700, #ffaa00); color: #0a0a0f; }
        .btn-secondary { background: rgba(255,255,255,0.1); color: #fff; margin-left: 10px; }
    </style>
</head>
<body>
    <div class="main">
        <h2 style="margin-bottom: 30px;">Edit Account: {{ account.account_name }}</h2>
        <div class="form-container">
            <form method="POST">
                <div class="form-group">
                    <label>Account Name</label>
                    <input type="text" name="account_name" value="{{ account.account_name }}" required>
                </div>
                <div class="form-group">
                    <label>Risk Multiplier</label>
                    <input type="number" step="0.1" name="risk_multiplier" value="{{ account.risk_multiplier }}" required>
                </div>
                <div class="form-group">
                    <label>Risk % Per Trade</label>
                    <input type="number" step="0.1" name="risk_percent" value="{{ account.risk_percent_per_trade }}" required>
                </div>
                <div class="form-group">
                    <label>Min Risk:Reward</label>
                    <input type="number" step="0.1" name="min_rr" value="{{ account.min_risk_reward_ratio }}" required>
                </div>
                <div class="form-group">
                    <label>
                        <input type="checkbox" name="use_rr_filter" {% if account.use_rr_filter %}checked{% endif %}>
                        Enable R:R Filter
                    </label>
                </div>
                <div class="form-group">
                    <label>
                        <input type="checkbox" name="is_active" {% if account.is_active %}checked{% endif %}>
                        Account Active
                    </label>
                </div>
                <button type="submit" class="btn btn-primary">Save Changes</button>
                <a href="/accounts" class="btn btn-secondary">Cancel</a>
            </form>
        </div>
    </div>
</body>
</html>
"""

WEBHOOK_TEST_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Webhook Test - AM Copy Kings</title>
    <style>
        body { font-family: Arial; background: #0a0a0f; color: #fff; padding: 40px; }
        .container { max-width: 800px; margin: 0 auto; }
        pre { background: #151520; padding: 20px; border-radius: 10px; overflow-x: auto; color: #00d084; }
        code { color: #ffd700; }
        .section { background: #151520; padding: 30px; border-radius: 15px; margin: 20px 0; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔌 Webhook Integration Test</h1>
        
        <div class="section">
            <h2>Your Webhook URL</h2>
            <pre>https://yourdomain.com/webhook/<code>YOUR_API_KEY_HERE</code></pre>
        </div>
        
        <div class="section">
            <h2>Example Payload (Open Trade)</h2>
            <pre>{
  "action": "OPEN",
  "symbol": "EURUSD",
  "direction": "BUY",
  "entry_price": 1.0850,
  "stop_loss": 1.0800,
  "take_profit": 1.0950,
  "lot_size": 0.1,
  "magic_number": "123456"
}</pre>
        </div>
        
        <div class="section">
            <h2>Example Payload (Close Trade)</h2>
            <pre>{
  "action": "CLOSE",
  "magic_number": "123456",
  "exit_price": 1.0900,
  "profit": 50.00
}</pre>
        </div>
        
        <p>Get your API key from the <a href="/api-keys" style="color: #ffd700;">API Keys page</a></p>
    </div>
</body>
</html>
"""

# ==================== INITIALIZATION ====================

def init_db():
    with app.app_context():
        db.create_all()
        print("Database initialized!")

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)