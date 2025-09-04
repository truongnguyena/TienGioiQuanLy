# spec_helper.rb for Tu Tien Community Platform
require 'rspec'
require 'webmock/rspec'
require 'vcr'
require 'sequel'
require 'dotenv'
require 'httparty'

# Load environment
Dotenv.load

# Database connection for testing
DB = Sequel.connect(ENV['TEST_DATABASE_URL'] || 'sqlite://test.db')

# Configure VCR for API testing
VCR.configure do |config|
  config.cassette_library_dir = 'spec/fixtures/vcr_cassettes'
  config.hook_into :webmock
  config.configure_rspec_metadata!
  config.filter_sensitive_data('<API_KEY>') { ENV['PERPLEXITY_API_KEY'] }
  config.filter_sensitive_data('<DATABASE_URL>') { ENV['DATABASE_URL'] }
end

# Configure RSpec
RSpec.configure do |config|
  config.expect_with :rspec do |expectations|
    expectations.include_chain_clauses_in_custom_matcher_descriptions = true
  end

  config.mock_with :rspec do |mocks|
    mocks.verify_partial_doubles = true
  end

  config.shared_context_metadata_behavior = :apply_to_host_groups
  config.filter_run_when_matching :focus
  config.example_status_persistence_file_path = 'spec/examples.txt'
  config.disable_monkey_patching!
  config.warnings = true

  if config.files_to_run.one?
    config.default_formatter = 'doc'
  end

  config.profile_examples = 10
  config.order = :random
  Kernel.srand config.seed

  # Database cleanup
  config.before(:each) do
    # Clear all tables before each test
    DB[:user].delete
    DB[:guild].delete
    DB[:world].delete
    DB[:expedition].delete
    DB[:achievement].delete
    DB[:chat_message].delete
  end

  # Helper methods
  config.include TestHelpers
end

# Test helpers module
module TestHelpers
  def create_test_user(attributes = {})
    default_attributes = {
      username: 'testuser',
      email: 'test@example.com',
      password_hash: 'hashed_password',
      cultivation_level: 'Luyện Khí Tầng 1',
      spiritual_power: 100,
      cultivation_points: 0,
      created_at: Time.now
    }
    
    user_id = DB[:user].insert(default_attributes.merge(attributes))
    DB[:user].where(id: user_id).first
  end

  def create_test_guild(attributes = {})
    default_attributes = {
      name: 'Test Guild',
      description: 'A test guild',
      level: 1,
      treasury: 10000,
      recruitment_open: true,
      max_members: 20,
      created_at: Time.now
    }
    
    guild_id = DB[:guild].insert(default_attributes.merge(attributes))
    DB[:guild].where(id: guild_id).first
  end

  def create_test_world(attributes = {})
    default_attributes = {
      name: 'Test World',
      description: 'A test world',
      world_type: 'Linh Giới',
      world_level: 1,
      spiritual_density: 50,
      danger_level: 1,
      is_contested: false,
      spiritual_stones_production: 100,
      created_at: Time.now
    }
    
    world_id = DB[:world].insert(default_attributes.merge(attributes))
    DB[:world].where(id: world_id).first
  end

  def create_test_expedition(attributes = {})
    default_attributes = {
      name: 'Test Expedition',
      description: 'A test expedition',
      expedition_type: 'Thám Hiểm',
      difficulty_level: 1,
      required_level: 'Luyện Khí Tầng 1',
      max_participants: 10,
      status: 'Chuẩn Bị',
      start_time: Time.now + 1.day,
      end_time: Time.now + 2.days,
      rewards: '{"Linh Thạch": 1000}',
      created_at: Time.now
    }
    
    expedition_id = DB[:expedition].insert(default_attributes.merge(attributes))
    DB[:expedition].where(id: expedition_id).first
  end

  def create_test_achievement(attributes = {})
    default_attributes = {
      name: 'Test Achievement',
      description: 'A test achievement',
      category: 'Tu Luyện',
      points: 100,
      rarity: 'Thường',
      requirements: '{"cultivation_level": "Luyện Khí Tầng 1"}',
      created_at: Time.now
    }
    
    achievement_id = DB[:achievement].insert(default_attributes.merge(attributes))
    DB[:achievement].where(id: achievement_id).first
  end

  def make_api_request(method, endpoint, data = nil)
    base_url = 'http://localhost:4567'
    url = "#{base_url}#{endpoint}"
    
    case method.to_sym
    when :get
      HTTParty.get(url)
    when :post
      HTTParty.post(url, body: data.to_json, headers: { 'Content-Type' => 'application/json' })
    when :put
      HTTParty.put(url, body: data.to_json, headers: { 'Content-Type' => 'application/json' })
    when :delete
      HTTParty.delete(url)
    end
  end

  def expect_successful_response(response)
    expect(response.code).to eq(200)
    expect(JSON.parse(response.body)['success']).to be true
  end

  def expect_error_response(response, status_code = 400)
    expect(response.code).to eq(status_code)
    expect(JSON.parse(response.body)['success']).to be false
  end
end
