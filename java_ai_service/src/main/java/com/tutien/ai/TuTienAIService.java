package com.tutien.ai;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.bind.annotation.*;
import org.springframework.http.ResponseEntity;
import org.springframework.http.HttpStatus;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.annotation.JsonProperty;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.*;
import java.util.concurrent.ThreadLocalRandom;

@SpringBootApplication
@RestController
@RequestMapping("/api/ai")
@CrossOrigin(origins = "*")
public class TuTienAIService {
    
    private final ObjectMapper objectMapper = new ObjectMapper();
    private final TuTienAIPersonality aiPersonality;
    private final List<ChatMemory> chatMemories = new ArrayList<>();
    
    public TuTienAIService() {
        this.aiPersonality = new TuTienAIPersonality();
    }
    
    public static void main(String[] args) {
        SpringApplication.run(TuTienAIService.class, args);
    }
    
    @GetMapping("/health")
    public ResponseEntity<Map<String, Object>> health() {
        Map<String, Object> response = new HashMap<>();
        response.put("status", "healthy");
        response.put("timestamp", LocalDateTime.now().format(DateTimeFormatter.ISO_LOCAL_DATE_TIME));
        response.put("service", "Java AI Service");
        response.put("ai_name", aiPersonality.getName());
        response.put("cultivation_level", aiPersonality.getCultivationLevel());
        return ResponseEntity.ok(response);
    }
    
    @PostMapping("/chat")
    public ResponseEntity<AIResponse> chat(@RequestBody ChatRequest request) {
        try {
            AIResponse response = processMessage(request.getMessage(), request.getContext());
            return ResponseEntity.ok(response);
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                .body(createErrorResponse("Failed to process message: " + e.getMessage()));
        }
    }
    
    @GetMapping("/personality")
    public ResponseEntity<TuTienAIPersonality> getPersonality() {
        return ResponseEntity.ok(aiPersonality);
    }
    
    @PostMapping("/personality")
    public ResponseEntity<Map<String, Object>> updatePersonality(@RequestBody Map<String, Object> updates) {
        try {
            aiPersonality.updatePersonality(updates);
            Map<String, Object> response = new HashMap<>();
            response.put("success", true);
            response.put("personality", aiPersonality);
            response.put("timestamp", LocalDateTime.now().format(DateTimeFormatter.ISO_LOCAL_DATE_TIME));
            return ResponseEntity.ok(response);
        } catch (Exception e) {
            Map<String, Object> response = new HashMap<>();
            response.put("success", false);
            response.put("error", e.getMessage());
            return ResponseEntity.badRequest().body(response);
        }
    }
    
    @GetMapping("/memories")
    public ResponseEntity<List<ChatMemory>> getMemories() {
        return ResponseEntity.ok(chatMemories);
    }
    
    @PostMapping("/memories/clear")
    public ResponseEntity<Map<String, Object>> clearMemories() {
        chatMemories.clear();
        Map<String, Object> response = new HashMap<>();
        response.put("success", true);
        response.put("message", "Memories cleared");
        response.put("timestamp", LocalDateTime.now().format(DateTimeFormatter.ISO_LOCAL_DATE_TIME));
        return ResponseEntity.ok(response);
    }
    
    private AIResponse processMessage(String message, Map<String, Object> context) {
        // Analyze message
        MessageAnalysis analysis = analyzeMessage(message);
        
        // Determine response type
        String responseType = determineResponseType(analysis);
        
        // Generate response
        String responseText = generateResponse(message, analysis, responseType, context);
        
        // Create AI response
        AIResponse response = new AIResponse();
        response.setText(responseText);
        response.setType(responseType);
        response.setMood(aiPersonality.getCurrentMood());
        response.setCultivationLevel(aiPersonality.getCultivationLevel());
        response.setSpecialAbility(aiPersonality.getRandomSpecialAbility());
        response.setWisdomLevel(aiPersonality.getWisdomLevel());
        response.setMysteryLevel(aiPersonality.getMysteryLevel());
        response.setTimestamp(LocalDateTime.now().format(DateTimeFormatter.ISO_LOCAL_DATE_TIME));
        response.setAiName(aiPersonality.getName());
        
        // Update personality based on message
        aiPersonality.updateMood(analysis);
        
        // Store memory
        storeMemory(message, response);
        
        return response;
    }
    
