# Tu Tiên Cộng Đồng (Celestial Cultivation Community)

## Overview

Tu Tiên Cộng Đồng is a Vietnamese-language web-based cultivation (martial arts/fantasy) role-playing game and community platform. The application simulates a mystical cultivation world where users can develop their spiritual powers, join guilds, participate in expeditions, manage worlds, and interact with an AI-powered cultivation system. The platform combines traditional cultivation themes with modern web technologies to create an immersive gaming experience.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Template Engine**: Jinja2 templates with Flask for server-side rendering
- **UI Framework**: Bootstrap 5.3.0 for responsive design and component styling
- **Styling**: Custom CSS with mystical/celestial theming using CSS variables for consistent color schemes
- **JavaScript**: Vanilla JavaScript with class-based architecture for different modules (Dashboard, ExpeditionManager, GuildManager, TuTienApp)
- **Icons**: Font Awesome 6.4.0 for consistent iconography
- **Interactive Elements**: Modal dialogs, tabs, progress bars, and real-time updates

### Backend Architecture
- **Web Framework**: Flask with SQLAlchemy ORM for database operations
- **Authentication**: Flask-Login for user session management
- **Database Models**: SQLAlchemy with declarative base, supporting Users, Guilds, Worlds, Expeditions, and related entities
- **AI Integration**: Custom CultivationAI class for game mechanics and fortune predictions
- **Route Structure**: Modular routing system handling authentication, dashboard, community features, and game mechanics

### Data Storage Solutions
- **Primary Database**: SQLite (configurable to PostgreSQL via DATABASE_URL environment variable)
- **Connection Management**: SQLAlchemy with connection pooling (pool_recycle: 300s, pool_pre_ping enabled)
- **Schema Design**: Relational model with foreign key relationships between users, guilds, expeditions, and worlds

### Authentication and Authorization
- **User Management**: Flask-Login with password hashing using Werkzeug security utilities
- **Session Security**: Secret key-based sessions with environment variable configuration
- **User Roles**: Implicit role system through guild membership and world ownership
- **Password Security**: Bcrypt-style password hashing with salt

### Game Systems Architecture
- **Cultivation System**: Multi-stage progression system with spiritual power metrics
- **Guild System**: Hierarchical organization with treasury, levels, and member management
- **Expedition System**: Collaborative exploration with participation tracking
- **World Management**: Resource-generating territories with ownership and contest mechanics
- **AI Advisor**: Fortune prediction and cultivation guidance system

## External Dependencies

### Core Web Framework
- Flask: Primary web framework
- Flask-SQLAlchemy: Database ORM integration
- Flask-Login: User authentication and session management
- Werkzeug: WSGI utilities and security functions

### Frontend Libraries
- Bootstrap 5.3.0: CSS framework for responsive design
- Font Awesome 6.4.0: Icon library
- CDN-delivered assets for external library management

### Database Technology
- SQLite: Default development database
- PostgreSQL: Production database option (configurable via DATABASE_URL)
- SQLAlchemy: ORM with relationship management

### Python Standard Library Usage
- datetime: Time-based game mechanics and user activity tracking
- os: Environment variable management
- random: Game mechanics randomization
- json: Data serialization for complex game state management
- logging: Application monitoring and debugging

### Deployment Configuration
- ProxyFix middleware: Reverse proxy support for production deployment
- Environment-based configuration: Database URLs and secret keys via environment variables
- Debug mode: Configurable based on environment