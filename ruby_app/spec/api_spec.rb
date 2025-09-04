# API tests for Tu Tien Community Platform
require 'spec_helper'

RSpec.describe 'Tu Tien Community API' do
  describe 'Health Check' do
    it 'returns healthy status' do
      response = make_api_request(:get, '/health')
      expect(response.code).to eq(200)
      
      data = JSON.parse(response.body)
      expect(data['status']).to eq('healthy')
      expect(data['services']).to have_key('database')
      expect(data['services']).to have_key('redis')
      expect(data['services']).to have_key('python_api')
    end
  end

  describe 'Users API' do
    describe 'GET /api/v1/users' do
      it 'returns empty list when no users exist' do
        response = make_api_request(:get, '/api/v1/users')
        expect_successful_response(response)
        
        data = JSON.parse(response.body)
        expect(data['data']).to be_empty
        expect(data['count']).to eq(0)
      end

      it 'returns users when they exist' do
        user1 = create_test_user(username: 'user1', email: 'user1@example.com')
        user2 = create_test_user(username: 'user2', email: 'user2@example.com')
        
        response = make_api_request(:get, '/api/v1/users')
        expect_successful_response(response)
        
        data = JSON.parse(response.body)
        expect(data['data'].length).to eq(2)
        expect(data['count']).to eq(2)
      end
    end

    describe 'GET /api/v1/users/:id' do
      it 'returns user when found' do
        user = create_test_user(username: 'testuser', email: 'test@example.com')
        
        response = make_api_request(:get, "/api/v1/users/#{user[:id]}")
        expect_successful_response(response)
        
        data = JSON.parse(response.body)
        expect(data['data']['username']).to eq('testuser')
        expect(data['data']['email']).to eq('test@example.com')
      end

      it 'returns 404 when user not found' do
        response = make_api_request(:get, '/api/v1/users/999')
        expect_error_response(response, 404)
      end
    end

    describe 'POST /api/v1/users' do
      it 'creates a new user' do
        user_data = {
          username: 'newuser',
          email: 'newuser@example.com',
          password_hash: 'hashed_password',
          cultivation_level: 'Luyện Khí Tầng 1',
          spiritual_power: 100
        }
        
        response = make_api_request(:post, '/api/v1/users', user_data)
        expect_successful_response(response)
        
        data = JSON.parse(response.body)
        expect(data['data']).to have_key('id')
        expect(data['message']).to eq('User created successfully')
      end

      it 'returns error for invalid data' do
        invalid_data = { username: 'test' } # Missing required fields
        
        response = make_api_request(:post, '/api/v1/users', invalid_data)
        expect_error_response(response, 400)
      end
    end
  end

  describe 'Guilds API' do
    describe 'GET /api/v1/guilds' do
      it 'returns empty list when no guilds exist' do
        response = make_api_request(:get, '/api/v1/guilds')
        expect_successful_response(response)
        
        data = JSON.parse(response.body)
        expect(data['data']).to be_empty
        expect(data['count']).to eq(0)
      end

      it 'returns guilds when they exist' do
        guild1 = create_test_guild(name: 'Guild 1')
        guild2 = create_test_guild(name: 'Guild 2')
        
        response = make_api_request(:get, '/api/v1/guilds')
        expect_successful_response(response)
        
        data = JSON.parse(response.body)
        expect(data['data'].length).to eq(2)
        expect(data['count']).to eq(2)
      end
    end

    describe 'GET /api/v1/guilds/:id' do
      it 'returns guild with members when found' do
        guild = create_test_guild(name: 'Test Guild')
        user = create_test_user(guild_id: guild[:id])
        
        response = make_api_request(:get, "/api/v1/guilds/#{guild[:id]}")
        expect_successful_response(response)
        
        data = JSON.parse(response.body)
        expect(data['data']['name']).to eq('Test Guild')
        expect(data['data']['members']).to be_an(Array)
        expect(data['data']['members'].length).to eq(1)
      end

      it 'returns 404 when guild not found' do
        response = make_api_request(:get, '/api/v1/guilds/999')
        expect_error_response(response, 404)
      end
    end

    describe 'POST /api/v1/guilds' do
      it 'creates a new guild' do
        guild_data = {
          name: 'New Guild',
          description: 'A new guild',
          level: 1,
          treasury: 10000,
          recruitment_open: true,
          max_members: 20
        }
        
        response = make_api_request(:post, '/api/v1/guilds', guild_data)
        expect_successful_response(response)
        
        data = JSON.parse(response.body)
        expect(data['data']).to have_key('id')
        expect(data['message']).to eq('Guild created successfully')
      end
    end
  end

  describe 'Worlds API' do
    describe 'GET /api/v1/worlds' do
      it 'returns empty list when no worlds exist' do
        response = make_api_request(:get, '/api/v1/worlds')
        expect_successful_response(response)
        
        data = JSON.parse(response.body)
        expect(data['data']).to be_empty
        expect(data['count']).to eq(0)
      end

      it 'returns worlds when they exist' do
        world1 = create_test_world(name: 'World 1')
        world2 = create_test_world(name: 'World 2')
        
        response = make_api_request(:get, '/api/v1/worlds')
        expect_successful_response(response)
        
        data = JSON.parse(response.body)
        expect(data['data'].length).to eq(2)
        expect(data['count']).to eq(2)
      end
    end

    describe 'GET /api/v1/worlds/:id' do
      it 'returns world when found' do
        world = create_test_world(name: 'Test World')
        
        response = make_api_request(:get, "/api/v1/worlds/#{world[:id]}")
        expect_successful_response(response)
        
        data = JSON.parse(response.body)
        expect(data['data']['name']).to eq('Test World')
      end

      it 'returns 404 when world not found' do
        response = make_api_request(:get, '/api/v1/worlds/999')
        expect_error_response(response, 404)
      end
    end
  end

  describe 'Statistics API' do
    describe 'GET /api/v1/stats' do
      it 'returns statistics' do
        # Create some test data
        create_test_user
        create_test_guild
        create_test_world
        create_test_expedition
        create_test_achievement
        
        response = make_api_request(:get, '/api/v1/stats')
        expect_successful_response(response)
        
        data = JSON.parse(response.body)
        expect(data['data']).to have_key('total_users')
        expect(data['data']).to have_key('total_guilds')
        expect(data['data']).to have_key('total_worlds')
        expect(data['data']).to have_key('total_expeditions')
        expect(data['data']).to have_key('total_achievements')
      end
    end
  end

  describe 'Data Export API' do
    describe 'GET /api/v1/export/:table' do
      it 'exports users data' do
        create_test_user(username: 'exportuser', email: 'export@example.com')
        
        response = make_api_request(:get, '/api/v1/export/user')
        expect_successful_response(response)
        
        data = JSON.parse(response.body)
        expect(data['table']).to eq('user')
        expect(data['data']).to be_an(Array)
        expect(data['data'].length).to eq(1)
        expect(data['data'].first['username']).to eq('exportuser')
      end

      it 'returns error for invalid table' do
        response = make_api_request(:get, '/api/v1/export/invalid_table')
        expect_error_response(response, 400)
      end
    end
  end

  describe 'Data Import API' do
    describe 'POST /api/v1/import/:table' do
      it 'imports users data' do
        user_data = {
          username: 'importuser',
          email: 'import@example.com',
          password_hash: 'hashed_password',
          cultivation_level: 'Luyện Khí Tầng 1',
          spiritual_power: 100
        }
        
        response = make_api_request(:post, '/api/v1/import/user', user_data)
        expect_successful_response(response)
        
        data = JSON.parse(response.body)
        expect(data['message']).to eq('1 record imported to user')
      end

      it 'imports multiple records' do
        users_data = [
          {
            username: 'user1',
            email: 'user1@example.com',
            password_hash: 'hashed_password',
            cultivation_level: 'Luyện Khí Tầng 1',
            spiritual_power: 100
          },
          {
            username: 'user2',
            email: 'user2@example.com',
            password_hash: 'hashed_password',
            cultivation_level: 'Luyện Khí Tầng 2',
            spiritual_power: 200
          }
        ]
        
        response = make_api_request(:post, '/api/v1/import/user', users_data)
        expect_successful_response(response)
        
        data = JSON.parse(response.body)
        expect(data['message']).to eq('2 records imported to user')
      end

      it 'returns error for invalid table' do
        response = make_api_request(:post, '/api/v1/import/invalid_table', {})
        expect_error_response(response, 400)
      end
    end
  end
end
