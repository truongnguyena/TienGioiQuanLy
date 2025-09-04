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
    # Simple cultivation system with bounds checking
    base_gain = random.randint(50, 200)
    
    # Prevent integer overflow
    if current_user.spiritual_power > 999999999 - base_gain:
        base_gain = min(base_gain, 999999999 - current_user.spiritual_power)
    
    current_user.spiritual_power += base_gain
    current_user.cultivation_points += base_gain // 10
    current_user.last_cultivation = datetime.utcnow()
    
    # Check for level up using detailed stage system
    current_level = current_user.cultivation_level
    stage_info = cultivation_ai.cultivation_stages.get(current_level)
    
    if stage_info and current_user.spiritual_power >= stage_info["max_power"]:
        # Determine next level
        current_stage = current_user.get_cultivation_stage()
        current_substage = current_user.get_cultivation_substage()
        
        new_level = None
        achievement_type = "common"
        
        if "Viên Mãn" in current_level:
            # Advance to next major stage
            major_stages = ["Luyện Khí", "Trúc Cơ", "Kết Đan", "Nguyên Anh", "Hóa Thần",
                           "Luyện Hư", "Hợp Thể", "Đại Thừa", "Độ Kiếp", "Tản Tiên"]
            try:
                current_major_index = major_stages.index(current_stage)
                if current_major_index < len(major_stages) - 1:
                    next_major_stage = major_stages[current_major_index + 1]
                    new_level = f"{next_major_stage} Tầng 1"
                    achievement_type = "legendary"
            except ValueError:
                pass
        elif "Tầng" in current_level:
            # Advance within current major stage
            for i in range(1, 9):
                if f"Tầng {i}" in current_level:
                    if i < 9:
                        new_level = current_level.replace(f"Tầng {i}", f"Tầng {i+1}")
                    else:
                        new_level = current_level.replace(f"Tầng {i}", "Viên Mãn")
                        achievement_type = "rare"
                    break
        
        if new_level and new_level in cultivation_ai.cultivation_stages:
            old_level = current_user.cultivation_level
            current_user.cultivation_level = new_level
            
            # Add achievement
            if achievement_type == "legendary":
                title = f"Đại Đột Phá {current_stage}"
                description = f"Viên mãn {current_stage}, đột phá lên {current_user.get_cultivation_stage()}"
            elif achievement_type == "rare":
                title = f"Viên Mãn {current_stage}"
                description = f"Đạt tới viên mãn cảnh giới {current_stage}"
            else:
                title = f"Tiến Bộ {current_stage}"
                description = f"Từ {old_level} lên {new_level}"
            
            achievement = Achievement(
                user_id=current_user.id,
                title=title,
                description=description,
                category="cultivation",
                rarity=achievement_type
            )
            db.session.add(achievement)
    
    db.session.commit()
    
    return jsonify({
        'success': True,
        'power_gained': base_gain,
        'new_total': current_user.spiritual_power,
        'cultivation_level': current_user.cultivation_level
    })

@app.route('/api/mine-stones', methods=['POST'])
@login_required
def mine_stones():
    # Admin users can mine without cooldown
    if not current_user.is_admin:
        # Check if user can mine (every 2 hours)
        if current_user.last_mining:
            time_diff = datetime.utcnow() - current_user.last_mining
            if time_diff.total_seconds() < 7200:  # 2 hours cooldown
                remaining = 7200 - time_diff.total_seconds()
                return jsonify({
                    'success': False, 
                    'error': f'Còn {int(remaining//60)} phút nữa mới có thể đào tiếp!',
                    'cooldown': remaining
                })
    
    # Calculate mining yield based on level
    base_yield = 50 + (current_user.mining_level * 25)
    mining_bonus = random.randint(0, current_user.mining_level * 10)
    total_yield = base_yield + mining_bonus
    
    # Add stones to user
    current_user.spiritual_stones += total_yield
    current_user.mining_experience += 10
    current_user.last_mining = datetime.utcnow()
    
    # Check for mining level up
    level_up = False
    if current_user.mining_experience >= (current_user.mining_level * 100):
        current_user.mining_level += 1
        current_user.mining_experience = 0
        level_up = True
    
    db.session.commit()
    
    return jsonify({
        'success': True,
        'stones_mined': total_yield,
        'new_total': current_user.spiritual_stones,
        'mining_level': current_user.mining_level,
        'mining_exp': current_user.mining_experience,
        'level_up': level_up
    })

