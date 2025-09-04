#!/usr/bin/env ruby
# Ruby API Server for Tu Tien Community Platform
require 'sinatra'
require 'json'
require 'httparty'
require 'sequel'
require 'redis'
require 'logger'
require 'dotenv'

# Load environment variables
Dotenv.load

# Configuration
set :port, 4567
set :bind, '0.0.0.0'
set :logging, true
set :show_exceptions, :after_handler

# Database connection
DB = Sequel.connect(ENV['DATABASE_URL'] || 'sqlite://../instance/tu_tien.db')

# Redis connection
REDIS = Redis.new(url: ENV['REDIS_URL'] || 'redis://localhost:6379')

# Logger
LOGGER = Logger.new(File.join(File.dirname(__FILE__), '..', 'logs', 'ruby_api.log'))

# Middleware
before do
  content_type :json
  headers 'Access-Control-Allow-Origin' => '*'
  headers 'Access-Control-Allow-Methods' => 'GET, POST, PUT, DELETE, OPTIONS'
  headers 'Access-Control-Allow-Headers' => 'Content-Type, Authorization'
end

# CORS preflight
options '*' do
  200
end

# Health check
get '/health' do
  {
    status: 'healthy',
    timestamp: Time.now.iso8601,
    services: {
      database: check_database_health,
      redis: check_redis_health,
      python_api: check_python_api_health
    }
  }.to_json
end

# API Routes
namespace '/api/v1' do
  # User management
  get '/users' do
    users = DB[:user].all
    {
      success: true,
      data: users,
      count: users.length
    }.to_json
  end

  get '/users/:id' do
    user = DB[:user].where(id: params[:id]).first
    if user
      {
        success: true,
        data: user
      }.to_json
    else
      status 404
      {
        success: false,
        error: 'User not found'
      }.to_json
    end
  end

  post '/users' do
    begin
      user_data = JSON.parse(request.body.read)
      user_id = DB[:user].insert(user_data)
      
      {
        success: true,
        data: { id: user_id },
        message: 'User created successfully'
      }.to_json
    rescue => e
      status 400
      {
        success: false,
        error: e.message
      }.to_json
    end
  end

  # Guild management
  get '/guilds' do
    guilds = DB[:guild].all
    {
      success: true,
      data: guilds,
      count: guilds.length
    }.to_json
  end

  get '/guilds/:id' do
    guild = DB[:guild].where(id: params[:id]).first
    if guild
      members = DB[:user].where(guild_id: params[:id]).all
      guild[:members] = members
      
      {
        success: true,
        data: guild
      }.to_json
    else
      status 404
      {
        success: false,
        error: 'Guild not found'
      }.to_json
    end
  end

  post '/guilds' do
    begin
      guild_data = JSON.parse(request.body.read)
      guild_id = DB[:guild].insert(guild_data)
      
      {
        success: true,
        data: { id: guild_id },
        message: 'Guild created successfully'
      }.to_json
    rescue => e
      status 400
      {
        success: false,
        error: e.message
      }.to_json
    end
  end

  # World management
  get '/worlds' do
    worlds = DB[:world].all
    {
      success: true,
      data: worlds,
      count: worlds.length
    }.to_json
  end

  get '/worlds/:id' do
    world = DB[:world].where(id: params[:id]).first
    if world
      {
        success: true,
        data: world
      }.to_json
    else
      status 404
      {
        success: false,
        error: 'World not found'
      }.to_json
    end
  end

  post '/worlds' do
    begin
      world_data = JSON.parse(request.body.read)
      world_id = DB[:world].insert(world_data)
      
      {
        success: true,
        data: { id: world_id },
        message: 'World created successfully'
      }.to_json
    rescue => e
      status 400
      {
        success: false,
        error: e.message
      }.to_json
    end
  end

  # Statistics
  get '/stats' do
    stats = {
      total_users: DB[:user].count,
      total_guilds: DB[:guild].count,
      total_worlds: DB[:world].count,
      active_expeditions: DB[:expedition].where(status: 'Đang Diễn Ra').count,
      total_achievements: DB[:achievement].count
    }
    
    {
      success: true,
      data: stats
    }.to_json
  end

  # Real-time data
  get '/realtime' do
    # Get cached real-time data from Redis
    realtime_data = {
      online_users: REDIS.get('online_users') || 0,
      active_guilds: REDIS.get('active_guilds') || 0,
      current_expeditions: REDIS.get('current_expeditions') || 0,
      last_updated: Time.now.iso8601
    }
    
    {
      success: true,
      data: realtime_data
    }.to_json
  end

  # Background job status
  get '/jobs/status' do
    job_stats = {
      pending: REDIS.llen('queue:default'),
      processed: REDIS.get('sidekiq:stat:processed') || 0,
      failed: REDIS.get('sidekiq:stat:failed') || 0
    }
    
    {
      success: true,
      data: job_stats
    }.to_json
  end

  # Data export
  get '/export/:table' do
    table = params[:table]
    allowed_tables = %w[user guild world expedition achievement]
    
    unless allowed_tables.include?(table)
      status 400
      return {
        success: false,
        error: 'Invalid table name'
      }.to_json
    end
    
    data = DB[table.to_sym].all
    {
      success: true,
      data: data,
      count: data.length,
      table: table
    }.to_json
  end

  # Data import
  post '/import/:table' do
    table = params[:table]
    allowed_tables = %w[user guild world expedition achievement]
    
    unless allowed_tables.include?(table)
      status 400
      return {
        success: false,
        error: 'Invalid table name'
      }.to_json
    end
    
    begin
      data = JSON.parse(request.body.read)
      
      if data.is_a?(Array)
        DB[table.to_sym].multi_insert(data)
        message = "#{data.length} records imported to #{table}"
      else
        DB[table.to_sym].insert(data)
        message = "1 record imported to #{table}"
      end
      
      {
        success: true,
        message: message
      }.to_json
    rescue => e
      status 400
      {
        success: false,
        error: e.message
      }.to_json
    end
  end
