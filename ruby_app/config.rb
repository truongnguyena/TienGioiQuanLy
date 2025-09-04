# Configuration file for Ruby API Server
require 'dotenv'
require 'logger'

# Load environment variables
Dotenv.load

module Config
  # Environment
  ENV = ENV['RUBY_ENV'] || 'development'
  PRODUCTION = ENV == 'production'
  DEVELOPMENT = ENV == 'development'
  TEST = ENV == 'test'

  # Server configuration
  PORT = ENV['PORT'] || 4567
  HOST = ENV['HOST'] || '0.0.0.0'

  # Database configuration
  DATABASE_URL = ENV['DATABASE_URL'] || 'sqlite://../instance/tu_tien.db'
  TEST_DATABASE_URL = ENV['TEST_DATABASE_URL'] || 'sqlite://test.db'

  # Redis configuration
  REDIS_URL = ENV['REDIS_URL'] || 'redis://localhost:6379'

  # Python API configuration
  PYTHON_API_URL = ENV['PYTHON_API_URL'] || 'http://localhost:5000'

  # Logging configuration
  LOG_LEVEL = ENV['LOG_LEVEL'] || 'info'
  LOG_FILE = ENV['LOG_FILE'] || '../logs/ruby_api.log'

  # Security configuration
  SECRET_KEY = ENV['SECRET_KEY'] || 'dev-secret-key-change-in-production'
  JWT_SECRET = ENV['JWT_SECRET'] || 'dev-jwt-secret-change-in-production'

  # External APIs
  PERPLEXITY_API_KEY = ENV['PERPLEXITY_API_KEY']
  OPENAI_API_KEY = ENV['OPENAI_API_KEY']

  # Background jobs
  SIDEKIQ_CONCURRENCY = (ENV['SIDEKIQ_CONCURRENCY'] || 5).to_i
  SIDEKIQ_TIMEOUT = (ENV['SIDEKIQ_TIMEOUT'] || 30).to_i

  # Monitoring
  NEW_RELIC_LICENSE_KEY = ENV['NEW_RELIC_LICENSE_KEY']
  SENTRY_DSN = ENV['SENTRY_DSN']

  # CORS configuration
  CORS_ORIGINS = ENV['CORS_ORIGINS']&.split(',') || ['*']

  # Rate limiting
  RATE_LIMIT_REQUESTS = (ENV['RATE_LIMIT_REQUESTS'] || 100).to_i
  RATE_LIMIT_WINDOW = (ENV['RATE_LIMIT_WINDOW'] || 3600).to_i

  # Cache configuration
  CACHE_TTL = (ENV['CACHE_TTL'] || 300).to_i
  CACHE_MAX_SIZE = (ENV['CACHE_MAX_SIZE'] || 1000).to_i

  # File uploads
  MAX_FILE_SIZE = (ENV['MAX_FILE_SIZE'] || 10 * 1024 * 1024).to_i # 10MB
  UPLOAD_DIR = ENV['UPLOAD_DIR'] || '../uploads'

  # Email configuration
  SMTP_HOST = ENV['SMTP_HOST']
  SMTP_PORT = (ENV['SMTP_PORT'] || 587).to_i
  SMTP_USERNAME = ENV['SMTP_USERNAME']
  SMTP_PASSWORD = ENV['SMTP_PASSWORD']
  SMTP_FROM = ENV['SMTP_FROM']

  # Notification configuration
  PUSH_NOTIFICATIONS_ENABLED = ENV['PUSH_NOTIFICATIONS_ENABLED'] == 'true'
  FCM_SERVER_KEY = ENV['FCM_SERVER_KEY']

  # Feature flags
  FEATURES = {
    real_time_updates: ENV['FEATURE_REAL_TIME_UPDATES'] != 'false',
    background_jobs: ENV['FEATURE_BACKGROUND_JOBS'] != 'false',
    data_export: ENV['FEATURE_DATA_EXPORT'] != 'false',
    data_import: ENV['FEATURE_DATA_IMPORT'] != 'false',
    api_documentation: ENV['FEATURE_API_DOCUMENTATION'] != 'false',
    monitoring: ENV['FEATURE_MONITORING'] != 'false'
  }

  # Validation rules
  VALIDATION_RULES = {
    username: {
      min_length: 3,
      max_length: 20,
      pattern: /\A[a-zA-Z0-9_]+\z/
    },
    email: {
      pattern: /\A[\w+\-.]+@[a-z\d\-]+(\.[a-z\d\-]+)*\.[a-z]+\z/i
    },
    password: {
      min_length: 6,
      max_length: 128
    },
    guild_name: {
      min_length: 3,
      max_length: 30
    },
    world_name: {
      min_length: 3,
      max_length: 50
    }
  }

  # Cultivation levels
  CULTIVATION_LEVELS = [
    'Luyện Khí Tầng 1', 'Luyện Khí Tầng 2', 'Luyện Khí Tầng 3',
    'Luyện Khí Tầng 4', 'Luyện Khí Tầng 5', 'Luyện Khí Tầng 6',
    'Luyện Khí Tầng 7', 'Luyện Khí Tầng 8', 'Luyện Khí Tầng 9',
    'Trúc Cơ Tầng 1', 'Trúc Cơ Tầng 2', 'Trúc Cơ Tầng 3',
    'Kết Đan Tầng 1', 'Kết Đan Tầng 2', 'Kết Đan Tầng 3',
    'Nguyên Anh Tầng 1', 'Nguyên Anh Tầng 2', 'Nguyên Anh Tầng 3',
    'Hóa Thần Tầng 1', 'Hóa Thần Tầng 2', 'Hóa Thần Tầng 3',
    'Luyện Hư Tầng 1', 'Luyện Hư Tầng 2', 'Luyện Hư Tầng 3',
    'Hợp Thể Tầng 1', 'Hợp Thể Tầng 2', 'Hợp Thể Tầng 3',
    'Đại Thừa Tầng 1', 'Đại Thừa Tầng 2', 'Đại Thừa Tầng 3',
    'Độ Kiếp Tầng 1', 'Độ Kiếp Tầng 2', 'Độ Kiếp Tầng 3',
    'Tản Tiên Tầng 1', 'Tản Tiên Tầng 2', 'Tản Tiên Tầng 3',
    'Toàn Chi Thiên Đạo'
  ]

  # World types
  WORLD_TYPES = [
    'Linh Giới', 'Ma Cảnh', 'Thiên Giới', 'Huyền Giới',
    'Minh Giới', 'Cực Giới', 'Vô Cực Giới', 'Thánh Giới'
  ]

  # Expedition types
  EXPEDITION_TYPES = [
    'Thám Hiểm', 'Tìm Kiếm', 'Chinh Chiến', 'Tu Luyện',
    'Khám Phá', 'Thu Thập', 'Bảo Vệ', 'Chinh Phục'
  ]

  # Achievement categories
  ACHIEVEMENT_CATEGORIES = [
    'Tu Luyện', 'Guild', 'Thế Giới', 'Thám Hiểm',
    'Tài Nguyên', 'Chiến Đấu', 'Xã Hội', 'Đặc Biệt'
  ]

  # Rarity levels
  RARITY_LEVELS = [
    'Thường', 'Hiếm', 'Cực Hiếm', 'Huyền Thoại', 'Thần Thánh'
  ]

  # Logger configuration
  def self.logger
    @logger ||= begin
      logger = Logger.new(LOG_FILE)
      logger.level = case LOG_LEVEL.downcase
                    when 'debug' then Logger::DEBUG
                    when 'info' then Logger::INFO
                    when 'warn' then Logger::WARN
                    when 'error' then Logger::ERROR
                    when 'fatal' then Logger::FATAL
                    else Logger::INFO
                    end
      logger
    end
  end

  # Validation helpers
  def self.valid_username?(username)
    return false unless username.is_a?(String)
    username.length >= VALIDATION_RULES[:username][:min_length] &&
    username.length <= VALIDATION_RULES[:username][:max_length] &&
    username.match?(VALIDATION_RULES[:username][:pattern])
  end

  def self.valid_email?(email)
    return false unless email.is_a?(String)
    email.match?(VALIDATION_RULES[:email][:pattern])
  end

  def self.valid_password?(password)
    return false unless password.is_a?(String)
    password.length >= VALIDATION_RULES[:password][:min_length] &&
    password.length <= VALIDATION_RULES[:password][:max_length]
  end

  def self.valid_cultivation_level?(level)
    CULTIVATION_LEVELS.include?(level)
  end

  def self.valid_world_type?(type)
    WORLD_TYPES.include?(type)
  end

  def self.valid_expedition_type?(type)
    EXPEDITION_TYPES.include?(type)
  end

  def self.valid_achievement_category?(category)
    ACHIEVEMENT_CATEGORIES.include?(category)
  end

  def self.valid_rarity?(rarity)
    RARITY_LEVELS.include?(rarity)
  end
end
