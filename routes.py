from flask import render_template, request, redirect, url_for, flash, jsonify, session
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import json
import random

from app import app, db
from models import User, Guild, World, GuildWar, Expedition, ExpeditionParticipant, ChatMessage, Achievement
from ai_helper import cultivation_ai

@app.route('/')
def index():
    # Get some statistics for the homepage
    stats = {
        'total_users': User.query.count(),
        'total_guilds': Guild.query.count(),
        'total_worlds': World.query.count(),
        'active_expeditions': Expedition.query.filter_by(status='Đang Diễn Ra').count()
    }
    
    # Recent activities
    recent_achievements = Achievement.query.order_by(Achievement.earned_at.desc()).limit(5).all()
    
    return render_template('index.html', stats=stats, recent_achievements=recent_achievements)

@app.route('/auth', methods=['GET', 'POST'])
def auth():
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'login':
            username = request.form.get('username')
            password = request.form.get('password')
            
            user = User.query.filter_by(username=username).first()
            
            if user and user.check_password(password):
                login_user(user)
                flash('Đăng nhập thành công!', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Tên đăng nhập hoặc mật khẩu không đúng!', 'error')
        
        elif action == 'register':
            username = request.form.get('username')
            email = request.form.get('email')
            password = request.form.get('password')
            dao_name = request.form.get('dao_name', '')
            
            if User.query.filter_by(username=username).first():
                flash('Tên đăng nhập đã tồn tại!', 'error')
            elif User.query.filter_by(email=email).first():
                flash('Email đã được sử dụng!', 'error')
            else:
                user = User(username=username, email=email, dao_name=dao_name)
                user.set_password(password)
                db.session.add(user)
                db.session.commit()
                
                flash('Đăng ký thành công! Hãy đăng nhập.', 'success')
                return redirect(url_for('auth'))
    
    return render_template('auth.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Đã đăng xuất thành công!', 'info')
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    # AI predictions and advice
    fortune = cultivation_ai.predict_cultivation_fortune(current_user)
    advice = cultivation_ai.get_cultivation_advice(current_user)
    weather = cultivation_ai.get_weather_forecast()
    
    # User's guild info
    guild = current_user.guild
    
    # Recent activities
    recent_messages = ChatMessage.query.filter_by(channel='general').order_by(ChatMessage.created_at.desc()).limit(10).all()
    
    # Available expeditions
    available_expeditions = Expedition.query.filter_by(status='Tuyển Thành Viên').limit(5).all()
    
    return render_template('dashboard.html', 
                         fortune=fortune, 
                         advice=advice, 
                         weather=weather,
                         guild=guild,
                         recent_messages=recent_messages,
                         available_expeditions=available_expeditions)

@app.route('/world-management')
@login_required
def world_management():
    owned_worlds = current_user.owned_worlds
    available_worlds = World.query.filter_by(owner_id=None).all()
    contested_worlds = World.query.filter_by(is_contested=True).all()
    
    return render_template('world_management.html', 
                         owned_worlds=owned_worlds,
                         available_worlds=available_worlds,
                         contested_worlds=contested_worlds)

@app.route('/guild-management')
@login_required
def guild_management():
    user_guild = current_user.guild
    all_guilds = Guild.query.all()
    
    # Guild wars
    active_wars = GuildWar.query.filter_by(status='Đang Diễn Ra').all()
    
    # War predictions if user is guild leader
    war_predictions = []
    if user_guild and user_guild.leader_id == current_user.id:
        for guild in all_guilds:
            if guild.id != user_guild.id:
                prediction = cultivation_ai.calculate_guild_war_prediction(user_guild, guild)
                prediction['target_guild'] = guild
                war_predictions.append(prediction)
    
    return render_template('guild_management.html',
                         user_guild=user_guild,
                         all_guilds=all_guilds,
                         active_wars=active_wars,
                         war_predictions=war_predictions)

@app.route('/expeditions')
@login_required
def expeditions():
    available_expeditions = Expedition.query.filter_by(status='Tuyển Thành Viên').all()
    active_expeditions = Expedition.query.filter_by(status='Đang Diễn Ra').all()
    user_expeditions = Expedition.query.join(ExpeditionParticipant).filter(ExpeditionParticipant.user_id == current_user.id).all()
    
    return render_template('expeditions.html',
                         available_expeditions=available_expeditions,
                         active_expeditions=active_expeditions,
                         user_expeditions=user_expeditions)

@app.route('/rankings')
@login_required
def rankings():
    # Different ranking categories
    power_rankings = User.query.order_by(User.spiritual_power.desc()).limit(50).all()
    reputation_rankings = User.query.order_by(User.reputation.desc()).limit(50).all()
    guild_rankings = Guild.query.order_by(Guild.level.desc(), Guild.experience.desc()).limit(30).all()
    
    # Weekly achievements
    week_ago = datetime.now() - timedelta(days=7)
    recent_achievements = Achievement.query.filter(Achievement.earned_at >= week_ago).order_by(Achievement.earned_at.desc()).all()
    
    return render_template('rankings.html',
                         power_rankings=power_rankings,
                         reputation_rankings=reputation_rankings,
                         guild_rankings=guild_rankings,
                         recent_achievements=recent_achievements)

@app.route('/community')
@login_required
def community():
    # Recent messages from different channels
    general_messages = ChatMessage.query.filter_by(channel='general').order_by(ChatMessage.created_at.desc()).limit(20).all()
    
    guild_messages = []
    if current_user.guild_id:
        guild_messages = ChatMessage.query.filter_by(channel='guild', channel_id=current_user.guild_id).order_by(ChatMessage.created_at.desc()).limit(20).all()
    
    return render_template('community.html',
                         general_messages=general_messages,
                         guild_messages=guild_messages)

@app.route('/profile')
@login_required
def profile():
    user_achievements = current_user.achievements
    user_expeditions = Expedition.query.join(ExpeditionParticipant).filter(ExpeditionParticipant.user_id == current_user.id).all()
    
    return render_template('profile.html',
                         user_achievements=user_achievements,
                         user_expeditions=user_expeditions)

# API Routes
@app.route('/api/cultivate', methods=['POST'])
@login_required
def cultivate():
    # Simple cultivation system
    base_gain = random.randint(50, 200)
    current_user.spiritual_power += base_gain
    current_user.cultivation_points += base_gain // 10
    current_user.last_cultivation = datetime.utcnow()
    
    # Check for level up
    current_stage = current_user.get_cultivation_stage()
    stage_info = cultivation_ai.cultivation_stages.get(current_stage)
    
    if current_user.spiritual_power >= stage_info["max_power"]:
        # Level up logic
        next_stages = list(cultivation_ai.cultivation_stages.keys())
        current_index = next_stages.index(current_stage)
        if current_index < len(next_stages) - 1:
            new_stage = next_stages[current_index + 1]
            current_user.cultivation_level = f"{new_stage} Tầng 1"
            
            # Add achievement
            achievement = Achievement(
                user_id=current_user.id,
                title=f"Đột Phá {new_stage}",
                description=f"Thành công đột phá lên cảnh giới {new_stage}",
                category="cultivation",
                rarity="rare" if current_index > 5 else "common"
            )
            db.session.add(achievement)
    
    db.session.commit()
    
    return jsonify({
        'success': True,
        'power_gained': base_gain,
        'new_total': current_user.spiritual_power,
        'cultivation_level': current_user.cultivation_level
    })

@app.route('/api/send-message', methods=['POST'])
@login_required
def send_message():
    content = request.json.get('content')
    channel = request.json.get('channel', 'general')
    channel_id = request.json.get('channel_id')
    
    if not content or len(content) > 500:
        return jsonify({'success': False, 'error': 'Nội dung tin nhắn không hợp lệ'})
    
    message = ChatMessage(
        user_id=current_user.id,
        content=content,
        channel=channel,
        channel_id=channel_id
    )
    
    db.session.add(message)
    db.session.commit()
    
    return jsonify({'success': True})

@app.route('/api/join-expedition/<int:expedition_id>', methods=['POST'])
@login_required
def join_expedition(expedition_id):
    expedition = Expedition.query.get_or_404(expedition_id)
    
    # Check if already joined
    existing = ExpeditionParticipant.query.filter_by(
        expedition_id=expedition_id,
        user_id=current_user.id
    ).first()
    
    if existing:
        return jsonify({'success': False, 'error': 'Bạn đã tham gia đạo lữ này rồi!'})
    
    # Check requirements
    if len(expedition.participants) >= expedition.max_participants:
        return jsonify({'success': False, 'error': 'Đạo lữ đã đủ thành viên!'})
    
    participant = ExpeditionParticipant(
        expedition_id=expedition_id,
        user_id=current_user.id
    )
    
    db.session.add(participant)
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Tham gia đạo lữ thành công!'})

@app.route('/api/create-guild', methods=['POST'])
@login_required
def create_guild():
    if current_user.guild_id:
        return jsonify({'success': False, 'error': 'Bạn đã có bang hội rồi!'})
    
    name = request.json.get('name')
    description = request.json.get('description', '')
    
    if not name or len(name) < 3:
        return jsonify({'success': False, 'error': 'Tên bang hội phải có ít nhất 3 ký tự!'})
    
    if Guild.query.filter_by(name=name).first():
        return jsonify({'success': False, 'error': 'Tên bang hội đã tồn tại!'})
    
    # Check cost
    guild_cost = 10000  # spiritual stones
    if current_user.spiritual_stones < guild_cost:
        return jsonify({'success': False, 'error': f'Cần {guild_cost} linh thạch để tạo bang hội!'})
    
    guild = Guild(
        name=name,
        description=description,
        leader_id=current_user.id
    )
    
    current_user.spiritual_stones -= guild_cost
    db.session.add(guild)
    db.session.commit()
    
    # Update user's guild
    current_user.guild_id = guild.id
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Tạo bang hội thành công!'})

@app.route('/api/get-messages/<channel>')
@login_required
def get_messages(channel):
    query = ChatMessage.query.filter_by(channel=channel)
    
    if channel == 'guild' and current_user.guild_id:
        query = query.filter_by(channel_id=current_user.guild_id)
    
    messages = query.order_by(ChatMessage.created_at.desc()).limit(50).all()
    
    return jsonify([{
        'id': msg.id,
        'username': msg.user.username,
        'dao_name': msg.user.dao_name or msg.user.username,
        'content': msg.content,
        'created_at': msg.created_at.strftime('%H:%M:%S')
    } for msg in messages])