end

# Error handling
error 404 do
  {
    success: false,
    error: 'Not found',
    message: 'The requested resource was not found'
  }.to_json
end

error 500 do
  {
    success: false,
    error: 'Internal server error',
    message: 'An unexpected error occurred'
  }.to_json
end

# Helper methods
def check_database_health
  begin
    DB.test_connection
    'healthy'
  rescue => e
    LOGGER.error "Database health check failed: #{e.message}"
    'unhealthy'
  end
end

def check_redis_health
  begin
    REDIS.ping == 'PONG' ? 'healthy' : 'unhealthy'
  rescue => e
    LOGGER.error "Redis health check failed: #{e.message}"
    'unhealthy'
  end
end

def check_python_api_health
  begin
    response = HTTParty.get('http://localhost:5000/', timeout: 5)
    response.code == 200 ? 'healthy' : 'unhealthy'
  rescue => e
    LOGGER.error "Python API health check failed: #{e.message}"
    'unhealthy'
  end
end

# Background job processor
class BackgroundJobProcessor
  include Sidekiq::Worker
  
  def perform(job_type, data)
    case job_type
    when 'update_user_stats'
      update_user_statistics(data)
    when 'process_guild_war'
      process_guild_war(data)
    when 'generate_world_resources'
      generate_world_resources(data)
    when 'send_notification'
      send_notification(data)
    else
      LOGGER.warn "Unknown job type: #{job_type}"
    end
  end
  
  private
  
  def update_user_statistics(data)
    user_id = data['user_id']
    # Update user statistics in background
    LOGGER.info "Updating statistics for user #{user_id}"
  end
  
  def process_guild_war(data)
    war_id = data['war_id']
    # Process guild war logic
    LOGGER.info "Processing guild war #{war_id}"
  end
  
  def generate_world_resources(data)
    world_id = data['world_id']
    # Generate resources for world
    LOGGER.info "Generating resources for world #{world_id}"
  end
  
  def send_notification(data)
    user_id = data['user_id']
    message = data['message']
    # Send notification to user
    LOGGER.info "Sending notification to user #{user_id}: #{message}"
  end
end

# Start server
if __FILE__ == $0
  puts "🚀 Starting Ruby API Server on port 4567..."
  puts "📊 Health check: http://localhost:4567/health"
  puts "📚 API docs: http://localhost:4567/api/v1"
  
  # Start background job processor
  Thread.new do
    require 'sidekiq'
    Sidekiq.configure_client do |config|
      config.redis = { url: ENV['REDIS_URL'] || 'redis://localhost:6379' }
    end
    
    puts "🔄 Background job processor started"
  end
  
  # Start the server
  Sinatra::Application.run!
end
