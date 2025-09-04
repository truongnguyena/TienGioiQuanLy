#!/usr/bin/env ruby
# Generate sample data for Tu Tien Community Platform
require 'json'
require 'faker'
require 'sequel'
require 'dotenv'

# Load environment
Dotenv.load

# Database connection
DB = Sequel.connect(ENV['DATABASE_URL'] || 'sqlite://../../instance/tu_tien.db')

# Configure Faker for Vietnamese content
Faker::Config.locale = 'vi'

class SampleDataGenerator
  def initialize
    @users = []
    @guilds = []
    @worlds = []
    @expeditions = []
    @achievements = []
  end

  def generate_all
    puts "🎲 Generating sample data for Tu Tien Community Platform..."
    
    generate_users(50)
    generate_guilds(10)
    generate_worlds(25)
    generate_expeditions(15)
    generate_achievements(30)
    generate_chat_messages(100)
    
    puts "✅ Sample data generation completed!"
    puts "📊 Generated:"
    puts "  - #{@users.length} users"
    puts "  - #{@guilds.length} guilds"
    puts "  - #{@worlds.length} worlds"
    puts "  - #{@expeditions.length} expeditions"
    puts "  - #{@achievements.length} achievements"
  end

  private

  def generate_users(count)
    puts "👥 Generating #{count} users..."
    
    count.times do |i|
      user = {
        username: Faker::Internet.username,
        email: Faker::Internet.email,
        password_hash: BCrypt::Password.create('password123'),
        cultivation_level: random_cultivation_level,
        spiritual_power: rand(100..50000),
        cultivation_points: rand(0..1000),
        dao_name: random_dao_name,
        sect_affiliation: random_sect,
        reputation: rand(0..1000),
        karma_points: rand(0..500),
        spiritual_stones: rand(1000..50000),
        pills_count: rand(0..20),
        artifacts_count: rand(0..10),
        mining_level: rand(1..10),
        mining_experience: rand(0..1000),
        last_mining: random_time_in_past,
        free_world_opening_used: [true, false].sample,
        is_admin: i < 3, # First 3 users are admins
        created_at: random_time_in_past,
        last_cultivation: random_time_in_past
      }
      
      @users << user
      DB[:user].insert(user)
    end
  end

  def generate_guilds(count)
    puts "🏰 Generating #{count} guilds..."
    
    count.times do |i|
      guild = {
        name: random_guild_name,
        description: Faker::Lorem.paragraph,
        level: rand(1..20),
        treasury: rand(10000..1000000),
        recruitment_open: [true, false].sample,
        max_members: rand(10..50),
        created_at: random_time_in_past
      }
      
      # Assign leader
      if @users.any?
        leader = @users.sample
        guild[:leader_id] = leader[:id] || DB[:user].first[:id]
      end
      
      @guilds << guild
      guild_id = DB[:guild].insert(guild)
      
      # Assign some users to guilds
      if i < 5 && @users.any?
        guild_members = @users.sample(rand(3..10))
        guild_members.each do |user|
          DB[:user].where(id: user[:id] || DB[:user].first[:id]).update(guild_id: guild_id)
        end
      end
    end
  end

  def generate_worlds(count)
    puts "🌍 Generating #{count} worlds..."
    
    count.times do |i|
      world = {
        name: random_world_name,
        description: Faker::Lorem.paragraph,
        world_type: random_world_type,
        world_level: rand(1..10),
        spiritual_density: rand(10..100),
        danger_level: rand(1..10),
        is_contested: [true, false].sample,
        spiritual_stones_production: rand(100..5000),
        special_resources: random_special_resources,
        created_at: random_time_in_past
      }
      
      # Assign owner
      if @users.any?
        owner = @users.sample
        world[:owner_id] = owner[:id] || DB[:user].first[:id]
      end
      
      @worlds << world
      DB[:world].insert(world)
    end
  end

  def generate_expeditions(count)
    puts "🗺️ Generating #{count} expeditions..."
    
    count.times do |i|
      expedition = {
        name: random_expedition_name,
        description: Faker::Lorem.paragraph,
        expedition_type: random_expedition_type,
        difficulty_level: rand(1..10),
        required_level: random_cultivation_level,
        max_participants: rand(5..20),
        status: random_expedition_status,
        start_time: random_future_time,
        end_time: random_future_time,
        rewards: random_rewards,
        created_at: random_time_in_past
      }
      
      # Assign organizer guild
      if @guilds.any?
        guild = @guilds.sample
        expedition[:organizer_guild_id] = guild[:id] || DB[:guild].first[:id]
      end
      
      @expeditions << expedition
      DB[:expedition].insert(expedition)
    end
  end

  def generate_achievements(count)
    puts "🏆 Generating #{count} achievements..."
    
    count.times do |i|
      achievement = {
        name: random_achievement_name,
        description: Faker::Lorem.sentence,
        category: random_achievement_category,
        points: rand(10..1000),
        rarity: random_rarity,
        requirements: random_requirements,
        created_at: random_time_in_past
      }
      
      @achievements << achievement
      DB[:achievement].insert(achievement)
    end
  end

  def generate_chat_messages(count)
    puts "💬 Generating #{count} chat messages..."
    
    count.times do |i|
      message = {
        content: random_chat_message,
        user_id: @users.sample[:id] || DB[:user].first[:id],
        channel: random_channel,
        created_at: random_time_in_past
      }
      
      DB[:chat_message].insert(message)
    end
  end

  # Helper methods for random data generation
  def random_cultivation_level
    stages = [
      'Luyện Khí Tầng 1', 'Luyện Khí Tầng 2', 'Luyện Khí Tầng 3',
      'Luyện Khí Tầng 4', 'Luyện Khí Tầng 5', 'Luyện Khí Tầng 6',
      'Luyện Khí Tầng 7', 'Luyện Khí Tầng 8', 'Luyện Khí Tầng 9',
      'Trúc Cơ Tầng 1', 'Trúc Cơ Tầng 2', 'Trúc Cơ Tầng 3',
      'Kết Đan Tầng 1', 'Kết Đan Tầng 2', 'Kết Đan Tầng 3',
      'Nguyên Anh Tầng 1', 'Nguyên Anh Tầng 2', 'Nguyên Anh Tầng 3',
      'Hóa Thần Tầng 1', 'Hóa Thần Tầng 2', 'Hóa Thần Tầng 3'
    ]
    stages.sample
  end

  def random_dao_name
    prefixes = ['Thiên', 'Địa', 'Huyền', 'Minh', 'Cực', 'Vô', 'Thánh', 'Tiên']
    suffixes = ['Đạo', 'Tôn', 'Tử', 'Tiên', 'Thánh', 'Vương', 'Đế', 'Tôn']
    "#{prefixes.sample}#{suffixes.sample}"
  end

  def random_sect
    sects = [
      'Thiên Đạo Tông', 'Huyền Môn', 'Cực Lạc Tông', 'Vô Cực Môn',
      'Thánh Tiên Tông', 'Minh Vương Tông', 'Địa Huyền Môn', 'Tiên Vương Tông'
    ]
    sects.sample
  end

  def random_guild_name
    prefixes = ['Thiên', 'Địa', 'Huyền', 'Minh', 'Cực', 'Vô', 'Thánh', 'Tiên']
    suffixes = ['Tông', 'Môn', 'Bang', 'Hội', 'Liên Minh']
    "#{prefixes.sample}#{suffixes.sample}"
  end

  def random_world_name
    prefixes = ['Thiên', 'Địa', 'Huyền', 'Minh', 'Cực', 'Vô', 'Thánh', 'Tiên']
    suffixes = ['Giới', 'Cảnh', 'Thiên', 'Địa', 'Huyền', 'Minh']
    "#{prefixes.sample}#{suffixes.sample}"
  end

  def random_world_type
    types = ['Linh Giới', 'Ma Cảnh', 'Thiên Giới', 'Huyền Giới', 'Minh Giới', 'Cực Giới']
    types.sample
  end

  def random_special_resources
    resources = ['Linh Thạch', 'Đan Dược', 'Pháp Bảo', 'Công Pháp', 'Bí Tịch', 'Linh Thảo']
    resources.sample(rand(1..3)).join(', ')
  end

  def random_expedition_name
    prefixes = ['Thám Hiểm', 'Tìm Kiếm', 'Chinh Phục', 'Khám Phá', 'Chinh Chiến']
    suffixes = ['Thiên Cung', 'Địa Phủ', 'Huyền Cảnh', 'Minh Giới', 'Cực Lạc']
    "#{prefixes.sample} #{suffixes.sample}"
  end

  def random_expedition_type
    types = ['Thám Hiểm', 'Tìm Kiếm', 'Chinh Chiến', 'Tu Luyện', 'Khám Phá']
    types.sample
  end

  def random_expedition_status
    statuses = ['Chuẩn Bị', 'Đang Diễn Ra', 'Hoàn Thành', 'Hủy Bỏ']
    statuses.sample
  end

  def random_rewards
    rewards = {
      'Linh Thạch' => rand(1000..10000),
      'Đan Dược' => rand(1..10),
      'Pháp Bảo' => rand(1..5),
      'Kinh Nghiệm' => rand(100..1000)
    }
    rewards.to_json
  end

  def random_achievement_name
    names = [
      'Tu Luyện Đầu Tiên', 'Thành Lập Guild', 'Chinh Phục Thế Giới',
      'Thám Hiểm Thành Công', 'Đạt Thành Tựu', 'Vượt Qua Thử Thách',
      'Thu Thập Tài Nguyên', 'Nâng Cấp Cấp Độ', 'Hoàn Thành Nhiệm Vụ'
    ]
    names.sample
  end

  def random_achievement_category
    categories = ['Tu Luyện', 'Guild', 'Thế Giới', 'Thám Hiểm', 'Tài Nguyên', 'Chiến Đấu']
    categories.sample
  end

  def random_rarity
    rarities = ['Thường', 'Hiếm', 'Cực Hiếm', 'Huyền Thoại', 'Thần Thánh']
    rarities.sample
  end

  def random_requirements
    requirements = {
      'cultivation_level' => random_cultivation_level,
      'spiritual_power' => rand(1000..50000),
      'guild_level' => rand(1..20),
      'world_count' => rand(1..10)
    }
    requirements.to_json
  end

  def random_chat_message
    messages = [
      'Chào mọi người!', 'Tu luyện thế nào rồi?', 'Có ai muốn tham gia expedition không?',
      'Guild mình cần thêm thành viên!', 'Vừa đạt được achievement mới!',
      'Thế giới này thật tuyệt!', 'Có ai biết cách nâng cấp không?',
      'Mining được nhiều linh thạch quá!', 'Guild war sắp bắt đầu rồi!'
    ]
    messages.sample
  end

  def random_channel
    channels = ['general', 'guild', 'world', 'expedition', 'trading']
    channels.sample
  end

  def random_time_in_past
    Time.now - rand(0..30).days - rand(0..23).hours - rand(0..59).minutes
  end

  def random_future_time
    Time.now + rand(1..30).days + rand(0..23).hours + rand(0..59).minutes
  end
end

# Run the generator
if __FILE__ == $0
  generator = SampleDataGenerator.new
  generator.generate_all
end
