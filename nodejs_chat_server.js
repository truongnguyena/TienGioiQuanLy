#!/usr/bin/env node
// Node.js Real-time Chat Server for Tu Tien AI Girl
const express = require('express');
const http = require('http');
const socketIo = require('socket.io');
const cors = require('cors');
const axios = require('axios');
const fs = require('fs');
const path = require('path');

class TuTienChatServer {
    constructor() {
        this.app = express();
        this.server = http.createServer(this.app);
        this.io = socketIo(this.server, {
            cors: {
                origin: "*",
                methods: ["GET", "POST"]
            }
        });
        
        this.port = process.env.PORT || 3000;
        this.pythonApiUrl = process.env.PYTHON_API_URL || 'http://localhost:5000';
        this.rubyApiUrl = process.env.RUBY_API_URL || 'http://localhost:4567';
        this.javaApiUrl = process.env.JAVA_API_URL || 'http://localhost:8080';
        this.csharpApiUrl = process.env.CSHARP_API_URL || 'http://localhost:5001';
        
        this.connectedUsers = new Map();
        this.chatHistory = [];
        this.aiPersonality = {
            name: "Linh Nhi",
            cultivationLevel: "Nguyên Anh Tầng 3",
            personality: {
                kindness: 95,
                wisdom: 88,
                playfulness: 75,
                mysteriousness: 80,
                helpfulness: 92
            }
        };
        
        this.setupMiddleware();
        this.setupRoutes();
        this.setupSocketHandlers();
        this.setupAIServices();
    }
    
    setupMiddleware() {
        this.app.use(cors());
        this.app.use(express.json());
        this.app.use(express.static('public'));
        
        // Logging middleware
        this.app.use((req, res, next) => {
            console.log(`${new Date().toISOString()} - ${req.method} ${req.path}`);
            next();
        });
    }
    
    setupRoutes() {
        // Health check
        this.app.get('/health', (req, res) => {
            res.json({
                status: 'healthy',
                timestamp: new Date().toISOString(),
                services: {
                    nodejs: 'running',
                    python: this.checkServiceStatus('python'),
                    ruby: this.checkServiceStatus('ruby'),
                    java: this.checkServiceStatus('java'),
                    csharp: this.checkServiceStatus('csharp')
                }
            });
        });
        
        // Get AI status
        this.app.get('/api/ai/status', (req, res) => {
            res.json({
                ai: this.aiPersonality,
                connectedUsers: this.connectedUsers.size,
                chatHistory: this.chatHistory.length
            });
        });
        
        // Get chat history
        this.app.get('/api/chat/history', (req, res) => {
            const limit = parseInt(req.query.limit) || 50;
            res.json(this.chatHistory.slice(-limit));
        });
        
        // Send message to AI
        this.app.post('/api/chat/send', async (req, res) => {
            try {
                const { message, userId, context } = req.body;
                const response = await this.processAIMessage(message, userId, context);
                res.json(response);
            } catch (error) {
                console.error('Error processing message:', error);
                res.status(500).json({ error: 'Failed to process message' });
            }
        });
        
        // Get AI personality
        this.app.get('/api/ai/personality', (req, res) => {
            res.json(this.aiPersonality);
        });
        
        // Update AI personality
        this.app.post('/api/ai/personality', (req, res) => {
            const { personality } = req.body;
            if (personality) {
                this.aiPersonality.personality = { ...this.aiPersonality.personality, ...personality };
                this.broadcastPersonalityUpdate();
                res.json({ success: true, personality: this.aiPersonality.personality });
            } else {
                res.status(400).json({ error: 'Invalid personality data' });
            }
        });
    }
    
