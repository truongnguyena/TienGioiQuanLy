-- Database Migration Script
-- Fix missing columns in world table

-- Add missing columns to world table
ALTER TABLE world ADD COLUMN world_level INTEGER DEFAULT 1;
ALTER TABLE world ADD COLUMN world_experience INTEGER DEFAULT 0;
ALTER TABLE world ADD COLUMN stability INTEGER DEFAULT 100;
ALTER TABLE world ADD COLUMN magical_resonance INTEGER DEFAULT 50;
ALTER TABLE world ADD COLUMN time_flow_rate FLOAT DEFAULT 1.0;
ALTER TABLE world ADD COLUMN gravity_strength FLOAT DEFAULT 1.0;
ALTER TABLE world ADD COLUMN barrier_strength INTEGER DEFAULT 0;
ALTER TABLE world ADD COLUMN guardian_level INTEGER DEFAULT 0;
ALTER TABLE world ADD COLUMN trap_density INTEGER DEFAULT 0;
ALTER TABLE world ADD COLUMN daily_income INTEGER DEFAULT 0;
ALTER TABLE world ADD COLUMN trade_routes INTEGER DEFAULT 0;
ALTER TABLE world ADD COLUMN market_level INTEGER DEFAULT 0;
ALTER TABLE world ADD COLUMN spiritual_herbs INTEGER DEFAULT 0;
ALTER TABLE world ADD COLUMN ancient_artifacts INTEGER DEFAULT 0;
ALTER TABLE world ADD COLUMN essence_crystals INTEGER DEFAULT 0;
ALTER TABLE world ADD COLUMN dragon_scales INTEGER DEFAULT 0;
ALTER TABLE world ADD COLUMN phoenix_feathers INTEGER DEFAULT 0;
ALTER TABLE world ADD COLUMN climate_control INTEGER DEFAULT 0;
ALTER TABLE world ADD COLUMN terrain_complexity INTEGER DEFAULT 1;
ALTER TABLE world ADD COLUMN ecosystem_diversity INTEGER DEFAULT 1;
ALTER TABLE world ADD COLUMN natural_wonders INTEGER DEFAULT 0;
ALTER TABLE world ADD COLUMN cultivation_bonus FLOAT DEFAULT 1.0;
ALTER TABLE world ADD COLUMN breakthrough_chance FLOAT DEFAULT 0.1;
ALTER TABLE world ADD COLUMN enlightenment_spots INTEGER DEFAULT 0;
ALTER TABLE world ADD COLUMN population_limit INTEGER DEFAULT 100;
ALTER TABLE world ADD COLUMN current_population INTEGER DEFAULT 0;
ALTER TABLE world ADD COLUMN development_level INTEGER DEFAULT 1;
ALTER TABLE world ADD COLUMN infrastructure_level INTEGER DEFAULT 1;
ALTER TABLE world ADD COLUMN dimensional_gate BOOLEAN DEFAULT 0;
ALTER TABLE world ADD COLUMN time_acceleration BOOLEAN DEFAULT 0;
ALTER TABLE world ADD COLUMN resource_multiplication BOOLEAN DEFAULT 0;
ALTER TABLE world ADD COLUMN auto_cultivation BOOLEAN DEFAULT 0;
ALTER TABLE world ADD COLUMN last_explored DATETIME;
ALTER TABLE world ADD COLUMN last_upgraded DATETIME;
ALTER TABLE world ADD COLUMN total_upgrades INTEGER DEFAULT 0;
ALTER TABLE world ADD COLUMN last_attacked DATETIME;
ALTER TABLE world ADD COLUMN successful_defenses INTEGER DEFAULT 0;
ALTER TABLE world ADD COLUMN special_events_count INTEGER DEFAULT 0;

-- Update existing records with default values
UPDATE world SET 
    world_level = 1,
    world_experience = 0,
    stability = 100,
    magical_resonance = 50,
    time_flow_rate = 1.0,
    gravity_strength = 1.0,
    barrier_strength = 0,
    guardian_level = 0,
    trap_density = 0,
    daily_income = 0,
    trade_routes = 0,
    market_level = 0,
    spiritual_herbs = 0,
    ancient_artifacts = 0,
    essence_crystals = 0,
    dragon_scales = 0,
    phoenix_feathers = 0,
    climate_control = 0,
    terrain_complexity = 1,
    ecosystem_diversity = 1,
    natural_wonders = 0,
    cultivation_bonus = 1.0,
    breakthrough_chance = 0.1,
    enlightenment_spots = 0,
    population_limit = 100,
    current_population = 0,
    development_level = 1,
    infrastructure_level = 1,
    dimensional_gate = 0,
    time_acceleration = 0,
    resource_multiplication = 0,
    auto_cultivation = 0,
    total_upgrades = 0,
    successful_defenses = 0,
    special_events_count = 0
WHERE world_level IS NULL;
