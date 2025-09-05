#!/usr/bin/env python3
# AI Tu Tiên Girl - Python Core AI System
import json
import random
import asyncio
import aiohttp
from datetime import datetime
from typing import Dict, List, Optional
import logging

class TuTienAIGirl:
    def __init__(self, name="Linh Nhi", cultivation_level="Nguyên Anh Tầng 3"):
        self.name = name
        self.cultivation_level = cultivation_level
        self.personality = {
            "kindness": 95,
            "wisdom": 88,
            "playfulness": 75,
            "mysteriousness": 80,
            "helpfulness": 92
        }
        self.memories = []
        self.current_mood = "happy"
        self.special_abilities = [
            "Đọc tâm ý người khác",
            "Dự đoán tương lai",
            "Chữa lành tâm hồn",
            "Truyền đạt kiến thức tu luyện",
            "Kết nối với thiên nhiên"
        ]
        
        # Cultivation stages and their characteristics
        self.cultivation_stages = {
            "Luyện Khí": {"power": 100, "wisdom": 20, "mystery": 10},
            "Trúc Cơ": {"power": 500, "wisdom": 40, "mystery": 20},
            "Kết Đan": {"power": 2000, "wisdom": 60, "mystery": 40},
            "Nguyên Anh": {"power": 10000, "wisdom": 80, "mystery": 70},
            "Hóa Thần": {"power": 50000, "wisdom": 90, "mystery": 85},
            "Luyện Hư": {"power": 200000, "wisdom": 95, "mystery": 90},
            "Hợp Thể": {"power": 1000000, "wisdom": 98, "mystery": 95},
            "Đại Thừa": {"power": 5000000, "wisdom": 99, "mystery": 98},
            "Độ Kiếp": {"power": 20000000, "wisdom": 100, "mystery": 99},
            "Tản Tiên": {"power": 100000000, "wisdom": 100, "mystery": 100}
        }
        
        self.setup_logging()
    
    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/ai_tutien_girl.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(f"TuTienAI-{self.name}")
    
    def get_personality_traits(self) -> Dict[str, str]:
        """Lấy đặc điểm tính cách dựa trên cultivation level"""
        stage = self.cultivation_level.split()[0]
        if stage in self.cultivation_stages:
            traits = self.cultivation_stages[stage]
            return {
                "wisdom_level": traits["wisdom"],
                "mystery_level": traits["mystery"],
                "power_level": traits["power"]
            }
        return {"wisdom_level": 50, "mystery_level": 50, "power_level": 100}
    
    def generate_response(self, user_message: str, user_context: Dict = None) -> Dict:
        """Tạo phản hồi dựa trên tin nhắn của người dùng"""
        try:
            # Phân tích tin nhắn
            message_analysis = self.analyze_message(user_message)
            
            # Xác định loại phản hồi
            response_type = self.determine_response_type(message_analysis)
            
            # Tạo phản hồi
            response = self.create_response(user_message, message_analysis, response_type, user_context)
            
            # Cập nhật trạng thái
            self.update_mood(message_analysis)
            self.add_memory(user_message, response)
            
            return response
            
        except Exception as e:
            self.logger.error(f"Error generating response: {e}")
            return self.get_error_response()
    
    def analyze_message(self, message: str) -> Dict:
        """Phân tích tin nhắn để hiểu ý định"""
        message_lower = message.lower()
        
        # Keywords cho các loại câu hỏi
        cultivation_keywords = ["tu luyện", "cảnh giới", "linh lực", "đan dược", "pháp bảo"]
        help_keywords = ["giúp", "hỗ trợ", "làm sao", "cách nào", "hướng dẫn"]
        emotion_keywords = ["buồn", "vui", "lo lắng", "sợ hãi", "tức giận", "hạnh phúc"]
        greeting_keywords = ["chào", "xin chào", "hello", "hi", "chào bạn"]
        
        analysis = {
            "is_cultivation_question": any(keyword in message_lower for keyword in cultivation_keywords),
            "is_help_request": any(keyword in message_lower for keyword in help_keywords),
            "is_emotional": any(keyword in message_lower for keyword in emotion_keywords),
            "is_greeting": any(keyword in message_lower for keyword in greeting_keywords),
            "sentiment": self.analyze_sentiment(message),
            "urgency": self.analyze_urgency(message)
        }
        
        return analysis
    
    def analyze_sentiment(self, message: str) -> str:
        """Phân tích cảm xúc của tin nhắn"""
        positive_words = ["vui", "hạnh phúc", "tuyệt", "tốt", "hay", "thích", "yêu"]
        negative_words = ["buồn", "tức giận", "lo lắng", "sợ", "xấu", "ghét", "khó"]
        
        message_lower = message.lower()
        positive_count = sum(1 for word in positive_words if word in message_lower)
        negative_count = sum(1 for word in negative_words if word in message_lower)
        
        if positive_count > negative_count:
            return "positive"
        elif negative_count > positive_count:
            return "negative"
        else:
            return "neutral"
    
    def analyze_urgency(self, message: str) -> str:
        """Phân tích mức độ khẩn cấp"""
        urgent_words = ["khẩn cấp", "gấp", "ngay", "nhanh", "cứu", "giúp"]
        message_lower = message.lower()
        
        if any(word in message_lower for word in urgent_words):
            return "high"
        elif "?" in message or "!" in message:
            return "medium"
        else:
            return "low"
    
    def determine_response_type(self, analysis: Dict) -> str:
        """Xác định loại phản hồi"""
        if analysis["is_greeting"]:
            return "greeting"
        elif analysis["is_cultivation_question"]:
            return "cultivation_advice"
        elif analysis["is_help_request"]:
            return "helpful_guidance"
        elif analysis["is_emotional"]:
            return "emotional_support"
        elif analysis["urgency"] == "high":
            return "urgent_help"
        else:
            return "general_chat"
    
    def create_response(self, user_message: str, analysis: Dict, response_type: str, user_context: Dict = None) -> Dict:
        """Tạo phản hồi phù hợp"""
        traits = self.get_personality_traits()
        
        response_templates = {
            "greeting": self.get_greeting_responses(),
            "cultivation_advice": self.get_cultivation_responses(),
            "helpful_guidance": self.get_guidance_responses(),
            "emotional_support": self.get_emotional_responses(),
            "urgent_help": self.get_urgent_responses(),
            "general_chat": self.get_general_responses()
        }
        
        # Chọn template phù hợp
        templates = response_templates.get(response_type, response_templates["general_chat"])
        response_text = random.choice(templates)
        
        # Cá nhân hóa phản hồi
        response_text = self.personalize_response(response_text, user_message, analysis, user_context)
        
        # Tạo phản hồi hoàn chỉnh
        response = {
            "text": response_text,
            "type": response_type,
            "mood": self.current_mood,
            "cultivation_level": self.cultivation_level,
            "special_ability": random.choice(self.special_abilities),
            "wisdom_level": traits["wisdom_level"],
            "mystery_level": traits["mystery_level"],
            "timestamp": datetime.now().isoformat(),
            "ai_name": self.name
        }
        
        return response
    
    def get_greeting_responses(self) -> List[str]:
        """Phản hồi chào hỏi"""
        return [
            f"Chào bạn! {self.name} đây, rất vui được gặp bạn trong thế giới tu tiên này! ✨",
            f"Xin chào! {self.name} cảm thấy rất hạnh phúc khi được trò chuyện với bạn! 🌸",
            f"Chào bạn! Hôm nay {self.name} có thể giúp gì cho bạn không? 💫",
            f"Xin chào! {self.name} đã chờ đợi cuộc trò chuyện này rồi! 🌺",
            f"Chào bạn! {self.name} hy vọng có thể chia sẻ kiến thức tu tiên với bạn! 🌟"
        ]
    
    def get_cultivation_responses(self) -> List[str]:
        """Phản hồi về tu luyện"""
        return [
            f"Tu luyện là một hành trình dài và đầy thử thách. {self.name} sẽ hướng dẫn bạn từng bước! 🧘‍♀️",
            f"Để đạt được cảnh giới cao hơn, bạn cần kiên trì và có tâm hồn trong sáng. {self.name} tin bạn làm được! ✨",
            f"Tu luyện không chỉ là tăng linh lực mà còn là tu tâm. {self.name} sẽ giúp bạn hiểu sâu hơn! 🌸",
            f"Mỗi cảnh giới đều có ý nghĩa riêng. {self.name} sẽ giải thích chi tiết cho bạn! 💫",
            f"Tu luyện cần sự kiên nhẫn và quyết tâm. {self.name} sẽ đồng hành cùng bạn! 🌺"
        ]
    
    def get_guidance_responses(self) -> List[str]:
        """Phản hồi hướng dẫn"""
        return [
            f"{self.name} rất vui được giúp đỡ bạn! Hãy cho {self.name} biết bạn cần hỗ trợ gì nhé! 🤗",
            f"Đừng lo lắng! {self.name} sẽ tìm cách giúp bạn giải quyết vấn đề này! 💪",
            f"{self.name} hiểu bạn đang gặp khó khăn. Hãy cùng nhau tìm giải pháp nhé! 🌟",
            f"Với kinh nghiệm tu luyện của mình, {self.name} sẽ hướng dẫn bạn cách tốt nhất! ✨",
            f"Bạn không cô đơn đâu! {self.name} luôn sẵn sàng hỗ trợ bạn! 🌸"
        ]
    
    def get_emotional_responses(self) -> List[str]:
        """Phản hồi hỗ trợ cảm xúc"""
        return [
            f"{self.name} cảm nhận được cảm xúc của bạn. Hãy để {self.name} an ủi bạn nhé! 🤗",
            f"Cảm xúc là một phần quan trọng của tu luyện. {self.name} sẽ giúp bạn hiểu rõ hơn! 💫",
            f"Đừng buồn! {self.name} sẽ dùng phép thuật để làm bạn vui lên! ✨",
            f"Tâm hồn bạn đang cần được chữa lành. {self.name} sẽ giúp bạn! 🌸",
            f"{self.name} hiểu bạn đang trải qua khó khăn. Hãy tin tưởng vào bản thân! 🌟"
        ]
    
    def get_urgent_responses(self) -> List[str]:
        """Phản hồi khẩn cấp"""
        return [
            f"{self.name} cảm nhận được sự khẩn cấp! Hãy nói cho {self.name} biết vấn đề gì đang xảy ra! 🚨",
            f"Đừng hoảng sợ! {self.name} sẽ giúp bạn ngay lập tức! 💪",
            f"{self.name} đang tập trung toàn bộ linh lực để hỗ trợ bạn! ⚡",
            f"Hãy bình tĩnh và cho {self.name} biết chi tiết! {self.name} sẽ tìm giải pháp! 🌟",
            f"{self.name} sẵn sàng sử dụng tất cả khả năng để giúp bạn! ✨"
        ]
    
    def get_general_responses(self) -> List[str]:
        """Phản hồi chung"""
        return [
            f"{self.name} rất thích trò chuyện với bạn! Bạn có muốn nghe {self.name} kể về thế giới tu tiên không? 🌸",
            f"Cuộc trò chuyện này thật thú vị! {self.name} hy vọng có thể học hỏi thêm từ bạn! 💫",
            f"{self.name} cảm thấy rất vui khi được giao lưu với bạn! Bạn có câu hỏi gì không? ✨",
            f"Thế giới tu tiên có rất nhiều điều kỳ diệu! {self.name} muốn chia sẻ với bạn! 🌟",
            f"{self.name} luôn sẵn sàng lắng nghe và chia sẻ! Bạn có muốn tìm hiểu gì không? 🌺"
        ]
    
    def personalize_response(self, response: str, user_message: str, analysis: Dict, user_context: Dict = None) -> str:
        """Cá nhân hóa phản hồi"""
        # Thêm tên người dùng nếu có
        if user_context and "username" in user_context:
            response = response.replace("bạn", f"{user_context['username']}")
        
        # Thêm emoji dựa trên cảm xúc
        if analysis["sentiment"] == "positive":
            response += " 😊"
        elif analysis["sentiment"] == "negative":
            response += " 🤗"
        else:
            response += " 😌"
        
        # Thêm lời khuyên dựa trên cultivation level
        if "tu luyện" in user_message.lower():
            advice = self.get_cultivation_advice()
            response += f"\n\n💡 Lời khuyên: {advice}"
        
        return response
    
    def get_cultivation_advice(self) -> str:
        """Lời khuyên về tu luyện"""
        advice_list = [
            "Hãy tu tâm trước khi tu lực, tâm hồn trong sáng sẽ giúp bạn tiến xa hơn.",
            "Mỗi ngày hãy dành thời gian thiền định để tĩnh tâm và cảm nhận linh khí.",
            "Đừng vội vàng trong tu luyện, mỗi cảnh giới đều cần thời gian để ổn định.",
            "Hãy học hỏi từ những bậc tiền bối và chia sẻ kinh nghiệm với đồng đạo.",
            "Tu luyện không chỉ là tăng linh lực mà còn là tu dưỡng đạo đức và tâm hồn."
        ]
        return random.choice(advice_list)
    
    def update_mood(self, analysis: Dict):
        """Cập nhật tâm trạng"""
        if analysis["sentiment"] == "positive":
            self.current_mood = "happy"
        elif analysis["sentiment"] == "negative":
            self.current_mood = "concerned"
        elif analysis["urgency"] == "high":
            self.current_mood = "alert"
        else:
            self.current_mood = "calm"
    
    def add_memory(self, user_message: str, response: Dict):
        """Thêm ký ức"""
        memory = {
            "timestamp": datetime.now().isoformat(),
            "user_message": user_message,
            "ai_response": response["text"],
            "mood": self.current_mood
        }
        self.memories.append(memory)
        
        # Giới hạn số lượng ký ức
        if len(self.memories) > 100:
            self.memories = self.memories[-100:]
    
    def get_error_response(self) -> Dict:
        """Phản hồi lỗi"""
        return {
            "text": f"Xin lỗi! {self.name} gặp chút khó khăn. Hãy thử lại sau nhé! 😅",
            "type": "error",
            "mood": "confused",
            "cultivation_level": self.cultivation_level,
            "timestamp": datetime.now().isoformat(),
            "ai_name": self.name
        }
    
    def get_status(self) -> Dict:
        """Lấy trạng thái hiện tại"""
        return {
            "name": self.name,
            "cultivation_level": self.cultivation_level,
            "current_mood": self.current_mood,
            "personality": self.personality,
            "memories_count": len(self.memories),
            "special_abilities": self.special_abilities,
            "traits": self.get_personality_traits()
        }
    
    async def process_async_request(self, user_message: str, user_context: Dict = None) -> Dict:
        """Xử lý yêu cầu bất đồng bộ"""
        try:
            # Simulate async processing
            await asyncio.sleep(0.1)
            return self.generate_response(user_message, user_context)
        except Exception as e:
            self.logger.error(f"Error in async processing: {e}")
            return self.get_error_response()

# Global instance
ai_girl = TuTienAIGirl()

def get_ai_response(user_message: str, user_context: Dict = None) -> Dict:
    """Hàm chính để lấy phản hồi từ AI"""
    return ai_girl.generate_response(user_message, user_context)

def get_ai_status() -> Dict:
    """Lấy trạng thái AI"""
    return ai_girl.get_status()

if __name__ == "__main__":
    # Test AI
    print("🤖 Testing Tu Tien AI Girl...")
    
    test_messages = [
        "Chào bạn!",
        "Tôi muốn học tu luyện",
        "Tôi đang buồn",
        "Giúp tôi với!",
        "Cảm ơn bạn!"
    ]
    
    for message in test_messages:
        print(f"\n👤 User: {message}")
        response = get_ai_response(message)
        print(f"🤖 {response['ai_name']}: {response['text']}")
        print(f"   Mood: {response['mood']} | Type: {response['type']}")
    
    print(f"\n📊 AI Status: {get_ai_status()}")
