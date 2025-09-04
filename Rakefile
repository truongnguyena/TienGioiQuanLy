# Rakefile for Tu Tien Community Platform
require 'rake'
require 'fileutils'
require 'json'
require 'yaml'
require 'time'

# Load environment
require 'dotenv'
Dotenv.load

# Configuration
APP_NAME = 'tu-tien-community'
PYTHON_APP_DIR = File.dirname(__FILE__)
RUBY_APP_DIR = File.join(PYTHON_APP_DIR, 'ruby_app')
LOG_DIR = File.join(PYTHON_APP_DIR, 'logs')
TEMP_DIR = File.join(PYTHON_APP_DIR, 'tmp')

# Ensure directories exist
[LOG_DIR, TEMP_DIR, RUBY_APP_DIR].each do |dir|
  FileUtils.mkdir_p(dir) unless Dir.exist?(dir)
end

namespace :app do
  desc "Start the full application stack"
  task :start do
    puts "🚀 Starting Tu Tien Community Platform..."
    
    # Start Python Flask app
    puts "Starting Python Flask app..."
    system("cd #{PYTHON_APP_DIR} && python main.py &")
    
    # Start Ruby API server
    puts "Starting Ruby API server..."
    system("cd #{RUBY_APP_DIR} && ruby api_server.rb &")
    
    # Start background job processor
    puts "Starting background job processor..."
    system("cd #{RUBY_APP_DIR} && bundle exec sidekiq &")
    
    puts "✅ All services started!"
  end

  desc "Stop all application services"
  task :stop do
    puts "🛑 Stopping all services..."
    
    # Kill Python processes
    system("pkill -f 'python main.py'")
    
    # Kill Ruby processes
    system("pkill -f 'ruby api_server.rb'")
    system("pkill -f 'sidekiq'")
    
    puts "✅ All services stopped!"
  end

  desc "Restart all services"
  task :restart => [:stop, :start]

  desc "Check application health"
  task :health do
    puts "🏥 Checking application health..."
    
    # Check Python app
    python_status = system("curl -s http://localhost:5000/health > /dev/null")
    puts python_status ? "✅ Python Flask app: Healthy" : "❌ Python Flask app: Unhealthy"
    
    # Check Ruby API
    ruby_status = system("curl -s http://localhost:4567/health > /dev/null")
    puts ruby_status ? "✅ Ruby API server: Healthy" : "❌ Ruby API server: Unhealthy"
    
    # Check database
    db_status = system("cd #{PYTHON_APP_DIR} && python -c 'from app import db; print(\"DB OK\")'")
    puts db_status ? "✅ Database: Healthy" : "❌ Database: Unhealthy"
  end
end

namespace :db do
  desc "Setup database with sample data"
  task :setup do
    puts "🗄️ Setting up database..."
    system("cd #{PYTHON_APP_DIR} && python init_production_db.py")
    puts "✅ Database setup complete!"
  end

  desc "Reset database"
  task :reset do
    puts "🔄 Resetting database..."
    system("cd #{PYTHON_APP_DIR} && python init_production_db.py")
    puts "✅ Database reset complete!"
  end

  desc "Backup database"
  task :backup do
    timestamp = Time.now.strftime("%Y%m%d_%H%M%S")
    backup_file = File.join(TEMP_DIR, "backup_#{timestamp}.sql")
    
    puts "💾 Creating database backup..."
    system("cd #{PYTHON_APP_DIR} && sqlite3 instance/tu_tien.db .dump > #{backup_file}")
    puts "✅ Database backed up to #{backup_file}"
  end

  desc "Restore database from backup"
  task :restore, [:backup_file] do |t, args|
    backup_file = args[:backup_file]
    unless backup_file && File.exist?(backup_file)
      puts "❌ Please specify a valid backup file"
      exit 1
    end
    
    puts "🔄 Restoring database from #{backup_file}..."
    system("cd #{PYTHON_APP_DIR} && sqlite3 instance/tu_tien.db < #{backup_file}")
    puts "✅ Database restored!"
  end
end

namespace :deploy do
  desc "Deploy to production"
  task :production do
    puts "🚀 Deploying to production..."
    
    # Run tests
    Rake::Task['test:all'].invoke
    
    # Backup database
    Rake::Task['db:backup'].invoke
    
    # Deploy to Render
    system("git push origin main")
    
    puts "✅ Production deployment initiated!"
  end

  desc "Deploy to staging"
  task :staging do
    puts "🧪 Deploying to staging..."
    
    # Run tests
    Rake::Task['test:all'].invoke
    
    # Deploy to staging
    system("git push origin staging")
    
    puts "✅ Staging deployment complete!"
  end
end

