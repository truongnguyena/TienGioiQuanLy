#!/usr/bin/env ruby
# Import data to Tu Tien Community Platform
require 'json'
require 'sequel'
require 'dotenv'
require 'fileutils'

# Load environment
Dotenv.load

# Database connection
DB = Sequel.connect(ENV['DATABASE_URL'] || 'sqlite://../../instance/tu_tien.db')

class DataImporter
  def initialize
    @import_dir = File.join(File.dirname(__FILE__), '..', '..', 'exports')
    @backup_dir = File.join(File.dirname(__FILE__), '..', '..', 'backups')
    FileUtils.mkdir_p(@backup_dir)
  end

  def import_all
    puts "📥 Importing all data to Tu Tien Community Platform..."
    
    # Create backup before import
    create_backup
    
    import_users
    import_guilds
    import_worlds
    import_expeditions
    import_achievements
    import_chat_messages
    
    puts "✅ Data import completed!"
  end

  def import_file(filename)
    unless File.exist?(filename)
      puts "❌ File not found: #{filename}"
      return false
    end
    
    puts "📥 Importing data from #{filename}..."
    
    # Create backup before import
    create_backup
    
    begin
      data = JSON.parse(File.read(filename))
      
      if data.is_a?(Array)
        import_array_data(data, filename)
      else
        import_single_record(data, filename)
      end
      
      puts "✅ Import completed successfully!"
      true
    rescue => e
      puts "❌ Import failed: #{e.message}"
      false
    end
  end

  private

  def create_backup
    timestamp = Time.now.strftime('%Y%m%d_%H%M%S')
    backup_file = File.join(@backup_dir, "backup_before_import_#{timestamp}.sql")
    
    puts "💾 Creating backup before import..."
    system("sqlite3 #{DB.url.gsub('sqlite://', '')} .dump > #{backup_file}")
    puts "✅ Backup created: #{backup_file}"
  end

  def import_array_data(data, filename)
    table_name = determine_table_name(filename)
    
    if table_name
      puts "📊 Importing #{data.length} records to #{table_name}..."
      
      # Clear existing data
      DB[table_name.to_sym].delete
      
      # Import new data
      DB[table_name.to_sym].multi_insert(data)
      
      puts "✅ #{data.length} records imported to #{table_name}"
    else
      puts "❌ Could not determine table name from filename: #{filename}"
    end
  end

  def import_single_record(data, filename)
    table_name = determine_table_name(filename)
    
    if table_name
      puts "📊 Importing 1 record to #{table_name}..."
      
      # Import single record
      DB[table_name.to_sym].insert(data)
      
      puts "✅ 1 record imported to #{table_name}"
    else
      puts "❌ Could not determine table name from filename: #{filename}"
    end
  end

  def determine_table_name(filename)
    basename = File.basename(filename, '.json')
    
    case basename
    when /^users/
      'user'
    when /^guilds/
      'guild'
    when /^worlds/
      'world'
    when /^expeditions/
      'expedition'
    when /^achievements/
      'achievement'
    when /^chat_messages/
      'chat_message'
    else
      nil
    end
  end

  def import_users
    users_file = Dir.glob(File.join(@import_dir, 'users_*.json')).max_by { |f| File.mtime(f) }
    
    if users_file && File.exist?(users_file)
      puts "👥 Importing users from #{users_file}..."
      data = JSON.parse(File.read(users_file))
      
      # Clear existing users
      DB[:user].delete
      
      # Import users
      DB[:user].multi_insert(data)
      
      puts "✅ #{data.length} users imported"
    else
      puts "⚠️ No users file found, skipping..."
    end
  end

  def import_guilds
    guilds_file = Dir.glob(File.join(@import_dir, 'guilds_*.json')).max_by { |f| File.mtime(f) }
    
    if guilds_file && File.exist?(guilds_file)
      puts "🏰 Importing guilds from #{guilds_file}..."
      data = JSON.parse(File.read(guilds_file))
      
      # Clear existing guilds
      DB[:guild].delete
      
      # Import guilds
      DB[:guild].multi_insert(data)
      
      puts "✅ #{data.length} guilds imported"
    else
      puts "⚠️ No guilds file found, skipping..."
    end
  end

  def import_worlds
    worlds_file = Dir.glob(File.join(@import_dir, 'worlds_*.json')).max_by { |f| File.mtime(f) }
    
    if worlds_file && File.exist?(worlds_file)
      puts "🌍 Importing worlds from #{worlds_file}..."
      data = JSON.parse(File.read(worlds_file))
      
      # Clear existing worlds
      DB[:world].delete
      
      # Import worlds
      DB[:world].multi_insert(data)
      
      puts "✅ #{data.length} worlds imported"
    else
      puts "⚠️ No worlds file found, skipping..."
    end
  end

  def import_expeditions
    expeditions_file = Dir.glob(File.join(@import_dir, 'expeditions_*.json')).max_by { |f| File.mtime(f) }
    
    if expeditions_file && File.exist?(expeditions_file)
      puts "🗺️ Importing expeditions from #{expeditions_file}..."
      data = JSON.parse(File.read(expeditions_file))
      
      # Clear existing expeditions
      DB[:expedition].delete
      
      # Import expeditions
      DB[:expedition].multi_insert(data)
      
      puts "✅ #{data.length} expeditions imported"
    else
      puts "⚠️ No expeditions file found, skipping..."
    end
  end

  def import_achievements
    achievements_file = Dir.glob(File.join(@import_dir, 'achievements_*.json')).max_by { |f| File.mtime(f) }
    
    if achievements_file && File.exist?(achievements_file)
      puts "🏆 Importing achievements from #{achievements_file}..."
      data = JSON.parse(File.read(achievements_file))
      
      # Clear existing achievements
      DB[:achievement].delete
      
      # Import achievements
      DB[:achievement].multi_insert(data)
      
      puts "✅ #{data.length} achievements imported"
    else
      puts "⚠️ No achievements file found, skipping..."
    end
  end

  def import_chat_messages
    messages_file = Dir.glob(File.join(@import_dir, 'chat_messages_*.json')).max_by { |f| File.mtime(f) }
    
    if messages_file && File.exist?(messages_file)
      puts "💬 Importing chat messages from #{messages_file}..."
      data = JSON.parse(File.read(messages_file))
      
      # Clear existing chat messages
      DB[:chat_message].delete
      
      # Import chat messages
      DB[:chat_message].multi_insert(data)
      
      puts "✅ #{data.length} chat messages imported"
    else
      puts "⚠️ No chat messages file found, skipping..."
    end
  end
end

# Run the importer
if __FILE__ == $0
  importer = DataImporter.new
  
  if ARGV.length > 0
    # Import specific file
    filename = ARGV[0]
    importer.import_file(filename)
  else
    # Import all data
    importer.import_all
  end
end
