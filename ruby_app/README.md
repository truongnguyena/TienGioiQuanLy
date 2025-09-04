# Ruby API Server for Tu Tien Community Platform

## 🚀 Overview

This Ruby API server provides additional functionality and services for the Tu Tien Community Platform, complementing the main Python Flask application.

## 📁 Structure

```
ruby_app/
├── api_server.rb          # Main Sinatra API server
├── config.rb              # Configuration management
├── scripts/               # Utility scripts
│   ├── generate_sample_data.rb
│   ├── export_data.rb
│   └── import_data.rb
├── spec/                  # RSpec test suite
│   ├── spec_helper.rb
│   └── api_spec.rb
└── README.md              # This file
```

## 🛠️ Features

### API Server
- **RESTful API** for data management
- **Health monitoring** endpoints
- **Data export/import** functionality
- **Real-time statistics**
- **Background job processing**
- **CORS support** for web integration

### Utility Scripts
- **Sample data generation** for testing
- **Data export** to JSON format
- **Data import** from JSON files
- **Database backup/restore**

### Testing Framework
- **RSpec** test suite
- **API endpoint testing**
- **Database integration tests**
- **Mock and stub support**

## 🚀 Quick Start

### Prerequisites
- Ruby 3.2.0+
- Bundler gem
- SQLite or PostgreSQL
- Redis (optional)

### Installation

1. **Install dependencies:**
```bash
cd ruby_app
bundle install
```

2. **Configure environment:**
```bash
cp .env.example .env
# Edit .env with your configuration
```

3. **Start the server:**
```bash
ruby api_server.rb
```

The server will start on `http://localhost:4567`

## 📚 API Documentation

### Health Check
```http
GET /health
```
Returns server health status and service availability.

### Users API
```http
GET    /api/v1/users          # List all users
GET    /api/v1/users/:id      # Get specific user
POST   /api/v1/users          # Create new user
```

### Guilds API
```http
GET    /api/v1/guilds         # List all guilds
GET    /api/v1/guilds/:id     # Get specific guild with members
POST   /api/v1/guilds         # Create new guild
```

### Worlds API
```http
GET    /api/v1/worlds         # List all worlds
GET    /api/v1/worlds/:id     # Get specific world
POST   /api/v1/worlds         # Create new world
```

### Statistics API
```http
GET    /api/v1/stats          # Get platform statistics
GET    /api/v1/realtime       # Get real-time data
```

### Data Management
```http
GET    /api/v1/export/:table  # Export table data
POST   /api/v1/import/:table  # Import table data
```

## 🧪 Testing

### Run all tests:
```bash
bundle exec rspec
```

### Run specific test file:
```bash
bundle exec rspec spec/api_spec.rb
```

### Run with coverage:
```bash
COVERAGE=true bundle exec rspec
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `RUBY_ENV` | Environment (development/test/production) | development |
| `PORT` | Server port | 4567 |
| `HOST` | Server host | 0.0.0.0 |
| `DATABASE_URL` | Database connection string | sqlite://../instance/tu_tien.db |
| `REDIS_URL` | Redis connection string | redis://localhost:6379 |
| `PYTHON_API_URL` | Python API base URL | http://localhost:5000 |
| `LOG_LEVEL` | Logging level | info |

### Feature Flags

Control feature availability via environment variables:

- `FEATURE_REAL_TIME_UPDATES` - Enable real-time data updates
- `FEATURE_BACKGROUND_JOBS` - Enable background job processing
- `FEATURE_DATA_EXPORT` - Enable data export functionality
- `FEATURE_DATA_IMPORT` - Enable data import functionality
- `FEATURE_API_DOCUMENTATION` - Enable API documentation
- `FEATURE_MONITORING` - Enable monitoring and metrics

## 📊 Scripts

### Generate Sample Data
```bash
ruby scripts/generate_sample_data.rb
```
Creates sample users, guilds, worlds, expeditions, and achievements for testing.

### Export Data
```bash
# Export all data
ruby scripts/export_data.rb

# Export specific table
ruby scripts/export_data.rb users
```

### Import Data
```bash
# Import from file
ruby scripts/import_data.rb exports/users_20250105_123456.json

# Import all data
ruby scripts/import_data.rb
```

## 🔄 Background Jobs

The server supports background job processing using Sidekiq:

### Job Types
- `update_user_stats` - Update user statistics
- `process_guild_war` - Process guild war logic
- `generate_world_resources` - Generate world resources
- `send_notification` - Send user notifications

### Job Status
```http
GET /api/v1/jobs/status
```
Returns pending, processed, and failed job counts.

## 📈 Monitoring

### Health Endpoints
- `/health` - Overall system health
- `/api/v1/stats` - Platform statistics
- `/api/v1/realtime` - Real-time metrics

### Logging
Logs are written to `../logs/ruby_api.log` with configurable levels.

## 🚀 Deployment

### Using Rake Tasks
```bash
# Start all services
rake app:start

# Stop all services
rake app:stop

# Restart services
rake app:restart

# Check health
rake app:health
```

### Manual Deployment
1. Install dependencies: `bundle install`
2. Configure environment variables
3. Start server: `ruby api_server.rb`
4. Start background jobs: `bundle exec sidekiq`

## 🔒 Security

### Authentication
- JWT token support
- API key authentication
- Rate limiting

### Data Protection
- Input validation
- SQL injection prevention
- XSS protection
- CORS configuration

## 🐛 Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Check `DATABASE_URL` configuration
   - Ensure database is accessible
   - Verify database permissions

2. **Redis Connection Error**
   - Check `REDIS_URL` configuration
   - Ensure Redis server is running
   - Verify Redis connectivity

3. **Python API Connection Error**
   - Check `PYTHON_API_URL` configuration
   - Ensure Python Flask app is running
   - Verify network connectivity

### Debug Mode
Set `RUBY_ENV=development` and `LOG_LEVEL=debug` for detailed logging.

## 📝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## 📄 License

This project is part of the Tu Tien Community Platform and follows the same license terms.

## 🤝 Support

For support and questions:
- Create an issue in the repository
- Check the documentation
- Review the test cases for examples