namespace :test do
  desc "Run all tests"
  task :all do
    puts "🧪 Running all tests..."
    
    # Run Python tests
    puts "Running Python tests..."
    system("cd #{PYTHON_APP_DIR} && python test_app.py")
    
    # Run Ruby tests
    puts "Running Ruby tests..."
    system("cd #{RUBY_APP_DIR} && bundle exec rspec")
    
    puts "✅ All tests completed!"
  end

  desc "Run Python tests only"
  task :python do
    puts "🐍 Running Python tests..."
    system("cd #{PYTHON_APP_DIR} && python test_app.py")
  end

  desc "Run Ruby tests only"
  task :ruby do
    puts "💎 Running Ruby tests..."
    system("cd #{RUBY_APP_DIR} && bundle exec rspec")
  end
end

namespace :build do
  desc "Build production assets"
  task :assets do
    puts "🏗️ Building production assets..."
    
    # Minify CSS
    system("cd #{PYTHON_APP_DIR}/static/css && npx clean-css-cli -o style.min.css style.css")
    
    # Minify JavaScript
    system("cd #{PYTHON_APP_DIR}/static/js && npx uglify-js --compress --mangle -o main.min.js main.js")
    
    puts "✅ Assets built successfully!"
  end

  desc "Clean build artifacts"
  task :clean do
    puts "🧹 Cleaning build artifacts..."
    
    FileUtils.rm_rf(Dir.glob("#{PYTHON_APP_DIR}/static/css/*.min.css"))
    FileUtils.rm_rf(Dir.glob("#{PYTHON_APP_DIR}/static/js/*.min.js"))
    FileUtils.rm_rf(TEMP_DIR)
    
    puts "✅ Build artifacts cleaned!"
  end
end

namespace :monitor do
  desc "Monitor application performance"
  task :performance do
    puts "📊 Monitoring application performance..."
    
    # Check memory usage
    memory_usage = `ps aux | grep -E '(python|ruby)' | awk '{sum+=$6} END {print sum/1024 " MB"}'`
    puts "Memory usage: #{memory_usage}"
    
    # Check CPU usage
    cpu_usage = `top -bn1 | grep -E '(python|ruby)' | awk '{sum+=$9} END {print sum "%"}'`
    puts "CPU usage: #{cpu_usage}"
    
    # Check disk usage
    disk_usage = `du -sh #{PYTHON_APP_DIR}`
    puts "Disk usage: #{disk_usage}"
  end

  desc "Monitor logs"
  task :logs do
    puts "📝 Monitoring application logs..."
    system("tail -f #{LOG_DIR}/*.log")
  end
end

namespace :data do
  desc "Generate sample data"
  task :generate do
    puts "📊 Generating sample data..."
    system("cd #{RUBY_APP_DIR} && ruby scripts/generate_sample_data.rb")
    puts "✅ Sample data generated!"
  end

  desc "Export data to JSON"
  task :export do
    puts "📤 Exporting data to JSON..."
    system("cd #{RUBY_APP_DIR} && ruby scripts/export_data.rb")
    puts "✅ Data exported!"
  end

  desc "Import data from JSON"
  task :import, [:json_file] do |t, args|
    json_file = args[:json_file]
    unless json_file && File.exist?(json_file)
      puts "❌ Please specify a valid JSON file"
      exit 1
    end
    
    puts "📥 Importing data from #{json_file}..."
    system("cd #{RUBY_APP_DIR} && ruby scripts/import_data.rb #{json_file}")
    puts "✅ Data imported!"
  end
end

# Default task
task :default => [:test, :build]

# Help task
desc "Show available tasks"
task :help do
  puts "🎯 Available tasks:"
  puts ""
  puts "Application:"
  puts "  rake app:start     - Start all services"
  puts "  rake app:stop      - Stop all services"
  puts "  rake app:restart   - Restart all services"
  puts "  rake app:health    - Check application health"
  puts ""
  puts "Database:"
  puts "  rake db:setup      - Setup database with sample data"
  puts "  rake db:reset      - Reset database"
  puts "  rake db:backup     - Backup database"
  puts "  rake db:restore    - Restore database from backup"
  puts ""
  puts "Deployment:"
  puts "  rake deploy:production - Deploy to production"
  puts "  rake deploy:staging    - Deploy to staging"
  puts ""
  puts "Testing:"
  puts "  rake test:all      - Run all tests"
  puts "  rake test:python   - Run Python tests only"
  puts "  rake test:ruby     - Run Ruby tests only"
  puts ""
  puts "Build:"
  puts "  rake build:assets  - Build production assets"
  puts "  rake build:clean   - Clean build artifacts"
  puts ""
  puts "Monitoring:"
  puts "  rake monitor:performance - Monitor performance"
  puts "  rake monitor:logs        - Monitor logs"
  puts ""
  puts "Data:"
  puts "  rake data:generate - Generate sample data"
  puts "  rake data:export   - Export data to JSON"
  puts "  rake data:import   - Import data from JSON"
end
