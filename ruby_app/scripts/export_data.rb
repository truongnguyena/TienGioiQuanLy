#!/usr/bin/env ruby
# Export data from Tu Tien Community Platform
require 'json'
require 'sequel'
require 'dotenv'
require 'fileutils'

# Load environment
Dotenv.load

# Database connection
DB = Sequel.connect(ENV['DATABASE_URL'] || 'sqlite://../../instance/tu_tien.db')

class DataExporter
  def initialize
    @export_dir = File.join(File.dirname(__FILE__), '..', '..', 'exports')
    FileUtils.mkdir_p(@export_dir)
    @timestamp = Time.now.strftime('%Y%m%d_%H%M%S')
  end

  def export_all
    puts "📤 Exporting all data from Tu Tien Community Platform..."
    
    export_users
    export_guilds
    export_worlds
    export_expeditions
    export_achievements
    export_chat_messages
    export_statistics
    
    puts "✅ Data export completed!"
    puts "📁 Export directory: #{@export_dir}"
  end

  def export_table(table_name)
    puts "📤 Exporting #{table_name} data..."
    
    data = DB[table_name.to_sym].all
    filename = File.join(@export_dir, "#{table_name}_#{@timestamp}.json")
    
    File.write(filename, JSON.pretty_generate(data))
    puts "✅ #{table_name} exported to #{filename}"
    
    {
      table: table_name,
      count: data.length,
      filename: filename
    }
  end

  private

  def export_users
    puts "👥 Exporting users..."
    users = DB[:user].all
    filename = File.join(@export_dir, "users_#{@timestamp}.json")
    
    # Remove sensitive data
    safe_users = users.map do |user|
      user.reject { |k, v| k == :password_hash }
    end
    
    File.write(filename, JSON.pretty_generate(safe_users))
    puts "✅ #{users.length} users exported to #{filename}"
  end

  def export_guilds
    puts "🏰 Exporting guilds..."
    guilds = DB[:guild].all
    filename = File.join(@export_dir, "guilds_#{@timestamp}.json")
    
    # Include member count
    guilds_with_members = guilds.map do |guild|
      member_count = DB[:user].where(guild_id: guild[:id]).count
      guild.merge(member_count: member_count)
    end
    
    File.write(filename, JSON.pretty_generate(guilds_with_members))
    puts "✅ #{guilds.length} guilds exported to #{filename}"
  end

  def export_worlds
    puts "🌍 Exporting worlds..."
    worlds = DB[:world].all
    filename = File.join(@export_dir, "worlds_#{@timestamp}.json")
    
    # Include owner information
    worlds_with_owners = worlds.map do |world|
      if world[:owner_id]
        owner = DB[:user].where(id: world[:owner_id]).first
        world.merge(owner_name: owner ? owner[:username] : 'Unknown')
      else
        world.merge(owner_name: 'No Owner')
      end
    end
    
    File.write(filename, JSON.pretty_generate(worlds_with_owners))
    puts "✅ #{worlds.length} worlds exported to #{filename}"
  end

  def export_expeditions
    puts "🗺️ Exporting expeditions..."
    expeditions = DB[:expedition].all
    filename = File.join(@export_dir, "expeditions_#{@timestamp}.json")
    
    # Include participant count
    expeditions_with_participants = expeditions.map do |expedition|
      participant_count = DB[:expedition_participant].where(expedition_id: expedition[:id]).count
      expedition.merge(participant_count: participant_count)
    end
    
    File.write(filename, JSON.pretty_generate(expeditions_with_participants))
    puts "✅ #{expeditions.length} expeditions exported to #{filename}"
  end

  def export_achievements
    puts "🏆 Exporting achievements..."
    achievements = DB[:achievement].all
    filename = File.join(@export_dir, "achievements_#{@timestamp}.json")
    
    File.write(filename, JSON.pretty_generate(achievements))
    puts "✅ #{achievements.length} achievements exported to #{filename}"
  end

  def export_chat_messages
    puts "💬 Exporting chat messages..."
    messages = DB[:chat_message].all
    filename = File.join(@export_dir, "chat_messages_#{@timestamp}.json")
    
    # Include user information
    messages_with_users = messages.map do |message|
      if message[:user_id]
        user = DB[:user].where(id: message[:user_id]).first
        message.merge(user_name: user ? user[:username] : 'Unknown')
      else
        message.merge(user_name: 'Unknown')
      end
    end
    
    File.write(filename, JSON.pretty_generate(messages_with_users))
    puts "✅ #{messages.length} chat messages exported to #{filename}"
  end

  def export_statistics
    puts "📊 Exporting statistics..."
    
    stats = {
      export_timestamp: Time.now.iso8601,
      total_users: DB[:user].count,
      total_guilds: DB[:guild].count,
      total_worlds: DB[:world].count,
      total_expeditions: DB[:expedition].count,
      total_achievements: DB[:achievement].count,
      total_chat_messages: DB[:chat_message].count,
      active_users: DB[:user].where(last_cultivation: (Time.now - 7.days)..Time.now).count,
      active_guilds: DB[:guild].where(recruitment_open: true).count,
      contested_worlds: DB[:world].where(is_contested: true).count,
      ongoing_expeditions: DB[:expedition].where(status: 'Đang Diễn Ra').count
    }
    
    filename = File.join(@export_dir, "statistics_#{@timestamp}.json")
    File.write(filename, JSON.pretty_generate(stats))
    puts "✅ Statistics exported to #{filename}"
  end
end

# Run the exporter
if __FILE__ == $0
  exporter = DataExporter.new
  
  if ARGV.length > 0
    # Export specific table
    table_name = ARGV[0]
    result = exporter.export_table(table_name)
    puts "📊 Exported #{result[:count]} records from #{result[:table]}"
  else
    # Export all data
    exporter.export_all
  end
end