    setupSocketHandlers() {
        this.io.on('connection', (socket) => {
            console.log(`User connected: ${socket.id}`);
            
            // User joins chat
            socket.on('join_chat', (userData) => {
                this.connectedUsers.set(socket.id, {
                    id: socket.id,
                    username: userData.username || 'Anonymous',
                    cultivationLevel: userData.cultivationLevel || 'Luyện Khí Tầng 1',
                    joinTime: new Date().toISOString()
                });
                
                socket.emit('ai_greeting', this.generateAIGreeting(userData));
                socket.broadcast.emit('user_joined', {
                    username: userData.username,
                    message: `${userData.username} đã tham gia cuộc trò chuyện!`
                });
            });
            
            // User sends message
            socket.on('send_message', async (data) => {
                try {
                    const { message, context } = data;
                    const user = this.connectedUsers.get(socket.id);
                    
                    if (!user) {
                        socket.emit('error', { message: 'User not found' });
                        return;
                    }
                    
                    // Add to chat history
                    const chatMessage = {
                        id: Date.now().toString(),
                        userId: socket.id,
                        username: user.username,
                        message: message,
                        timestamp: new Date().toISOString(),
                        type: 'user'
                    };
                    
                    this.chatHistory.push(chatMessage);
                    
                    // Broadcast user message
                    this.io.emit('user_message', chatMessage);
                    
                    // Process with AI
                    const aiResponse = await this.processAIMessage(message, socket.id, context);
                    
                    // Add AI response to chat history
                    const aiMessage = {
                        id: (Date.now() + 1).toString(),
                        userId: 'ai',
                        username: this.aiPersonality.name,
                        message: aiResponse.text,
                        timestamp: new Date().toISOString(),
                        type: 'ai',
                        aiData: {
                            mood: aiResponse.mood,
                            cultivationLevel: aiResponse.cultivation_level,
                            specialAbility: aiResponse.special_ability,
                            wisdomLevel: aiResponse.wisdom_level
                        }
                    };
                    
                    this.chatHistory.push(aiMessage);
                    
                    // Broadcast AI response
                    this.io.emit('ai_message', aiMessage);
                    
                } catch (error) {
                    console.error('Error handling message:', error);
                    socket.emit('error', { message: 'Failed to process message' });
                }
            });
            
            // User requests AI status
            socket.on('get_ai_status', () => {
                socket.emit('ai_status', {
                    ai: this.aiPersonality,
                    connectedUsers: this.connectedUsers.size,
                    chatHistory: this.chatHistory.length
                });
            });
            
            // User disconnects
            socket.on('disconnect', () => {
                const user = this.connectedUsers.get(socket.id);
                if (user) {
                    this.connectedUsers.delete(socket.id);
                    socket.broadcast.emit('user_left', {
                        username: user.username,
                        message: `${user.username} đã rời khỏi cuộc trò chuyện!`
                    });
                }
                console.log(`User disconnected: ${socket.id}`);
            });
        });
    }
    
    setupAIServices() {
        // Initialize AI services
        this.aiServices = {
            python: this.pythonApiUrl,
            ruby: this.rubyApiUrl,
            java: this.javaApiUrl,
            csharp: this.csharpApiUrl
        };
    }
    
    async processAIMessage(message, userId, context = {}) {
        try {
            // Try Python AI first
            const pythonResponse = await this.callPythonAI(message, context);
            if (pythonResponse) {
                return pythonResponse;
            }
            
            // Fallback to Ruby AI
            const rubyResponse = await this.callRubyAI(message, context);
            if (rubyResponse) {
                return rubyResponse;
            }
            
            // Fallback to Java AI
            const javaResponse = await this.callJavaAI(message, context);
            if (javaResponse) {
                return javaResponse;
            }
            
            // Fallback to C# AI
            const csharpResponse = await this.callCSharpAI(message, context);
            if (csharpResponse) {
                return csharpResponse;
            }
            
            // Default response if all services fail
            return this.getDefaultResponse(message);
            
        } catch (error) {
            console.error('Error processing AI message:', error);
            return this.getDefaultResponse(message);
        }
    }
    
    async callPythonAI(message, context) {
        try {
            const response = await axios.post(`${this.pythonApiUrl}/api/ai/chat`, {
                message: message,
                context: context,
                ai_type: 'tutien_girl'
            }, { timeout: 5000 });
            
            return response.data;
        } catch (error) {
            console.error('Python AI error:', error.message);
            return null;
        }
    }
    
    async callRubyAI(message, context) {
        try {
            const response = await axios.post(`${this.rubyApiUrl}/api/v1/ai/chat`, {
                message: message,
                context: context,
                ai_type: 'tutien_girl'
            }, { timeout: 5000 });
            
            return response.data;
        } catch (error) {
            console.error('Ruby AI error:', error.message);
            return null;
        }
    }
    