@app.route('/api/create-world-free', methods=['POST'])
@login_required  
def create_world_free():
    if current_user.free_world_opening_used:
        return jsonify({'success': False, 'error': 'Bạn đã sử dụng lượt mở thế giới miễn phí rồi!'})
    
    # Validate JSON request
    if not request.json:
        return jsonify({'success': False, 'error': 'Dữ liệu JSON không hợp lệ!'})
    
    name = request.json.get('name')
    world_type = request.json.get('world_type', 'Linh Giới')
    description = request.json.get('description', '')
    
    if not name or len(name) < 3:
        return jsonify({'success': False, 'error': 'Tên thế giới phải có ít nhất 3 ký tự!'})
    
    # Create the world
    world = World(
        name=name,
        world_type=world_type,
        description=description,
        owner_id=current_user.id,
        spiritual_density=random.randint(40, 80),
        danger_level=random.randint(1, 3),
        resource_richness=random.randint(30, 70),
        spiritual_stones_production=random.randint(100, 300)
    )
    
    # Mark free opening as used
    current_user.free_world_opening_used = True
    
    try:
        db.session.add(world)
        db.session.commit()
        
        return jsonify({
            'success': True, 
            'message': f'Đã tạo thế giới "{name}" thành công!',
            'world': {
                'id': world.id,
                'name': world.name,
                'type': world.world_type,
                'spiritual_density': world.spiritual_density,
                'production': world.spiritual_stones_production
            }
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': 'Lỗi khi tạo thế giới. Vui lòng thử lại!'})

@app.route('/api/explore-world/<int:world_id>', methods=['POST'])
@login_required
def explore_world(world_id):
    world = World.query.get_or_404(world_id)
    
    # Check if user owns the world
    if world.owner_id != current_user.id:
        return jsonify({'success': False, 'error': 'Bạn không sở hữu thế giới này!'})
    
    # Check energy requirement
    energy_cost = world.danger_level * 50
    if current_user.spiritual_power < energy_cost:
        return jsonify({'success': False, 'error': f'Cần {energy_cost} linh lực để khám phá!'})
    
    # Deduct energy
    current_user.spiritual_power -= energy_cost
    
    # Calculate rewards based on world properties
    base_stones = world.spiritual_stones_production // 10
    bonus_stones = random.randint(base_stones, base_stones * 2)
    
    # Chance for rare materials
    rare_chance = (world.resource_richness + world.spiritual_density) / 200
    found_rare = random.random() < rare_chance
    rare_materials = random.randint(1, 3) if found_rare else 0
    
    # Update rewards
    current_user.spiritual_stones += bonus_stones
    if found_rare:
        world.rare_materials_count += rare_materials
    
    # Update exploration timestamp
    from datetime import datetime
    world.last_explored = datetime.utcnow()
    
    db.session.commit()
    
    rewards = {
        'spiritual_stones': bonus_stones,
        'rare_materials': rare_materials,
        'energy_cost': energy_cost
    }
    
    return jsonify({
        'success': True,
        'message': 'Khám phá thành công!',
        'rewards': rewards
    })

@app.route('/api/upgrade-world/<int:world_id>', methods=['POST'])
@login_required
def upgrade_world(world_id):
    world = World.query.get_or_404(world_id)
    
    # Check if user owns the world
    if world.owner_id != current_user.id:
        return jsonify({'success': False, 'error': 'Bạn không sở hữu thế giới này!'})
    
    # Validate JSON request
    if not request.json:
        return jsonify({'success': False, 'error': 'Dữ liệu JSON không hợp lệ!'})
    
    upgrade_type = request.json.get('upgrade_type')
    
    # Calculate upgrade cost
    base_cost = 5000
    level_multiplier = (world.spiritual_density + world.resource_richness + world.danger_level) // 10
    upgrade_cost = base_cost * (level_multiplier + 1)
    
    if current_user.spiritual_stones < upgrade_cost:
        return jsonify({'success': False, 'error': f'Cần {upgrade_cost} linh thạch để nâng cấp!'})
    
    # Apply upgrade
    if upgrade_type == 'spiritual_density':
        if world.spiritual_density >= 100:
            return jsonify({'success': False, 'error': 'Mật độ linh khí đã đạt tối đa!'})
        world.spiritual_density = min(100, world.spiritual_density + 10)
        upgrade_name = 'Mật Độ Linh Khí'
    elif upgrade_type == 'resource_richness':
        if world.resource_richness >= 100:
            return jsonify({'success': False, 'error': 'Độ phong phú tài nguyên đã đạt tối đa!'})
        world.resource_richness = min(100, world.resource_richness + 10)
        upgrade_name = 'Độ Phong Phú Tài Nguyên'
    elif upgrade_type == 'production':
        world.spiritual_stones_production += 50
        upgrade_name = 'Sản Xuất Linh Thạch'
    else:
        return jsonify({'success': False, 'error': 'Loại nâng cấp không hợp lệ!'})
    
    # Deduct cost
    current_user.spiritual_stones -= upgrade_cost
    
    try:
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'Nâng cấp {upgrade_name} thành công!',
            'upgrade_cost': upgrade_cost,
            'world': {
                'spiritual_density': world.spiritual_density,
                'resource_richness': world.resource_richness,
                'production': world.spiritual_stones_production
            }
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': 'Lỗi khi nâng cấp. Vui lòng thử lại!'})

@app.route('/mining')
@login_required
def mining():
    return render_template('mining.html')

@app.route('/api/send-message', methods=['POST'])
@login_required
def send_message():
    # Validate JSON request
    if not request.json:
        return jsonify({'success': False, 'error': 'Dữ liệu JSON không hợp lệ!'})
    
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
    
    # Validate JSON request
    if not request.json:
        return jsonify({'success': False, 'error': 'Dữ liệu JSON không hợp lệ!'})
    
    name = request.json.get('name')
    description = request.json.get('description', '')
    
    if not name or len(name) < 3:
        return jsonify({'success': False, 'error': 'Tên bang hội phải có ít nhất 3 ký tự!'})
    
    if Guild.query.filter_by(name=name).first():
        return jsonify({'success': False, 'error': 'Tên bang hội đã tồn tại!'})
    
    # Check cost (admin users get free guild creation)
    guild_cost = 10000  # spiritual stones
    if not current_user.is_admin and current_user.spiritual_stones < guild_cost:
        return jsonify({'success': False, 'error': f'Cần {guild_cost} linh thạch để tạo bang hội!'})
    
    guild = Guild(
        name=name,
        description=description,
        leader_id=current_user.id
    )
    
    # Admin users don't pay the cost
    if not current_user.is_admin:
        current_user.spiritual_stones -= guild_cost
    
    try:
        db.session.add(guild)
        db.session.commit()
        
        # Update user's guild
        current_user.guild_id = guild.id
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Tạo bang hội thành công!'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': 'Lỗi khi tạo bang hội. Vui lòng thử lại!'})