    private MessageAnalysis analyzeMessage(String message) {
        String lowerMessage = message.toLowerCase();
        
        MessageAnalysis analysis = new MessageAnalysis();
        analysis.setCultivationQuestion(containsKeywords(lowerMessage, 
            Arrays.asList("tu luyện", "cảnh giới", "linh lực", "đan dược", "pháp bảo")));
        analysis.setHelpRequest(containsKeywords(lowerMessage, 
            Arrays.asList("giúp", "hỗ trợ", "làm sao", "cách nào", "hướng dẫn")));
        analysis.setEmotional(containsKeywords(lowerMessage, 
            Arrays.asList("buồn", "vui", "lo lắng", "sợ hãi", "tức giận", "hạnh phúc")));
        analysis.setGreeting(containsKeywords(lowerMessage, 
            Arrays.asList("chào", "xin chào", "hello", "hi", "chào bạn")));
        analysis.setSentiment(analyzeSentiment(message));
        analysis.setUrgency(analyzeUrgency(message));
        
        return analysis;
    }
    
    private boolean containsKeywords(String message, List<String> keywords) {
        return keywords.stream().anyMatch(message::contains);
    }
    
    private String analyzeSentiment(String message) {
        String lowerMessage = message.toLowerCase();
        List<String> positiveWords = Arrays.asList("vui", "hạnh phúc", "tuyệt", "tốt", "hay", "thích", "yêu");
        List<String> negativeWords = Arrays.asList("buồn", "tức giận", "lo lắng", "sợ", "xấu", "ghét", "khó");
        
        long positiveCount = positiveWords.stream().mapToLong(word -> 
            lowerMessage.split(word, -1).length - 1).sum();
        long negativeCount = negativeWords.stream().mapToLong(word -> 
            lowerMessage.split(word, -1).length - 1).sum();
        
        if (positiveCount > negativeCount) return "positive";
        if (negativeCount > positiveCount) return "negative";
        return "neutral";
    }
    
    private String analyzeUrgency(String message) {
        String lowerMessage = message.toLowerCase();
        List<String> urgentWords = Arrays.asList("khẩn cấp", "gấp", "ngay", "nhanh", "cứu", "giúp");
        
        if (urgentWords.stream().anyMatch(lowerMessage::contains)) return "high";
        if (message.contains("?") || message.contains("!")) return "medium";
        return "low";
    }
    
    private String determineResponseType(MessageAnalysis analysis) {
        if (analysis.isGreeting()) return "greeting";
        if (analysis.isCultivationQuestion()) return "cultivation_advice";
        if (analysis.isHelpRequest()) return "helpful_guidance";
        if (analysis.isEmotional()) return "emotional_support";
        if ("high".equals(analysis.getUrgency())) return "urgent_help";
        return "general_chat";
    }
    
    private String generateResponse(String message, MessageAnalysis analysis, String responseType, Map<String, Object> context) {
        String username = context != null ? (String) context.get("username") : "bạn";
        
        switch (responseType) {
            case "greeting":
                return generateGreetingResponse(username);
            case "cultivation_advice":
                return generateCultivationResponse(username);
            case "helpful_guidance":
                return generateGuidanceResponse(username);
            case "emotional_support":
                return generateEmotionalResponse(username);
            case "urgent_help":
                return generateUrgentResponse(username);
            default:
                return generateGeneralResponse(username);
        }
    }
    
    private String generateGreetingResponse(String username) {
        List<String> responses = Arrays.asList(
            String.format("Chào %s! %s đây, rất vui được gặp bạn trong thế giới tu tiên này! ✨", username, aiPersonality.getName()),
            String.format("Xin chào %s! %s cảm thấy rất hạnh phúc khi được trò chuyện với bạn! 🌸", username, aiPersonality.getName()),
            String.format("Chào %s! Hôm nay %s có thể giúp gì cho bạn không? 💫", username, aiPersonality.getName()),
            String.format("Xin chào %s! %s đã chờ đợi cuộc trò chuyện này rồi! 🌺", username, aiPersonality.getName()),
            String.format("Chào %s! %s hy vọng có thể chia sẻ kiến thức tu tiên với bạn! 🌟", username, aiPersonality.getName())
        );
        return responses.get(ThreadLocalRandom.current().nextInt(responses.size()));
    }
    
    private String generateCultivationResponse(String username) {
        List<String> responses = Arrays.asList(
            String.format("Tu luyện là một hành trình dài và đầy thử thách. %s sẽ hướng dẫn bạn từng bước! 🧘‍♀️", aiPersonality.getName()),
            String.format("Để đạt được cảnh giới cao hơn, bạn cần kiên trì và có tâm hồn trong sáng. %s tin bạn làm được! ✨", aiPersonality.getName()),
            String.format("Tu luyện không chỉ là tăng linh lực mà còn là tu tâm. %s sẽ giúp bạn hiểu sâu hơn! 🌸", aiPersonality.getName()),
            String.format("Mỗi cảnh giới đều có ý nghĩa riêng. %s sẽ giải thích chi tiết cho bạn! 💫", aiPersonality.getName()),
            String.format("Tu luyện cần sự kiên nhẫn và quyết tâm. %s sẽ đồng hành cùng bạn! 🌺", aiPersonality.getName())
        );
        return responses.get(ThreadLocalRandom.current().nextInt(responses.size()));
    }
    