    async callJavaAI(message, context) {
        try {
            const response = await axios.post(`${this.javaApiUrl}/api/ai/chat`, {
                message: message,
                context: context,
                ai_type: 'tutien_girl'
            }, { timeout: 5000 });
            
            return response.data;
        } catch (error) {
            console.error('Java AI error:', error.message);
            return null;
        }
    }
    
    async callCSharpAI(message, context) {
        try {
            const response = await axios.post(`${this.csharpApiUrl}/api/ai/chat`, {
                message: message,
                context: context,
                ai_type: 'tutien_girl'
            }, { timeout: 5000 });
            
            return response.data;
        } catch (error) {
            console.error('C# AI error:', error.message);
            return null;
        }
    }
    
    getDefaultResponse(message) {
        const responses = [
            "Xin lỗi! Linh Nhi đang gặp chút khó khăn. Hãy thử lại sau nhé! 😅",
            "Linh Nhi đang tập trung tu luyện, hãy đợi một chút! 🧘‍♀️",
            "Có vẻ như có gì đó không ổn. Linh Nhi sẽ cố gắng hơn! 💪",
            "Linh Nhi đang suy nghĩ... Hãy cho Linh Nhi thêm thời gian! 🤔",
            "Linh Nhi cảm thấy hơi mệt. Hãy thử lại sau nhé! 😴"
        ];
        
        return {
            text: responses[Math.floor(Math.random() * responses.length)],
            type: 'default',
            mood: 'confused',
            cultivation_level: this.aiPersonality.cultivationLevel,
            special_ability: 'Đọc tâm ý người khác',
            wisdom_level: 88,
            mystery_level: 80,
            timestamp: new Date().toISOString(),
            ai_name: this.aiPersonality.name
        };
    }
    
    generateAIGreeting(userData) {
        const greetings = [
            `Chào ${userData.username}! Linh Nhi rất vui được gặp bạn! ✨`,
            `Xin chào ${userData.username}! Hãy để Linh Nhi giúp đỡ bạn! 🌸`,
            `Chào ${userData.username}! Linh Nhi hy vọng có thể chia sẻ kiến thức tu tiên với bạn! 💫`,
            `Xin chào ${userData.username}! Linh Nhi đã chờ đợi cuộc trò chuyện này! 🌺`,
            `Chào ${userData.username}! Linh Nhi sẵn sàng hỗ trợ bạn trong hành trình tu tiên! 🌟`
        ];
        
        return {
            text: greetings[Math.floor(Math.random() * greetings.length)],
            type: 'greeting',
            mood: 'happy',
            cultivation_level: this.aiPersonality.cultivationLevel,
            special_ability: 'Đọc tâm ý người khác',
            wisdom_level: 88,
            mystery_level: 80,
            timestamp: new Date().toISOString(),
            ai_name: this.aiPersonality.name
        };
    }
    
    checkServiceStatus(service) {
        // This would check if the service is actually running
        // For now, return 'unknown'
        return 'unknown';
    }
    
    broadcastPersonalityUpdate() {
        this.io.emit('ai_personality_updated', {
            personality: this.aiPersonality.personality,
            timestamp: new Date().toISOString()
        });
    }
    
    start() {
        this.server.listen(this.port, () => {
            console.log(`🚀 Tu Tien Chat Server running on port ${this.port}`);
            console.log(`🤖 AI Girl: ${this.aiPersonality.name} (${this.aiPersonality.cultivationLevel})`);
            console.log(`🌐 WebSocket server ready for connections`);
            console.log(`📡 Connected to services:`);
            console.log(`   - Python AI: ${this.pythonApiUrl}`);
            console.log(`   - Ruby AI: ${this.rubyApiUrl}`);
            console.log(`   - Java AI: ${this.javaApiUrl}`);
            console.log(`   - C# AI: ${this.csharpApiUrl}`);
        });
    }
}

// Start server
const server = new TuTienChatServer();
server.start();

module.exports = TuTienChatServer;
