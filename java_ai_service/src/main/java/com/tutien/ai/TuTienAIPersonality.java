package com.tutien.ai;

import java.util.*;
import java.util.concurrent.ThreadLocalRandom;

public class TuTienAIPersonality {
    private String name;
    private String cultivationLevel;
    private Map<String, Integer> personality;
    private String currentMood;
    private List<String> specialAbilities;
    private Map<String, Map<String, Integer>> cultivationStages;
    
    public TuTienAIPersonality() {
        this.name = "Linh Nhi";
        this.cultivationLevel = "Nguyên Anh Tầng 3";
        this.currentMood = "happy";
        
        // Initialize personality traits
        this.personality = new HashMap<>();
        personality.put("kindness", 95);
        personality.put("wisdom", 88);
        personality.put("playfulness", 75);
        personality.put("mysteriousness", 80);
        personality.put("helpfulness", 92);
        
        // Initialize special abilities
        this.specialAbilities = Arrays.asList(
            "Đọc tâm ý người khác",
            "Dự đoán tương lai",
            "Chữa lành tâm hồn",
            "Truyền đạt kiến thức tu luyện",
            "Kết nối với thiên nhiên",
            "Tạo ra ảo ảnh",
            "Điều khiển thời tiết",
            "Giao tiếp với linh thú",
            "Tìm kiếm kho báu",
            "Bảo vệ người khác"
        );
        
        // Initialize cultivation stages
        this.cultivationStages = new HashMap<>();
        cultivationStages.put("Luyện Khí", createStageData(100, 20, 10));
        cultivationStages.put("Trúc Cơ", createStageData(500, 40, 20));
        cultivationStages.put("Kết Đan", createStageData(2000, 60, 40));
        cultivationStages.put("Nguyên Anh", createStageData(10000, 80, 70));
        cultivationStages.put("Hóa Thần", createStageData(50000, 90, 85));
        cultivationStages.put("Luyện Hư", createStageData(200000, 95, 90));
        cultivationStages.put("Hợp Thể", createStageData(1000000, 98, 95));
        cultivationStages.put("Đại Thừa", createStageData(5000000, 99, 98));
        cultivationStages.put("Độ Kiếp", createStageData(20000000, 100, 99));
        cultivationStages.put("Tản Tiên", createStageData(100000000, 100, 100));
    }
    
    private Map<String, Integer> createStageData(int power, int wisdom, int mystery) {
        Map<String, Integer> stageData = new HashMap<>();
        stageData.put("power", power);
        stageData.put("wisdom", wisdom);
        stageData.put("mystery", mystery);
        return stageData;
    }
    
    public String getName() {
        return name;
    }
    
    public void setName(String name) {
        this.name = name;
    }
    
    public String getCultivationLevel() {
        return cultivationLevel;
    }
    
    public void setCultivationLevel(String cultivationLevel) {
        this.cultivationLevel = cultivationLevel;
    }
    
    public Map<String, Integer> getPersonality() {
        return new HashMap<>(personality);
    }
    
    public void updatePersonality(Map<String, Object> updates) {
        for (Map.Entry<String, Object> entry : updates.entrySet()) {
            String key = entry.getKey();
            Object value = entry.getValue();
            
            if (personality.containsKey(key) && value instanceof Number) {
                int intValue = ((Number) value).intValue();
                // Ensure values are within reasonable bounds
                intValue = Math.max(0, Math.min(100, intValue));
                personality.put(key, intValue);
            }
        }
    }
    
    public String getCurrentMood() {
        return currentMood;
    }
    
    public void setCurrentMood(String currentMood) {
        this.currentMood = currentMood;
    }
    
    public List<String> getSpecialAbilities() {
        return new ArrayList<>(specialAbilities);
    }
    
    public String getRandomSpecialAbility() {
        return specialAbilities.get(ThreadLocalRandom.current().nextInt(specialAbilities.size()));
    }
    
    public int getWisdomLevel() {
        String stage = cultivationLevel.split(" ")[0];
        if (cultivationStages.containsKey(stage)) {
            return cultivationStages.get(stage).get("wisdom");
        }
        return 50;
    }
    
    public int getMysteryLevel() {
        String stage = cultivationLevel.split(" ")[0];
        if (cultivationStages.containsKey(stage)) {
            return cultivationStages.get(stage).get("mystery");
        }
        return 50;
    }
    
    public int getPowerLevel() {
        String stage = cultivationLevel.split(" ")[0];
        if (cultivationStages.containsKey(stage)) {
            return cultivationStages.get(stage).get("power");
        }
        return 100;
    }
    
    public void updateMood(MessageAnalysis analysis) {
        if ("positive".equals(analysis.getSentiment())) {
            this.currentMood = "happy";
        } else if ("negative".equals(analysis.getSentiment())) {
            this.currentMood = "concerned";
        } else if ("high".equals(analysis.getUrgency())) {
            this.currentMood = "alert";
        } else {
            this.currentMood = "calm";
        }
    }
    