    private String generateGuidanceResponse(String username) {
        List<String> responses = Arrays.asList(
            String.format("%s rất vui được giúp đỡ bạn! Hãy cho %s biết bạn cần hỗ trợ gì nhé! 🤗", aiPersonality.getName(), aiPersonality.getName()),
            String.format("Đừng lo lắng! %s sẽ tìm cách giúp bạn giải quyết vấn đề này! 💪", aiPersonality.getName()),
            String.format("%s hiểu bạn đang gặp khó khăn. Hãy cùng nhau tìm giải pháp nhé! 🌟", aiPersonality.getName()),
            String.format("Với kinh nghiệm tu luyện của mình, %s sẽ hướng dẫn bạn cách tốt nhất! ✨", aiPersonality.getName()),
            String.format("Bạn không cô đơn đâu! %s luôn sẵn sàng hỗ trợ bạn! 🌸", aiPersonality.getName())
        );
        return responses.get(ThreadLocalRandom.current().nextInt(responses.size()));
    }
    
    private String generateEmotionalResponse(String username) {
        List<String> responses = Arrays.asList(
            String.format("%s cảm nhận được cảm xúc của bạn. Hãy để %s an ủi bạn nhé! 🤗", aiPersonality.getName(), aiPersonality.getName()),
            String.format("Cảm xúc là một phần quan trọng của tu luyện. %s sẽ giúp bạn hiểu rõ hơn! 💫", aiPersonality.getName()),
            String.format("Đừng buồn! %s sẽ dùng phép thuật để làm bạn vui lên! ✨", aiPersonality.getName()),
            String.format("Tâm hồn bạn đang cần được chữa lành. %s sẽ giúp bạn! 🌸", aiPersonality.getName()),
            String.format("%s hiểu bạn đang trải qua khó khăn. Hãy tin tưởng vào bản thân! 🌟", aiPersonality.getName())
        );
        return responses.get(ThreadLocalRandom.current().nextInt(responses.size()));
    }
    
    private String generateUrgentResponse(String username) {
        List<String> responses = Arrays.asList(
            String.format("%s cảm nhận được sự khẩn cấp! Hãy nói cho %s biết vấn đề gì đang xảy ra! 🚨", aiPersonality.getName(), aiPersonality.getName()),
            String.format("Đừng hoảng sợ! %s sẽ giúp bạn ngay lập tức! 💪", aiPersonality.getName()),
            String.format("%s đang tập trung toàn bộ linh lực để hỗ trợ bạn! ⚡", aiPersonality.getName()),
            String.format("Hãy bình tĩnh và cho %s biết chi tiết! %s sẽ tìm giải pháp! 🌟", aiPersonality.getName(), aiPersonality.getName()),
            String.format("%s sẵn sàng sử dụng tất cả khả năng để giúp bạn! ✨", aiPersonality.getName())
        );
        return responses.get(ThreadLocalRandom.current().nextInt(responses.size()));
    }
    
    private String generateGeneralResponse(String username) {
        List<String> responses = Arrays.asList(
            String.format("%s rất thích trò chuyện với bạn! Bạn có muốn nghe %s kể về thế giới tu tiên không? 🌸", aiPersonality.getName(), aiPersonality.getName()),
            String.format("Cuộc trò chuyện này thật thú vị! %s hy vọng có thể học hỏi thêm từ bạn! 💫", aiPersonality.getName()),
            String.format("%s cảm thấy rất vui khi được giao lưu với bạn! Bạn có câu hỏi gì không? ✨", aiPersonality.getName()),
            String.format("Thế giới tu tiên có rất nhiều điều kỳ diệu! %s muốn chia sẻ với bạn! 🌟", aiPersonality.getName()),
            String.format("%s luôn sẵn sàng lắng nghe và chia sẻ! Bạn có muốn tìm hiểu gì không? 🌺", aiPersonality.getName())
        );
        return responses.get(ThreadLocalRandom.current().nextInt(responses.size()));
    }
    
    private void storeMemory(String userMessage, AIResponse aiResponse) {
        ChatMemory memory = new ChatMemory();
        memory.setTimestamp(LocalDateTime.now().format(DateTimeFormatter.ISO_LOCAL_DATE_TIME));
        memory.setUserMessage(userMessage);
        memory.setAiResponse(aiResponse.getText());
        memory.setMood(aiPersonality.getCurrentMood());
        
        chatMemories.add(memory);
        
        // Keep only last 100 memories
        if (chatMemories.size() > 100) {
            chatMemories.remove(0);
        }
    }
    
