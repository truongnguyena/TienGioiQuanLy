# Gemfile for Tu Tien Community Platform
source 'https://rubygems.org'

ruby '3.2.0'

# Web framework and HTTP
gem 'sinatra', '~> 3.0'
gem 'rack', '~> 3.0'
gem 'puma', '~> 6.0'

# Database and ORM
gem 'sequel', '~> 5.0'
gem 'pg', '~> 1.5'
gem 'sqlite3', '~> 1.6'

# API and JSON handling
gem 'json', '~> 2.6'
gem 'multi_json', '~> 1.15'
gem 'oj', '~> 3.16'

# HTTP client for API calls
gem 'httparty', '~> 0.21'
gem 'faraday', '~> 2.7'

# Background jobs and processing
gem 'sidekiq', '~> 7.0'
gem 'redis', '~> 5.0'

# File processing and utilities
gem 'fileutils'
gem 'pathname'
gem 'time'
gem 'date'

# Build and deployment tools
gem 'rake', '~> 13.0'
gem 'capistrano', '~> 3.17'
gem 'capistrano-rbenv', '~> 2.2'

# Testing framework
gem 'rspec', '~> 3.12'
gem 'rspec-core', '~> 3.12'
gem 'rspec-expectations', '~> 3.12'
gem 'rspec-mocks', '~> 3.12'
gem 'webmock', '~> 3.19'
gem 'vcr', '~> 6.1'

# Development tools
gem 'pry', '~> 0.14'
gem 'pry-byebug', '~> 3.10'
gem 'rubocop', '~> 1.50'
gem 'rubocop-rspec', '~> 2.20'

# Documentation
gem 'yard', '~> 0.9'
gem 'redcarpet', '~> 3.6'

# Monitoring and logging
gem 'logger'
gem 'syslog-logger', '~> 1.7'

# Data processing
gem 'csv'
gem 'yaml'
gem 'xml-simple', '~> 1.1'

# Security
gem 'bcrypt', '~> 3.1'
gem 'jwt', '~> 2.7'

# Performance monitoring
gem 'memory_profiler', '~> 1.0'
gem 'stackprof', '~> 0.2'

# Environment management
gem 'dotenv', '~> 2.8'

group :development do
  gem 'rerun', '~> 0.14'
  gem 'guard', '~> 2.18'
  gem 'guard-rspec', '~> 4.7'
end

group :test do
  gem 'factory_bot', '~> 6.4'
  gem 'faker', '~> 3.2'
end

group :production do
  gem 'unicorn', '~> 6.1'
  gem 'newrelic_rpm', '~> 9.0'
end
