# Added guild management APIs for settings, war declarations, and member recruitment.
from flask import render_template, request, redirect, url_for, flash, jsonify, session
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import json
import random

from app import app, db, cache
from models import User, Guild, World, GuildWar, Expedition, ExpeditionParticipant, ChatMessage, Achievement
from db_optimizer import DatabaseOptimizer
from ai_helper import cultivation_ai

# Import Perplexity AI helper
try:
    from perplexity_helper import perplexity_manager
    PERPLEXITY_AVAILABLE = True
except ImportError:
    perplexity_manager = None
    PERPLEXITY_AVAILABLE = False
except Exception as e:
    print(f"Perplexity AI not available: {e}")
    perplexity_manager = None
    PERPLEXITY_AVAILABLE = False

@app.route('/')
@cache.cached(timeout=300)  # Cache for 5 minutes
def index():
    # Get optimized statistics using DatabaseOptimizer
    user_stats = DatabaseOptimizer.get_user_stats()
    guild_stats = DatabaseOptimizer.get_guild_stats()
    world_stats = DatabaseOptimizer.get_world_stats()
    
    stats = {
        'total_users': user_stats['total_users'],
        'total_guilds': guild_stats['total_guilds'],
        'total_worlds': world_stats['total_worlds'],
        'active_expeditions': Expedition.query.filter_by(status='Đang Diễn Ra').count()
    }

    # Get recent achievements with caching
    recent_achievements = DatabaseOptimizer.get_recent_achievements(5)

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
                           "Luyện Hư", "Hợp Thể", "Đại Thừa", "Độ Kiếp", "Tản Tiên", "Toàn Chi Thiên Đạo"]
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
    upgrade_cost = world.get_upgrade_cost(upgrade_type)

    if current_user.spiritual_stones < upgrade_cost:
        return jsonify({'success': False, 'error': f'Cần {upgrade_cost} linh thạch để nâng cấp!'})

    # Apply upgrade based on type
    upgrade_name = ''
    upgrade_success = True
    
    try:
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
            
        elif upgrade_type == 'world_level':
            world.world_level += 1
            world.world_experience = 0
            world.population_limit += 50
            world.daily_income += world.world_level * 100
            upgrade_name = f'Cấp Thế Giới (Lv.{world.world_level})'
            
        elif upgrade_type == 'barrier_strength':
            if world.barrier_strength >= 100:
                return jsonify({'success': False, 'error': 'Kết giới đã đạt tối đa!'})
            world.barrier_strength = min(100, world.barrier_strength + 15)
            upgrade_name = 'Sức Mạnh Kết Giới'
            
        elif upgrade_type == 'guardian_level':
            world.guardian_level += 1
            world.successful_defenses += world.guardian_level
            upgrade_name = f'Thủ Hộ Thần (Lv.{world.guardian_level})'
            
        elif upgrade_type == 'cultivation_bonus':
            world.cultivation_bonus = min(3.0, world.cultivation_bonus + 0.2)
            world.breakthrough_chance = min(0.5, world.breakthrough_chance + 0.05)
            upgrade_name = 'Bonus Tu Luyện'
            
        elif upgrade_type == 'market_level':
            world.market_level += 1
            world.trade_routes += 2
            world.daily_income += world.market_level * 200
            upgrade_name = f'Chợ Búa (Lv.{world.market_level})'
            
        elif upgrade_type == 'infrastructure':
            world.infrastructure_level += 1
            world.development_level = min(10, world.development_level + 1)
            world.population_limit += 100
            upgrade_name = f'Cơ Sở Hạ Tầng (Lv.{world.infrastructure_level})'
            
        elif upgrade_type == 'climate_control':
            world.climate_control = min(10, world.climate_control + 1)
            world.ecosystem_diversity = min(10, world.ecosystem_diversity + 1)
            upgrade_name = 'Kiểm Soát Khí Hậu'
            
        elif upgrade_type == 'enlightenment_spots':
            world.enlightenment_spots += 1
            world.cultivation_bonus += 0.1
            upgrade_name = 'Điểm Ngộ Đạo'
            
        elif upgrade_type == 'dimensional_gate':
            if world.dimensional_gate:
                return jsonify({'success': False, 'error': 'Cổng không gian đã được kích hoạt!'})
            world.dimensional_gate = True
            world.trade_routes += 10
            upgrade_name = 'Cổng Không Gian'
            
        elif upgrade_type == 'time_acceleration':
            if world.time_acceleration:
                return jsonify({'success': False, 'error': 'Tăng tốc thời gian đã được kích hoạt!'})
            world.time_acceleration = True
            world.time_flow_rate = 2.0
            world.cultivation_bonus += 0.5
            upgrade_name = 'Tăng Tốc Thời Gian'
            
        elif upgrade_type == 'auto_cultivation':
            if world.auto_cultivation:
                return jsonify({'success': False, 'error': 'Tự động tu luyện đã được kích hoạt!'})
            world.auto_cultivation = True
            world.cultivation_bonus += 1.0
            upgrade_name = 'Tự Động Tu Luyện'
            
        elif upgrade_type == 'resource_multiplication':
            if world.resource_multiplication:
                return jsonify({'success': False, 'error': 'Nhân tài nguyên đã được kích hoạt!'})
            world.resource_multiplication = True
            world.spiritual_stones_production *= 2
            world.daily_income *= 2
            upgrade_name = 'Nhân Tài Nguyên'
            
        else:
            return jsonify({'success': False, 'error': 'Loại nâng cấp không hợp lệ!'})

        # Deduct cost and update world stats
        current_user.spiritual_stones -= upgrade_cost
        world.total_upgrades += 1
        world.last_upgraded = datetime.utcnow()
        world.world_experience += 100

        # Check for world level up
        required_exp = world.world_level * 500
        if world.world_experience >= required_exp:
            world.world_level += 1
            world.world_experience = 0
            world.stability = min(100, world.stability + 10)

        db.session.commit()

        return jsonify({
            'success': True,
            'message': f'Nâng cấp {upgrade_name} thành công!',
            'upgrade_cost': upgrade_cost,
            'world': {
                'world_level': world.world_level,
                'spiritual_density': world.spiritual_density,
                'resource_richness': world.resource_richness,
                'production': world.spiritual_stones_production,
                'barrier_strength': world.barrier_strength,
                'guardian_level': world.guardian_level,
                'cultivation_bonus': world.cultivation_bonus,
                'market_level': world.market_level,
                'infrastructure_level': world.infrastructure_level,
                'total_power': world.get_total_power(),
                'dimensional_gate': world.dimensional_gate,
                'time_acceleration': world.time_acceleration,
                'auto_cultivation': world.auto_cultivation,
                'resource_multiplication': world.resource_multiplication
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

@app.route('/api/upgrade-test-account', methods=['POST'])
@login_required
def upgrade_test_account():
    """Nâng cấp tài khoản test lên cảnh giới Toàn Chi Thiên Đạo Đại Viên Mãn"""

    # Chỉ admin hoặc tài khoản có tên "thiendao" mới được sử dụng
    if not current_user.is_admin and 'thiendao' not in current_user.username.lower() and 'test' not in current_user.username.lower():
        return jsonify({
            'success': False, 
            'error': 'Chỉ tài khoản thiendao, test hoặc admin mới có thể nâng cấp!'
        })

    try:
        # Nâng cấp lên cảnh giới Toàn Chi Thiên Đạo Đại Viên Mãn
        current_user.cultivation_level = "Toàn Chi Thiên Đạo Đại Viên Mãn"
        current_user.spiritual_power = 999999999999  # 999 tỷ linh lực (max level)
        current_user.spiritual_stones = 999999999  # 999 triệu linh thạch
        current_user.cultivation_points = 10000000  # 10 triệu điểm tu luyện
        current_user.pills_count = 99999  # 99,999 đan dược
        current_user.artifacts_count = 9999  # 9,999 pháp bảo
        current_user.reputation = 1000000  # 1 triệu danh tiếng
        current_user.karma_points = 999999  # 999,999 nghiệp lực
        current_user.mining_level = 999  # Level 999 đào mỏ (max)
        current_user.mining_experience = 0

        # Mở khóa toàn bộ quyền năng hệ thống
        current_user.is_admin = True  # Admin privileges
        current_user.free_world_opening_used = False  # Reset world opening

        # Thêm achievement đặc biệt
        achievement = Achievement(
            user_id=current_user.id,
            title="Toàn Chi Thiên Đạo Đại Viên Mãn - Chí Tôn",
            description="Đạt được đỉnh cao tuyệt đối của tu tiên, vượt qua mọi giới hạn, thành tựu vô thượng chí tôn!",
            category="cultivation",
            rarity="legendary"
        )
        db.session.add(achievement)

        # Thêm achievement hệ thống
        system_achievement = Achievement(
            user_id=current_user.id,
            title="Hệ Thống Chi Chủ - Toàn Quyền",
            description="Mở khóa toàn bộ quyền năng hệ thống, trở thành chủ tể của thế giới tu tiên",
            category="system",
            rarity="legendary"
        )
        db.session.add(system_achievement)

        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Đã nâng cấp thành công lên Toàn Chi Thiên Đạo Đại Viên Mãn! Mở khóa toàn bộ quyền năng hệ thống!',
            'new_stats': {
                'cultivation_level': current_user.cultivation_level,
                'spiritual_power': current_user.spiritual_power,
                'spiritual_stones': current_user.spiritual_stones,
                'cultivation_points': current_user.cultivation_points,
                'is_admin': current_user.is_admin,
                'mining_level': current_user.mining_level
            }
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': f'Lỗi khi nâng cấp tài khoản: {str(e)}'
        })

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

# ========================
# PERPLEXITY AI ROUTES
# ========================

@app.route('/api/ai/cultivation-advice', methods=['POST'])
@login_required
def ai_cultivation_advice():
    """Get AI cultivation strategy advice"""
    if not PERPLEXITY_AVAILABLE:
        return jsonify({
            'success': False,
            'error': 'AI Hỗ trợ chưa được kích hoạt!'
        })

    try:
        user_data = {
            'cultivation_level': current_user.cultivation_level,
            'spiritual_power': current_user.spiritual_power,
            'spiritual_stones': current_user.spiritual_stones,
            'pills_count': current_user.pills_count,
            'artifacts_count': current_user.artifacts_count,
            'cultivation_points': current_user.cultivation_points
        }

        if perplexity_manager:
            advice = perplexity_manager.get_cultivation_advice(user_data)
        else:
            advice = "AI hỗ trợ chưa sẵn sàng!"

        return jsonify({
            'success': True,
            'advice': advice,
            'type': 'cultivation'
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Lỗi khi lấy lời khuyên tu luyện: {str(e)}'
        })

@app.route('/api/ai/guild-management', methods=['POST'])
@login_required
def ai_guild_management():
    """Get AI guild management advice"""
    if not PERPLEXITY_AVAILABLE:
        return jsonify({
            'success': False,
            'error': 'AI Hỗ trợ chưa được kích hoạt!'
        })

    if not current_user.guild_id:
        return jsonify({
            'success': False,
            'error': 'Bạn cần tham gia bang hội để nhận lời khuyên quản lý!'
        })

    try:
        guild = Guild.query.get(current_user.guild_id)
        if not guild:
            return jsonify({'success': False, 'error': 'Không tìm thấy bang hội!'})

        guild_data = {
            'name': guild.name,
            'member_count': len(guild.members),
            'level': guild.level,
            'treasury': guild.treasury
        }

        user_role = "Bang Chủ" if guild.leader_id == current_user.id else "Thành Viên"

        if perplexity_manager:
            advice = perplexity_manager.get_guild_management_advice(guild_data, user_role)
        else:
            advice = "AI hỗ trợ chưa sẵn sàng!"

        return jsonify({
            'success': True,
            'advice': advice,
            'type': 'guild_management'
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Lỗi khi lấy lời khuyên bang hội: {str(e)}'
        })

@app.route('/api/ai/expedition-advice', methods=['POST'])
@login_required
def ai_expedition_advice():
    """Get AI expedition planning advice"""
    if not PERPLEXITY_AVAILABLE:
        return jsonify({
            'success': False,
            'error': 'AI Hỗ trợ chưa được kích hoạt!'
        })

    try:
        context = request.json.get('context', 'planning') if request.json else 'planning'
        expedition_id = request.json.get('expedition_id') if request.json else None

        if expedition_id:
            # Get advice for existing expedition
            expedition = Expedition.query.get(expedition_id)
            if not expedition:
                return jsonify({'success': False, 'error': 'Không tìm thấy đạo lữ!'})

            expedition_data = {
                'name': expedition.name,
                'destination': expedition.destination,
                'status': expedition.status,
                'participants': expedition.participants
            }
            context = 'ongoing'
        else:
            # Get general expedition planning advice
            expedition_data = request.json or {}
            if not expedition_data:
                expedition_data = {
                    'destination': 'Bí Cảnh Linh Dược',
                    'difficulty_level': 3,
                    'duration_hours': 24,
                    'max_participants': 5,
                    'min_cultivation': current_user.cultivation_level
                }

        if perplexity_manager:
            advice = perplexity_manager.get_expedition_advice(expedition_data, context)
        else:
            advice = "AI hỗ trợ chưa sẵn sàng!"

        return jsonify({
            'success': True,
            'advice': advice,
            'type': 'expedition'
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Lỗi khi lấy lời khuyên đạo lữ: {str(e)}'
        })

@app.route('/api/ai/resource-optimization', methods=['POST'])
@login_required
def ai_resource_optimization():
    """Get AI resource management advice"""
    if not PERPLEXITY_AVAILABLE:
        return jsonify({
            'success': False,
            'error': 'AI Hỗ trợ chưa được kích hoạt!'
        })

    try:
        user_resources = {
            'spiritual_stones': current_user.spiritual_stones,
            'pills_count': current_user.pills_count,
            'artifacts_count': current_user.artifacts_count,
            'mining_level': current_user.mining_level,
            'cultivation_points': current_user.cultivation_points,
            'cultivation_level': current_user.cultivation_level
        }

        goals = request.json.get('goals', []) if request.json else []

        if perplexity_manager:
            advice = perplexity_manager.get_resource_optimization_advice(user_resources, goals)
        else:
            advice = "AI hỗ trợ chưa sẵn sàng!"

        return jsonify({
            'success': True,
            'advice': advice,
            'type': 'resources'
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Lỗi khi lấy lời khuyên tài nguyên: {str(e)}'
        })

@app.route('/api/ai/general', methods=['POST'])
@login_required
def ai_general_advice():
    """Get general AI advice about Tu Tiên world"""
    if not PERPLEXITY_AVAILABLE:
        return jsonify({
            'success': False,
            'error': 'AI Hỗ trợ chưa được kích hoạt!'
        })

    try:
        data = request.json or {}
        question = data.get('question', '')

        if not question:
            return jsonify({
                'success': False,
                'error': 'Vui lòng nhập câu hỏi!'
            })

        context = {
            'user_level': current_user.cultivation_level,
            'spiritual_power': current_user.spiritual_power,
            'guild': Guild.query.get(current_user.guild_id).name if current_user.guild_id else None
        }

        if perplexity_manager:
            advice = perplexity_manager.get_general_advice(question, context)
        else:
            advice = "AI hỗ trợ chưa sẵn sàng!"

        return jsonify({
            'success': True,
            'advice': advice,
            'type': 'general',
            'question': question
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Lỗi khi xử lý câu hỏi: {str(e)}'
        })

# ========================
# GUILD MANAGEMENT ROUTES
# ========================

@app.route('/api/update-guild-settings', methods=['POST'])
@login_required
def update_guild_settings():
    """Cập nhật cài đặt bang hội"""
    if not current_user.guild_id:
        return jsonify({'success': False, 'error': 'Bạn không thuộc bang hội nào!'})

    guild = Guild.query.get(current_user.guild_id)
    if not guild:
        return jsonify({'success': False, 'error': 'Không tìm thấy bang hội!'})

    # Chỉ bang chủ mới được cập nhật cài đặt
    if guild.leader_id != current_user.id:
        return jsonify({'success': False, 'error': 'Chỉ bang chủ mới có thể cập nhật cài đặt!'})

    try:
        data = request.json or {}

        # Cập nhật mô tả
        if 'description' in data:
            guild.description = data['description'][:500]  # Giới hạn 500 ký tự

        # Cập nhật trạng thái tuyển thành viên
        if 'recruitment_open' in data:
            guild.recruitment_open = bool(data['recruitment_open'])

        # Cập nhật yêu cầu tu vi tối thiểu
        if 'min_cultivation_level' in data:
            guild.min_cultivation_level = data['min_cultivation_level']

        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Cập nhật cài đặt bang hội thành công!',
            'guild': {
                'description': guild.description,
                'recruitment_open': guild.recruitment_open,
                'min_cultivation_level': guild.min_cultivation_level
            }
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': f'Lỗi khi cập nhật: {str(e)}'})

@app.route('/api/toggle-guild-recruitment', methods=['POST'])
@login_required
def toggle_guild_recruitment():
    """Bật/tắt tuyển thành viên bang hội"""
    if not current_user.guild_id:
        return jsonify({'success': False, 'error': 'Bạn không thuộc bang hội nào!'})

    guild = Guild.query.get(current_user.guild_id)
    if not guild:
        return jsonify({'success': False, 'error': 'Không tìm thấy bang hội!'})

    # Chỉ bang chủ mới được thay đổi
    if guild.leader_id != current_user.id:
        return jsonify({'success': False, 'error': 'Chỉ bang chủ mới có thể thay đổi cài đặt tuyển thành viên!'})

    try:
        data = request.json or {}
        recruitment_open = data.get('recruitment_open', not guild.recruitment_open)

        guild.recruitment_open = recruitment_open
        db.session.commit()

        status = "mở" if recruitment_open else "đóng"
        return jsonify({
            'success': True,
            'message': f'Đã {status} tuyển thành viên!',
            'recruitment_open': recruitment_open
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': f'Lỗi khi cập nhật: {str(e)}'})

@app.route('/api/declare-war', methods=['POST'])
@login_required
def declare_war():
    """Tuyên chiến với bang hội khác"""
    if not current_user.guild_id:
        return jsonify({'success': False, 'error': 'Bạn cần thuộc bang hội để tuyên chiến!'})

    guild = Guild.query.get(current_user.guild_id)
    if not guild:
        return jsonify({'success': False, 'error': 'Không tìm thấy bang hội!'})

    # Chỉ bang chủ mới được tuyên chiến
    if guild.leader_id != current_user.id:
        return jsonify({'success': False, 'error': 'Chỉ bang chủ mới có thể tuyên chiến!'})

    try:
        data = request.json or {}
        target_guild_id = data.get('target_guild_id')
        war_type = data.get('war_type')

        if not target_guild_id or not war_type:
            return jsonify({'success': False, 'error': 'Thiếu thông tin tuyên chiến!'})

        target_guild = Guild.query.get(target_guild_id)
        if not target_guild:
            return jsonify({'success': False, 'error': 'Không tìm thấy bang hội mục tiêu!'})

        if target_guild_id == guild.id:
            return jsonify({'success': False, 'error': 'Không thể tuyên chiến với chính mình!'})

        # Kiểm tra xem có đang trong chiến tranh không
        existing_war = GuildWar.query.filter(
            ((GuildWar.guild_id == guild.id) & (GuildWar.target_guild_id == target_guild_id)) |
            ((GuildWar.guild_id == target_guild_id) & (GuildWar.target_guild_id == guild.id))
        ).filter_by(status='Đang Diễn Ra').first()

        if existing_war:
            return jsonify({'success': False, 'error': 'Đã có chiến tranh đang diễn ra với bang hội này!'})

        # Tạo chiến tranh mới
        war = GuildWar(
            guild_id=guild.id,
            target_guild_id=target_guild_id,
            war_type=war_type,
            status='Đang Diễn Ra'
        )

        db.session.add(war)
        db.session.commit()

        return jsonify({
            'success': True,
            'message': f'Đã tuyên {war_type} với {target_guild.name}!',
            'war': {
                'id': war.id,
                'target_guild': target_guild.name,
                'war_type': war_type,
                'start_time': war.start_time.isoformat()
            }
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': f'Lỗi khi tuyên chiến: {str(e)}'})

@app.route('/api/request-join-guild', methods=['POST'])
@login_required
def request_join_guild():
    """Gửi yêu cầu gia nhập bang hội"""
    if current_user.guild_id:
        return jsonify({'success': False, 'error': 'Bạn đã có bang hội rồi!'})

    try:
        data = request.json or {}
        guild_id = data.get('guild_id')

        if not guild_id:
            return jsonify({'success': False, 'error': 'Thiếu ID bang hội!'})

        guild = Guild.query.get(guild_id)
        if not guild:
            return jsonify({'success': False, 'error': 'Không tìm thấy bang hội!'})

        if not guild.recruitment_open:
            return jsonify({'success': False, 'error': 'Bang hội này không tuyển thành viên!'})

        # Kiểm tra số lượng thành viên tối đa (giới hạn 50 thành viên)
        if len(guild.members) >= 50:
            return jsonify({'success': False, 'error': 'Bang hội đã đầy thành viên!'})

        # Thêm người dùng vào bang hội ngay lập tức (có thể thay đổi thành hệ thống phê duyệt)
        current_user.guild_id = guild.id

        # Tăng kinh nghiệm bang hội
        guild.experience += 100

        db.session.commit()

        return jsonify({
            'success': True,
            'message': f'Đã gia nhập bang hội {guild.name} thành công!',
            'guild': {
                'name': guild.name,
                'description': guild.description,
                'level': guild.level
            }
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': f'Lỗi khi gia nhập: {str(e)}'})

@app.route('/api/leave-guild', methods=['POST'])
@login_required
def leave_guild():
    """Rời khỏi bang hội"""
    if not current_user.guild_id:
        return jsonify({'success': False, 'error': 'Bạn không thuộc bang hội nào!'})

    guild = Guild.query.get(current_user.guild_id)
    if not guild:
        return jsonify({'success': False, 'error': 'Không tìm thấy bang hội!'})

    # Bang chủ không thể rời bang hội
    if guild.leader_id == current_user.id:
        return jsonify({'success': False, 'error': 'Bang chủ không thể rời bang hội! Hãy chuyển quyền bang chủ trước.'})

    try:
        guild_name = guild.name
        current_user.guild_id = None

        db.session.commit()

        return jsonify({
            'success': True,
            'message': f'Đã rời khỏi bang hội {guild_name}!'
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': f'Lỗi khi rời bang hội: {str(e)}'})

@app.route('/api/transfer-guild-leadership', methods=['POST'])
@login_required
def transfer_guild_leadership():
    """Chuyển quyền bang chủ"""
    if not current_user.guild_id:
        return jsonify({'success': False, 'error': 'Bạn không thuộc bang hội nào!'})

    guild = Guild.query.get(current_user.guild_id)
    if not guild:
        return jsonify({'success': False, 'error': 'Không tìm thấy bang hội!'})

    # Chỉ bang chủ hiện tại mới có thể chuyển quyền
    if guild.leader_id != current_user.id:
        return jsonify({'success': False, 'error': 'Chỉ bang chủ mới có thể chuyển quyền!'})

    try:
        data = request.json or {}
        new_leader_id = data.get('new_leader_id')

        if not new_leader_id:
            return jsonify({'success': False, 'error': 'Thiếu ID thành viên mới!'})

        new_leader = User.query.get(new_leader_id)
        if not new_leader:
            return jsonify({'success': False, 'error': 'Không tìm thấy thành viên!'})

        if new_leader.guild_id != guild.id:
            return jsonify({'success': False, 'error': 'Thành viên không thuộc bang hội này!'})

        # Chuyển quyền
        guild.leader_id = new_leader_id

        db.session.commit()

        return jsonify({
            'success': True,
            'message': f'Đã chuyển quyền bang chủ cho {new_leader.dao_name or new_leader.username}!',
            'new_leader': {
                'id': new_leader.id,
                'name': new_leader.dao_name or new_leader.username
            }
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': f'Lỗi khi chuyển quyền: {str(e)}'})

@app.route('/api/kick-member', methods=['POST'])
@login_required
def kick_member():
    """Đuổi thành viên khỏi bang hội"""
    if not current_user.guild_id:
        return jsonify({'success': False, 'error': 'Bạn không thuộc bang hội nào!'})

    guild = Guild.query.get(current_user.guild_id)
    if not guild:
        return jsonify({'success': False, 'error': 'Không tìm thấy bang hội!'})

    # Chỉ bang chủ mới có thể đuổi thành viên
    if guild.leader_id != current_user.id:
        return jsonify({'success': False, 'error': 'Chỉ bang chủ mới có thể đuổi thành viên!'})

    try:
        data = request.json or {}
        member_id = data.get('member_id')

        if not member_id:
            return jsonify({'success': False, 'error': 'Thiếu ID thành viên!'})

        member = User.query.get(member_id)
        if not member:
            return jsonify({'success': False, 'error': 'Không tìm thấy thành viên!'})

        if member.guild_id != guild.id:
            return jsonify({'success': False, 'error': 'Thành viên không thuộc bang hội này!'})

        if member.id == guild.leader_id:
            return jsonify({'success': False, 'error': 'Không thể đuổi bang chủ!'})

        # Đuổi thành viên
        member_name = member.dao_name or member.username
        member.guild_id = None

        db.session.commit()

        return jsonify({
            'success': True,
            'message': f'Đã đuổi {member_name} khỏi bang hội!',
            'kicked_member': {
                'id': member.id,
                'name': member_name
            }
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': f'Lỗi khi đuổi thành viên: {str(e)}'})

@app.route('/api/promote-member', methods=['POST'])
@login_required
def promote_member():
    """Thăng chức thành viên (placeholder cho tương lai)"""
    return jsonify({'success': True, 'message': 'Tính năng thăng chức sẽ được phát triển!'})

@app.route('/api/demote-member', methods=['POST'])
@login_required
def demote_member():
    """Giáng chức thành viên (placeholder cho tương lai)"""
    return jsonify({'success': True, 'message': 'Tính năng giáng chức sẽ được phát triển!'})

@app.route('/api/guild-join-requests', methods=['GET'])
@login_required
def guild_join_requests():
    """Lấy danh sách yêu cầu gia nhập bang hội (placeholder)"""
    return jsonify({'success': True, 'requests': []})

@app.route('/api/handle-join-request', methods=['POST'])
@login_required
def handle_join_request():
    """Xử lý yêu cầu gia nhập bang hội (placeholder)"""
    return jsonify({'success': True, 'message': 'Tính năng sẽ được phát triển!'})

@app.route('/api/conquer-world/<int:world_id>', methods=['POST'])
@login_required
def conquer_world(world_id):
    """Chinh phục thế giới khác"""
    world = World.query.get_or_404(world_id)
    
    # Kiểm tra xem thế giới có thể chinh phục được không
    if world.owner_id:
        return jsonify({'success': False, 'error': 'Thế giới này đã có chủ!'})
    
    # Tính chi phí chinh phục dựa trên sức mạnh thế giới
    world_power = world.get_total_power()
    conquest_cost = max(5000, world_power // 2)
    power_requirement = world_power
    
    # Kiểm tra điều kiện
    if current_user.spiritual_stones < conquest_cost:
        return jsonify({'success': False, 'error': f'Cần {conquest_cost} linh thạch để chinh phục!'})
    
    if current_user.spiritual_power < power_requirement:
        return jsonify({'success': False, 'error': f'Cần {power_requirement} linh lực để chinh phục!'})
    
    try:
        # Trừ chi phí
        current_user.spiritual_stones -= conquest_cost
        current_user.spiritual_power -= power_requirement // 3  # Mất 1/3 sức mạnh do chiến đấu
        
        # Chuyển quyền sở hữu
        world.owner_id = current_user.id
        world.is_contested = False
        world.last_attacked = datetime.utcnow()
        
        # Bonus chinh phục
        world.spiritual_stones_production += 50
        world.stability = max(50, world.stability - 20)  # Giảm ổn định sau chinh phục
        
        # Thêm achievement
        achievement = Achievement(
            user_id=current_user.id,
            title=f"Chinh Phục {world.name}",
            description=f"Đã chinh phục thành công thế giới {world.name} với sức mạnh {world_power}",
            category="conquest",
            rarity="epic" if world_power > 10000 else "rare"
        )
        db.session.add(achievement)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'Đã chinh phục {world.name}! Chi phí: {conquest_cost:,} linh thạch',
            'world': {
                'name': world.name,
                'production': world.spiritual_stones_production,
                'total_power': world.get_total_power()
            }
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': 'Lỗi khi chinh phục thế giới!'})

@app.route('/api/harvest-world/<int:world_id>', methods=['POST'])
@login_required
def harvest_world(world_id):
    """Thu hoạch tài nguyên từ thế giới"""
    world = World.query.get_or_404(world_id)
    
    if world.owner_id != current_user.id:
        return jsonify({'success': False, 'error': 'Bạn không sở hữu thế giới này!'})
    
    try:
        # Tính toán tài nguyên thu hoạch
        base_harvest = world.daily_income or world.spiritual_stones_production
        
        # Bonus từ các tính năng đặc biệt
        multiplier = 1.0
        if world.resource_multiplication:
            multiplier *= 2.0
        if world.time_acceleration:
            multiplier *= 1.5
        if world.market_level > 0:
            multiplier *= (1 + world.market_level * 0.1)
        
        total_harvest = int(base_harvest * multiplier)
        
        # Thu hoạch tài nguyên đặc biệt
        special_resources = {}
        if world.resource_richness >= 80:
            special_resources['spiritual_herbs'] = random.randint(1, world.resource_richness // 20)
            world.spiritual_herbs += special_resources['spiritual_herbs']
        
        if world.spiritual_density >= 90:
            special_resources['essence_crystals'] = random.randint(1, world.spiritual_density // 30)
            world.essence_crystals += special_resources['essence_crystals']
        
        if world.world_level >= 5:
            special_resources['ancient_artifacts'] = random.randint(0, world.world_level // 5)
            world.ancient_artifacts += special_resources['ancient_artifacts']
        
        # Cập nhật tài nguyên người chơi
        current_user.spiritual_stones += total_harvest
        
        # Cập nhật thống kê thế giới
        world.world_experience += 10
        world.special_events_count += 1
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'Thu hoạch thành công từ {world.name}!',
            'resources': {
                'spiritual_stones': total_harvest,
                'special_resources': special_resources
            },
            'multiplier': multiplier
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': 'Lỗi khi thu hoạch!'})

@app.route('/api/activate-world-ability/<int:world_id>', methods=['POST'])
@login_required
def activate_world_ability(world_id):
    """Kích hoạt khả năng đặc biệt của thế giới"""
    world = World.query.get_or_404(world_id)
    
    if world.owner_id != current_user.id:
        return jsonify({'success': False, 'error': 'Bạn không sở hữu thế giới này!'})
    
    data = request.json or {}
    ability_type = data.get('ability_type')
    
    try:
        if ability_type == 'time_acceleration' and world.time_acceleration:
            # Tăng tốc tu luyện trong 1 giờ
            bonus_power = int(current_user.spiritual_power * 0.1)
            current_user.spiritual_power += bonus_power
            message = f'Tăng tốc thời gian! +{bonus_power} linh lực'
            
        elif ability_type == 'dimensional_gate' and world.dimensional_gate:
            # Mở cổng đến thế giới khác (bonus tài nguyên)
            bonus_stones = world.world_level * 1000
            current_user.spiritual_stones += bonus_stones
            message = f'Mở cổng không gian! +{bonus_stones} linh thạch'
            
        elif ability_type == 'mass_cultivation' and world.auto_cultivation:
            # Tu luyện hàng loạt
            bonus_power = int(world.cultivation_bonus * 500)
            bonus_points = world.enlightenment_spots * 100
            current_user.spiritual_power += bonus_power
            current_user.cultivation_points += bonus_points
            message = f'Tu luyện hàng loạt! +{bonus_power} linh lực, +{bonus_points} điểm tu luyện'
            
        else:
            return jsonify({'success': False, 'error': 'Khả năng không khả dụng!'})
        
        # Giảm ổn định thế giới sau khi sử dụng khả năng
        world.stability = max(0, world.stability - 10)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': message,
            'world_stability': world.stability
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': 'Lỗi khi kích hoạt khả năng!'})

@app.route('/api/refresh-war-predictions', methods=['GET'])
@login_required
def refresh_war_predictions():
    """Làm mới dự đoán chiến tranh"""
    if not current_user.guild_id:
        return jsonify({'success': False, 'error': 'Bạn không thuộc bang hội nào!'})

    guild = Guild.query.get(current_user.guild_id)
    if not guild:
        return jsonify({'success': False, 'error': 'Không tìm thấy bang hội!'})

    if guild.leader_id != current_user.id:
        return jsonify({'success': False, 'error': 'Chỉ bang chủ mới có thể xem dự đoán chiến tranh!'})

    try:
        all_guilds = Guild.query.filter(Guild.id != guild.id).all()
        predictions = []

        for target_guild in all_guilds:
            # Tính toán dự đoán đơn giản
            my_power = sum(member.spiritual_power or 0 for member in guild.members)
            target_power = sum(member.spiritual_power or 0 for member in target_guild.members)

            if target_power > 0:
                win_probability = min(95, max(5, int((my_power / target_power) * 50)))
            else:
                win_probability = 95

            prediction = {
                'target_guild_id': target_guild.id,
                'target_guild_name': target_guild.name,
                'win_probability': win_probability,
                'duration_days': random.randint(1, 7),
                'casualty_estimate': 'Thấp' if win_probability > 70 else 'Trung Bình' if win_probability > 40 else 'Cao'
            }
            predictions.append(prediction)

        # Sắp xếp theo tỷ lệ thắng
        predictions.sort(key=lambda x: x['win_probability'], reverse=True)

        return jsonify({
            'success': True,
            'predictions': predictions[:5]  # Chỉ trả về 5 dự đoán hàng đầu
        })

    except Exception as e:
        return jsonify({'success': False, 'error': f'Lỗi khi tải dự đoán: {str(e)}'})

@app.route('/api/get-world-details/<int:world_id>', methods=['GET'])
@login_required
def get_world_details(world_id):
    """Lấy thông tin chi tiết thế giới"""
    world = World.query.get_or_404(world_id)
    
    if world.owner_id != current_user.id:
        return jsonify({'success': False, 'error': 'Bạn không sở hữu thế giới này!'})
    
    try:
        world_data = {
            'id': world.id,
            'name': world.name,
            'world_type': world.world_type,
            'world_level': world.world_level or 1,
            'world_experience': world.world_experience or 0,
            'spiritual_density': world.spiritual_density or 50,
            'resource_richness': world.resource_richness or 50,
            'stability': world.stability or 100,
            'barrier_strength': world.barrier_strength or 0,
            'guardian_level': world.guardian_level or 0,
            'market_level': world.market_level or 0,
            'infrastructure_level': world.infrastructure_level or 1,
            'cultivation_bonus': world.cultivation_bonus or 1.0,
            'enlightenment_spots': world.enlightenment_spots or 0,
            'spiritual_stones_production': world.spiritual_stones_production or 100,
            'daily_income': world.daily_income or 0,
            'dimensional_gate': world.dimensional_gate or False,
            'time_acceleration': world.time_acceleration or False,
            'auto_cultivation': world.auto_cultivation or False,
            'resource_multiplication': world.resource_multiplication or False,
            'total_power': world.get_total_power(),
            'special_resources': {
                'spiritual_herbs': world.spiritual_herbs or 0,
                'ancient_artifacts': world.ancient_artifacts or 0,
                'essence_crystals': world.essence_crystals or 0,
                'dragon_scales': world.dragon_scales or 0,
                'phoenix_feathers': world.phoenix_feathers or 0
            }
        }
        
        return jsonify({
            'success': True,
            'world': world_data
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': f'Lỗi khi tải thông tin: {str(e)}'})