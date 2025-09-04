import random
import os
from datetime import datetime, timedelta

class CultivationAI:
    def __init__(self):
        # Hệ thống cảnh giới chi tiết với 9 tầng + viên mãn cho mỗi cấp
        self.cultivation_stages = self._build_detailed_stages()
        
        # Cảnh giới chính và ngưỡng tổng quát
        self.major_stages = {
            "Luyện Khí": {"min_power": 0, "max_power": 10000},
            "Trúc Cơ": {"min_power": 10000, "max_power": 50000},
            "Kết Đan": {"min_power": 50000, "max_power": 200000},
            "Nguyên Anh": {"min_power": 200000, "max_power": 1000000},
            "Hóa Thần": {"min_power": 1000000, "max_power": 5000000},
            "Luyện Hư": {"min_power": 5000000, "max_power": 20000000},
            "Hợp Thể": {"min_power": 20000000, "max_power": 100000000},
            "Đại Thừa": {"min_power": 100000000, "max_power": 500000000},
            "Độ Kiếp": {"min_power": 500000000, "max_power": 2000000000},
            "Tản Tiên": {"min_power": 2000000000, "max_power": 10000000000}
        }
    
    def _build_detailed_stages(self):
        """Xây dựng hệ thống tầng chi tiết"""
        stages = {}
        major_stages = [
            ("Luyện Khí", 0, 10000),
            ("Trúc Cơ", 10000, 50000),
            ("Kết Đan", 50000, 200000),
            ("Nguyên Anh", 200000, 1000000),
            ("Hóa Thần", 1000000, 5000000),
            ("Luyện Hư", 5000000, 20000000),
            ("Hợp Thể", 20000000, 100000000),
            ("Đại Thừa", 100000000, 500000000),
            ("Độ Kiếp", 500000000, 2000000000),
            ("Tản Tiên", 2000000000, 10000000000)
        ]
        
        for stage_name, min_power, max_power in major_stages:
            power_range = max_power - min_power
            # Chia thành 10 phần: 9 tầng + viên mãn
            step = power_range // 10
            
            # 9 tầng đầu
            for i in range(1, 10):
                substage_min = min_power + (i - 1) * step
                substage_max = min_power + i * step
                stages[f"{stage_name} Tầng {i}"] = {
                    "min_power": substage_min,
                    "max_power": substage_max,
                    "major_stage": stage_name
                }
            
            # Tầng viên mãn
            stages[f"{stage_name} Viên Mãn"] = {
                "min_power": min_power + 9 * step,
                "max_power": max_power,
                "major_stage": stage_name
            }
        
        self.weather_conditions = [
            "Linh Khí Dồi Dào - Tu luyện tăng 20%",
            "Thiên Lôi Tụ Tập - Nguy hiểm tăng nhưng breakthrough dễ hơn",
            "Âm Dương Thái Cực - Cân bằng hoàn hảo cho tu luyện",
            "Ma Khí Xâm Nhập - Tu luyện chậm nhưng tăng kháng ma",
            "Thiên Nhiên Linh Khí - Tăng cường khả năng hấp thụ linh khí"
        ]
        
        return stages
    
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
        
        # Tính toán dựa trên nhiều yếu tố (handle None values)
        user_factors = (
            (user.spiritual_power or 0) % 7 +
            (user.karma_points or 0) % 5 +
            (user.reputation or 0) % 3 +
            datetime.now().day % 8
        ) % len(fortunes)
        
        return fortunes[user_factors]
    
    def get_cultivation_advice(self, user):
        """Đưa ra lời khuyên tu luyện thông minh"""
        advice = []
        
        current_level = user.cultivation_level
        stage_info = self.cultivation_stages.get(current_level)
        
        if not stage_info:
            # Fallback to first stage if not found
            stage_info = self.cultivation_stages.get("Luyện Khí Tầng 1")
            if not stage_info:
                stage_info = {"min_power": 0, "max_power": 1000, "major_stage": "Luyện Khí"}
        
        # Phân tích tiến độ
        power_range = stage_info["max_power"] - stage_info["min_power"]
        if power_range > 0:
            progress = (user.spiritual_power - stage_info["min_power"]) / power_range
        else:
            progress = 1.0  # Max progress if no range
        
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
        guild1_power = (guild1.level or 1) * 1000 + (guild1.treasury or 0) + (guild1.territory_count or 1) * 500
        guild2_power = (guild2.level or 1) * 1000 + (guild2.treasury or 0) + (guild2.territory_count or 1) * 500
        
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
