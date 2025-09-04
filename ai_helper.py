import random
import os
from datetime import datetime, timedelta

class CultivationAI:
    def __init__(self):
        self.cultivation_stages = {
            "Luyện Khí": {"min_power": 0, "max_power": 1000},
            "Trúc Cơ": {"min_power": 1000, "max_power": 5000},
            "Kết Đan": {"min_power": 5000, "max_power": 20000},
            "Nguyên Anh": {"min_power": 20000, "max_power": 100000},
            "Hóa Thần": {"min_power": 100000, "max_power": 500000},
            "Luyện Hư": {"min_power": 500000, "max_power": 2000000},
            "Hợp Thể": {"min_power": 2000000, "max_power": 10000000},
            "Đại Thừa": {"min_power": 10000000, "max_power": 50000000},
            "Độ Kiếp": {"min_power": 50000000, "max_power": 200000000},
            "Tản Tiên": {"min_power": 200000000, "max_power": 1000000000}
        }
        
        self.weather_conditions = [
            "Linh Khí Dồi Dào - Tu luyện tăng 20%",
            "Thiên Lôi Tụ Tập - Nguy hiểm tăng nhưng breakthrough dễ hơn",
            "Âm Dương Thái Cực - Cân bằng hoàn hảo cho tu luyện",
            "Ma Khí Xâm Nhập - Tu luyện chậm nhưng tăng kháng ma",
            "Thiên Nhiên Linh Khí - Tăng cường khả năng hấp thụ linh khí"
        ]
    
    def predict_cultivation_fortune(self, user):
        """Dự đoán vận mệnh tu luyện của người dùng"""
        fortunes = [
            "Hôm nay là ngày tốt lành cho việc đột phá cảnh giới!",
            "Nên tránh tu luyện công pháp mạnh trong 3 ngày tới.",
            "Có cơ hội gặp được cao nhân chỉ điểm đạo pháp.",
            "Thiên kiếp sắp tới, cần chuẩn bị tâm lý và tài nguyên.",
            "Vận mệnh thuận lợi cho việc luyện đan dược.",
            "Thích hợp khám phá bí cảnh tìm kiếm cơ duyên.",
            "Nên tập trung vào tu luyện thần thức.",
            "Có thể gặp phải tiểu nhân, cần cảnh giác.",
        ]
        
        # Tính toán dựa trên nhiều yếu tố
        user_factors = (
            user.spiritual_power % 7 +
            user.karma_points % 5 +
            user.reputation % 3 +
            datetime.now().day % 8
        ) % len(fortunes)
        
        return fortunes[user_factors]
    
    def get_cultivation_advice(self, user):
        """Đưa ra lời khuyên tu luyện thông minh"""
        advice = []
        
        current_stage = user.get_cultivation_stage()
        stage_info = self.cultivation_stages.get(current_stage, self.cultivation_stages["Luyện Khí"])
        
        # Phân tích tiến độ
        progress = (user.spiritual_power - stage_info["min_power"]) / (stage_info["max_power"] - stage_info["min_power"])
        
        if progress < 0.3:
            advice.append("Nên tập trung tu luyện cơ bản để tăng nền tảng.")
        elif progress < 0.7:
            advice.append("Có thể bắt đầu học các thuật pháp cao cấp hơn.")
        else:
            advice.append("Chuẩn bị đột phá lên tầng cao hơn!")
        
        # Phân tích tài nguyên
        if user.spiritual_stones < 500:
            advice.append("Cần tích lũy thêm linh thạch cho tu luyện.")
        
        if user.pills_count < 3:
            advice.append("Nên luyện hoặc mua thêm đan dược.")
        
        # Phân tích hoạt động xã hội
        if not user.guild_id:
            advice.append("Tham gia môn phái sẽ có nhiều cơ hội tu luyện hơn.")
        
        return advice
    
    def calculate_guild_war_prediction(self, guild1, guild2):
        """Dự đoán kết quả chiến tranh bang hội"""
        # Tính sức mạnh tổng hợp
        guild1_power = guild1.level * 1000 + guild1.treasury + guild1.territory_count * 500
        guild2_power = guild2.level * 1000 + guild2.treasury + guild2.territory_count * 500
        
        # Thêm yếu tố ngẫu nhiên
        guild1_power *= random.uniform(0.8, 1.2)
        guild2_power *= random.uniform(0.8, 1.2)
        
        if guild1_power > guild2_power:
            win_probability = min(90, 50 + (guild1_power - guild2_power) / guild1_power * 40)
        else:
            win_probability = max(10, 50 - (guild2_power - guild1_power) / guild2_power * 40)
        
        return {
            "guild1_win_probability": round(win_probability, 1),
            "guild2_win_probability": round(100 - win_probability, 1),
            "predicted_duration_days": random.randint(3, 14),
            "casualty_estimate": "Trung bình" if abs(guild1_power - guild2_power) < guild1_power * 0.2 else "Cao"
        }
    
    def get_weather_forecast(self):
        """Dự báo thời tiết linh khí"""
        return {
            "current": random.choice(self.weather_conditions),
            "tomorrow": random.choice(self.weather_conditions),
            "weekly_trend": "Linh khí sẽ dồi dào trong tuần tới"
        }
    
    def generate_expedition_route(self, difficulty, destination):
        """Tạo lộ trình đạo lữ thông minh"""
        routes = {
            1: ["Rừng Tre Xanh", "Suối Linh Tuyền", "Đồi Hoa Lan"],
            2: ["Thung Lũng Sương Mù", "Hang Dơi Máu", "Đỉnh Núi Kiếm"],
            3: ["Sa Mạc Cát Vàng", "Đền Cổ Bỏ Hoang", "Hồ Nước Độc"],
            4: ["Rừng Quỷ Dữ", "Thành Phố Ma", "Cổng Địa Ngục"],
            5: ["Thiên Đình", "Cung Điện Rồng", "Vực Sâu Vô Đáy"]
        }
        
        base_route = routes.get(difficulty, routes[1])
        
        return {
            "waypoints": base_route,
            "estimated_time": f"{difficulty * 6}-{difficulty * 8} giờ",
            "recommended_supplies": [
                "Đan dược hồi phục",
                "Pháp bảo phòng thủ", 
                "Linh thạch dự phòng",
                "Bùa hộ mạng"
            ],
            "special_events": [
                f"Có 30% cơ hội gặp Linh Thú cấp {difficulty}",
                f"Khả năng tìm thấy Thiên Tài Địa Bảo: {difficulty * 15}%"
            ]
        }

# Global AI instance
cultivation_ai = CultivationAI()
