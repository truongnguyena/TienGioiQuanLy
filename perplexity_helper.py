import os
import json
import requests
from typing import Dict, Any, Optional

class PerplexityManager:
    """
    Perplexity AI Assistant for Tu Tiên management support
    """
    
    def __init__(self):
        self.api_key = os.environ.get("PERPLEXITY_API_KEY")
        self.base_url = "https://api.perplexity.ai/chat/completions"
        self.model = "llama-3.1-sonar-small-128k-online"
        
        if not self.api_key:
            print("Warning: PERPLEXITY_API_KEY not found. AI features will be disabled.")
    
    def _make_request(self, messages: list, system_prompt: str = None) -> Optional[Dict[str, Any]]:
        """Make API request to Perplexity"""
        try:
            # Prepare messages with system prompt if provided
            formatted_messages = []
            if system_prompt:
                formatted_messages.append({
                    "role": "system",
                    "content": system_prompt
                })
            
            formatted_messages.extend(messages)
            
            payload = {
                "model": self.model,
                "messages": formatted_messages,
                "temperature": 0.2,
                "max_tokens": 1000,
                "stream": False
            }
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            response = requests.post(self.base_url, headers=headers, json=payload)
            response.raise_for_status()
            
            return response.json()
            
        except Exception as e:
            print(f"Perplexity API error: {e}")
            return None
    
    def get_cultivation_advice(self, user_data: dict) -> str:
        """Get cultivation strategy advice based on user's current status"""
        system_prompt = """Bạn là một vị Tiên sư chuyên gia về tu luyện trong thế giới Tu Tiên. 
        Hãy đưa ra lời khuyên chiến lược về tu luyện, phát triển nhân vật dựa trên thông tin hiện tại.
        Trả lời bằng tiếng Việt với phong cách cổ điển tu tiên."""
        
        current_level = user_data.get('cultivation_level', 'Luyện Khí Tầng 1')
        spiritual_power = user_data.get('spiritual_power', 0)
        resources = {
            'spiritual_stones': user_data.get('spiritual_stones', 0),
            'pills': user_data.get('pills_count', 0),
            'artifacts': user_data.get('artifacts_count', 0)
        }
        
        query = f"""
        Hiện tại ta đang ở cảnh giới {current_level} với {spiritual_power} điểm linh lực.
        Tài nguyên hiện có: {resources['spiritual_stones']} linh thạch, {resources['pills']} dan dược, {resources['artifacts']} pháp bảo.
        
        Hãy tư vấn chiến lược tu luyện tốt nhất cho giai đoạn hiện tại:
        1. Nên tập trung vào hoạt động gì để tiến bộ nhanh nhất?
        2. Làm thế nào để tối ưu hóa việc sử dụng tài nguyên?
        3. Có lời khuyên gì về việc phân bổ thời gian tu luyện?
        """
        
        messages = [{"role": "user", "content": query}]
        response = self._make_request(messages, system_prompt)
        
        if response and response.get('choices'):
            return response['choices'][0]['message']['content']
        else:
            return "Tiên sư hiện tại không thể truyền đạt được. Hãy thử lại sau!"
    
    def get_guild_management_advice(self, guild_data: dict, user_role: str) -> str:
        """Get guild management advice"""
        system_prompt = """Bạn là một vị Trưởng lão am hiểu về quản lý bang hội trong thế giới Tu Tiên.
        Đưa ra lời khuyên về quản lý bang hội, phát triển tổ chức, và chiến lược hợp tác.
        Trả lời bằng tiếng Việt với phong cách cổ điển tu tiên."""
        
        guild_name = guild_data.get('name', 'Unknown Guild')
        member_count = guild_data.get('member_count', 0)
        guild_level = guild_data.get('level', 1)
        treasury = guild_data.get('treasury', 0)
        
        query = f"""
        Bang hội {guild_name} hiện có {member_count} thành viên, cấp độ {guild_level}, kho bạc {treasury} linh thạch.
        Ta đang giữ vai trò {user_role} trong bang hội.
        
        Hãy tư vấn về:
        1. Chiến lược phát triển bang hội phù hợp với quy mô hiện tại
        2. Cách tăng cường sự đoàn kết và hợp tác giữa các thành viên
        3. Kế hoạch tài chính và đầu tư cho bang hội
        4. Hoạt động nào nên ưu tiên để nâng cao uy tín bang hội
        """
        
        messages = [{"role": "user", "content": query}]
        response = self._make_request(messages, system_prompt)
        
        if response and response.get('choices'):
            return response['choices'][0]['message']['content']
        else:
            return "Trưởng lão hiện tại đang tĩnh tâm. Hãy thử lại sau!"
    
    def get_expedition_advice(self, expedition_data: dict, context: str = "planning") -> str:
        """Get expedition planning and coordination advice"""
        system_prompt = """Bạn là một vị Đạo trưởng dày dặn kinh nghiệm trong việc tổ chức và dẫn dắt các cuộc đạo lữ.
        Đưa ra lời khuyên về lập kế hoạch, tổ chức và điều phối đạo lữ an toàn hiệu quả.
        Trả lời bằng tiếng Việt với phong cách cổ điển tu tiên."""
        
        if context == "planning":
            query = f"""
            Đang lên kế hoạch cho một cuộc đạo lữ:
            - Điểm đến: {expedition_data.get('destination', 'Chưa xác định')}
            - Độ khó: {expedition_data.get('difficulty_level', 1)}/5
            - Thời gian dự kiến: {expedition_data.get('duration_hours', 24)} giờ
            - Số người tham gia tối đa: {expedition_data.get('max_participants', 5)}
            - Yêu cầu tu vi tối thiểu: {expedition_data.get('min_cultivation', 'Không')}
            
            Hãy tư vấn về:
            1. Chuẩn bị cần thiết cho cuộc đạo lữ này
            2. Chiến lược tổ chức nhóm và phân công nhiệm vụ
            3. Rủi ro tiềm ẩn và cách phòng tránh
            4. Cách tối ưu hóa phần thưởng cho toàn bộ đoàn
            """
        else:  # ongoing expedition management
            query = f"""
            Đang điều phối cuộc đạo lữ "{expedition_data.get('name', 'Unknown')}" tại {expedition_data.get('destination', 'Unknown')}:
            - Số người đã tham gia: {len(expedition_data.get('participants', []))}
            - Trạng thái: {expedition_data.get('status', 'active')}
            
            Cần lời khuyên về quản lý và điều phối đoàn đạo lữ đang diễn ra.
            """
        
        messages = [{"role": "user", "content": query}]
        response = self._make_request(messages, system_prompt)
        
        if response and response.get('choices'):
            return response['choices'][0]['message']['content']
        else:
            return "Đạo trưởng hiện đang nhập định. Hãy thử lại sau!"
    
    def get_resource_optimization_advice(self, user_resources: dict, goals: list = None) -> str:
        """Get resource management and optimization advice"""
        system_prompt = """Bạn là một vị Quản lý kho bạc cao cấp, chuyên gia về tối ưu hóa tài nguyên trong tu tiên.
        Đưa ra lời khuyên về quản lý tài chính, đầu tư và tối ưu hóa tài nguyên.
        Trả lời bằng tiếng Việt với phong cách cổ điển tu tiên."""
        
        resources = {
            'spiritual_stones': user_resources.get('spiritual_stones', 0),
            'pills': user_resources.get('pills_count', 0),
            'artifacts': user_resources.get('artifacts_count', 0),
            'mining_level': user_resources.get('mining_level', 1),
            'cultivation_points': user_resources.get('cultivation_points', 0)
        }
        
        goals_text = "Chưa có mục tiêu cụ thể"
        if goals and isinstance(goals, list):
            goals_text = ", ".join(str(g) for g in goals)
        
        query = f"""
        Hiện tại kho tàng của ta có:
        - {resources['spiritual_stones']} linh thạch
        - {resources['pills']} dan dược
        - {resources['artifacts']} pháp bảo
        - Cấp độ đào mỏ: {resources['mining_level']}
        - Điểm tu luyện: {resources['cultivation_points']}
        
        Mục tiêu phát triển: {goals_text}
        
        Hãy tư vấn về:
        1. Cách phân bổ tài nguyên hiệu quả nhất
        2. Hoạt động nào nên ưu tiên để tăng thu nhập
        3. Chiến lược đầu tư dài hạn
        4. Cách cân bằng giữa chi tiêu hiện tại và tích lũy tương lai
        """
        
        messages = [{"role": "user", "content": query}]
        response = self._make_request(messages, system_prompt)
        
        if response and response.get('choices'):
            return response['choices'][0]['message']['content']
        else:
            return "Quản lý kho bạc đang kiểm kê. Hãy thử lại sau!"
    
    def get_general_advice(self, question: str, context: dict = None) -> str:
        """Get general Tu Tiên world advice"""
        system_prompt = """Bạn là một vị Tiên nhân uyên bác, am hiểu mọi việc trong thế giới Tu Tiên.
        Trả lời các câu hỏi về thế giới tu tiên, cốt truyện, và cuộc sống trong cộng đồng tu tiên.
        Luôn trả lời bằng tiếng Việt với phong cách cổ điển, uy nghiêm nhưng thân thiện."""
        
        context_info = ""
        if context and isinstance(context, dict):
            context_info = f"\n\nBối cảnh hiện tại: {json.dumps(context, ensure_ascii=False)}"
        
        full_query = f"{question}{context_info}"
        
        messages = [{"role": "user", "content": full_query}]
        response = self._make_request(messages, system_prompt)
        
        if response and response.get('choices'):
            return response['choices'][0]['message']['content']
        else:
            return "Tiên nhân hiện tại không thể đáp ứng. Hãy thử lại sau!"

# Global instance
perplexity_manager = PerplexityManager()