@app.route('/api/create-expedition', methods=['POST'])
@login_required
def create_expedition():
    # Validate JSON request
    if not request.json:
        return jsonify({'success': False, 'error': 'Dữ liệu JSON không hợp lệ!'})
    
    data = request.json
    
    name = data.get('name')
    destination = data.get('destination')
    description = data.get('description', '')
    
    if not name or len(name) < 3:
        return jsonify({'success': False, 'error': 'Tên đạo lữ phải có ít nhất 3 ký tự!'})
    
    if not destination:
        return jsonify({'success': False, 'error': 'Điểm đến không được để trống!'})
    
    # Check cost (admin users get free expedition creation)
    expedition_cost = 5000  # spiritual stones
    if not current_user.is_admin and current_user.spiritual_stones < expedition_cost:
        return jsonify({'success': False, 'error': f'Cần {expedition_cost} linh thạch để tạo đạo lữ!'})
    
    expedition = Expedition(
        name=name,
        destination=destination,
        description=description,
        difficulty_level=max(1, min(5, int(data.get('difficulty_level', 1)))),
        max_participants=max(1, min(10, int(data.get('max_participants', 5)))),
        duration_hours=max(1, min(168, int(data.get('duration_hours', 24)))),
        min_cultivation=data.get('min_cultivation'),
        required_items=data.get('required_items'),
        potential_rewards=data.get('potential_rewards'),
        organizer_guild_id=current_user.guild_id
    )
    
    # Admin users don't pay the cost
    if not current_user.is_admin:
        current_user.spiritual_stones -= expedition_cost
    
    try:
        # Validate integer fields before database insert
        if not isinstance(expedition.difficulty_level, int) or not isinstance(expedition.max_participants, int):
            return jsonify({'success': False, 'error': 'Dữ liệu số không hợp lệ!'})
            
        db.session.add(expedition)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Tạo đạo lữ thành công!'})
    except (ValueError, TypeError) as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': 'Dữ liệu đầu vào không hợp lệ!'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': 'Lỗi khi tạo đạo lữ. Vui lòng thử lại!'})

@app.route('/api/get-messages', methods=['GET'])
@login_required  
def get_messages():
    channel = request.args.get('channel', 'general')
    channel_id = request.args.get('channel_id')
    
    query = ChatMessage.query.filter_by(channel=channel)
    if channel_id:
        query = query.filter_by(channel_id=channel_id)
    
    messages = query.order_by(ChatMessage.created_at.desc()).limit(20).all()
    
    message_list = []
    for msg in messages:
        message_list.append({
            'id': msg.id,
            'content': msg.content,
            'user_id': msg.user_id,
            'user_name': msg.user.dao_name or msg.user.username,
            'created_at': msg.created_at.isoformat()
        })
    
    return jsonify({'success': True, 'messages': message_list})