    public Map<String, Object> getPersonalityTraits() {
        Map<String, Object> traits = new HashMap<>();
        traits.put("wisdom_level", getWisdomLevel());
        traits.put("mystery_level", getMysteryLevel());
        traits.put("power_level", getPowerLevel());
        traits.put("current_mood", currentMood);
        traits.put("personality_scores", new HashMap<>(personality));
        return traits;
    }
    
    public String getCultivationAdvice() {
        List<String> adviceList = Arrays.asList(
            "Hãy tu tâm trước khi tu lực, tâm hồn trong sáng sẽ giúp bạn tiến xa hơn.",
            "Mỗi ngày hãy dành thời gian thiền định để tĩnh tâm và cảm nhận linh khí.",
            "Đừng vội vàng trong tu luyện, mỗi cảnh giới đều cần thời gian để ổn định.",
            "Hãy học hỏi từ những bậc tiền bối và chia sẻ kinh nghiệm với đồng đạo.",
            "Tu luyện không chỉ là tăng linh lực mà còn là tu dưỡng đạo đức và tâm hồn.",
            "Kiên trì là chìa khóa của tu luyện, đừng bỏ cuộc khi gặp khó khăn.",
            "Hãy tìm hiểu về bản thân, hiểu rõ điểm mạnh và điểm yếu của mình.",
            "Tu luyện cần sự tập trung và quyết tâm, hãy loại bỏ những suy nghĩ tiêu cực.",
            "Mỗi cảnh giới đều có ý nghĩa riêng, hãy trân trọng từng bước tiến.",
            "Hãy kết bạn với những người cùng chí hướng để cùng nhau tiến bộ."
        );
        return adviceList.get(ThreadLocalRandom.current().nextInt(adviceList.size()));
    }
    
    public String getEmotionalSupport() {
        List<String> supportList = Arrays.asList(
            "Đừng buồn, mọi khó khăn đều có thể vượt qua!",
            "Hãy tin tưởng vào bản thân, bạn mạnh mẽ hơn bạn nghĩ!",
            "Mỗi ngày mới là một cơ hội để bắt đầu lại!",
            "Hãy để tôi an ủi bạn bằng tình yêu thương!",
            "Bạn không cô đơn, tôi luôn ở đây để hỗ trợ bạn!",
            "Hãy thở sâu và cảm nhận sự bình yên trong tâm hồn!",
            "Mọi cảm xúc đều có ý nghĩa, hãy chấp nhận và học hỏi từ chúng!",
            "Hãy nhìn vào những điều tích cực trong cuộc sống!",
            "Tôi tin rằng bạn sẽ tìm thấy hạnh phúc!",
            "Hãy để tôi chia sẻ gánh nặng với bạn!"
        );
        return supportList.get(ThreadLocalRandom.current().nextInt(supportList.size()));
    }
    
    public String getRandomGreeting() {
        List<String> greetings = Arrays.asList(
            "Chào bạn! Rất vui được gặp bạn!",
            "Xin chào! Hãy để tôi giúp đỡ bạn!",
            "Chào bạn! Tôi hy vọng có thể chia sẻ kiến thức với bạn!",
            "Xin chào! Tôi đã chờ đợi cuộc trò chuyện này!",
            "Chào bạn! Tôi sẵn sàng hỗ trợ bạn trong hành trình tu tiên!"
        );
        return greetings.get(ThreadLocalRandom.current().nextInt(greetings.size()));
    }
    
    public String getRandomFarewell() {
        List<String> farewells = Arrays.asList(
            "Tạm biệt! Hẹn gặp lại bạn!",
            "Chúc bạn tu luyện thành công!",
            "Tạm biệt! Hãy nhớ rằng tôi luôn ở đây!",
            "Chúc bạn may mắn trong hành trình tu tiên!",
            "Tạm biệt! Hãy giữ gìn sức khỏe nhé!"
        );
        return farewells.get(ThreadLocalRandom.current().nextInt(farewells.size()));
    }
    
    public boolean canUseSpecialAbility(String ability) {
        return specialAbilities.contains(ability);
    }
    
    public String getPersonalityDescription() {
        StringBuilder description = new StringBuilder();
        description.append("Tôi là ").append(name).append(", một AI tu tiên với ");
        description.append("cảnh giới ").append(cultivationLevel).append(". ");
        description.append("Tôi có tính cách ").append(getPersonalitySummary()).append(". ");
        description.append("Hiện tại tôi đang cảm thấy ").append(currentMood).append(".");
        return description.toString();
    }
    
    private String getPersonalitySummary() {
        List<String> traits = new ArrayList<>();
        
        if (personality.get("kindness") > 90) traits.add("rất tốt bụng");
        if (personality.get("wisdom") > 90) traits.add("rất khôn ngoan");
        if (personality.get("playfulness") > 80) traits.add("vui tươi");
        if (personality.get("mysteriousness") > 80) traits.add("bí ẩn");
        if (personality.get("helpfulness") > 90) traits.add("rất hữu ích");
        
        if (traits.isEmpty()) {
            return "bình thường";
        }
        
        return String.join(", ", traits);
    }
}