    private AIResponse createErrorResponse(String errorMessage) {
        AIResponse response = new AIResponse();
        response.setText(String.format("Xin lỗi! %s gặp chút khó khăn. Hãy thử lại sau nhé! 😅", aiPersonality.getName()));
        response.setType("error");
        response.setMood("confused");
        response.setCultivationLevel(aiPersonality.getCultivationLevel());
        response.setTimestamp(LocalDateTime.now().format(DateTimeFormatter.ISO_LOCAL_DATE_TIME));
        response.setAiName(aiPersonality.getName());
        return response;
    }
    
    // Inner classes for data structures
    public static class ChatRequest {
        @JsonProperty("message")
        private String message;
        
        @JsonProperty("context")
        private Map<String, Object> context;
        
        // Getters and setters
        public String getMessage() { return message; }
        public void setMessage(String message) { this.message = message; }
        public Map<String, Object> getContext() { return context; }
        public void setContext(Map<String, Object> context) { this.context = context; }
    }
    
    public static class AIResponse {
        @JsonProperty("text")
        private String text;
        
        @JsonProperty("type")
        private String type;
        
        @JsonProperty("mood")
        private String mood;
        
        @JsonProperty("cultivation_level")
        private String cultivationLevel;
        
        @JsonProperty("special_ability")
        private String specialAbility;
        
        @JsonProperty("wisdom_level")
        private int wisdomLevel;
        
        @JsonProperty("mystery_level")
        private int mysteryLevel;
        
        @JsonProperty("timestamp")
        private String timestamp;
        
        @JsonProperty("ai_name")
        private String aiName;
        
        // Getters and setters
        public String getText() { return text; }
        public void setText(String text) { this.text = text; }
        public String getType() { return type; }
        public void setType(String type) { this.type = type; }
        public String getMood() { return mood; }
        public void setMood(String mood) { this.mood = mood; }
        public String getCultivationLevel() { return cultivationLevel; }
        public void setCultivationLevel(String cultivationLevel) { this.cultivationLevel = cultivationLevel; }
        public String getSpecialAbility() { return specialAbility; }
        public void setSpecialAbility(String specialAbility) { this.specialAbility = specialAbility; }
        public int getWisdomLevel() { return wisdomLevel; }
        public void setWisdomLevel(int wisdomLevel) { this.wisdomLevel = wisdomLevel; }
        public int getMysteryLevel() { return mysteryLevel; }
        public void setMysteryLevel(int mysteryLevel) { this.mysteryLevel = mysteryLevel; }
        public String getTimestamp() { return timestamp; }
        public void setTimestamp(String timestamp) { this.timestamp = timestamp; }
        public String getAiName() { return aiName; }
        public void setAiName(String aiName) { this.aiName = aiName; }
    }
    
    public static class MessageAnalysis {
        private boolean cultivationQuestion;
        private boolean helpRequest;
        private boolean emotional;
        private boolean greeting;
        private String sentiment;
        private String urgency;
        
        // Getters and setters
        public boolean isCultivationQuestion() { return cultivationQuestion; }
        public void setCultivationQuestion(boolean cultivationQuestion) { this.cultivationQuestion = cultivationQuestion; }
        public boolean isHelpRequest() { return helpRequest; }
        public void setHelpRequest(boolean helpRequest) { this.helpRequest = helpRequest; }
        public boolean isEmotional() { return emotional; }
        public void setEmotional(boolean emotional) { this.emotional = emotional; }
        public boolean isGreeting() { return greeting; }
        public void setGreeting(boolean greeting) { this.greeting = greeting; }
        public String getSentiment() { return sentiment; }
        public void setSentiment(String sentiment) { this.sentiment = sentiment; }
        public String getUrgency() { return urgency; }
        public void setUrgency(String urgency) { this.urgency = urgency; }
    }
    
    public static class ChatMemory {
        private String timestamp;
        private String userMessage;
        private String aiResponse;
        private String mood;
        
        // Getters and setters
        public String getTimestamp() { return timestamp; }
        public void setTimestamp(String timestamp) { this.timestamp = timestamp; }
        public String getUserMessage() { return userMessage; }
        public void setUserMessage(String userMessage) { this.userMessage = userMessage; }
        public String getAiResponse() { return aiResponse; }
        public void setAiResponse(String aiResponse) { this.aiResponse = aiResponse; }
        public String getMood() { return mood; }
        public void setMood(String mood) { this.mood = mood; }
    }
}
