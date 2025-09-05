using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Hosting;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using System.Text.Json;
using System.IO;
using System.Net.Http;
using System.Text;

namespace TuTienVoiceService
{
    public class Program
    {
        public static void Main(string[] args)
        {
            CreateHostBuilder(args).Build().Run();
        }

        public static IHostBuilder CreateHostBuilder(string[] args) =>
            Host.CreateDefaultBuilder(args)
                .ConfigureWebHostDefaults(webBuilder =>
                {
                    webBuilder.UseStartup<Startup>();
                });
    }

    public class Startup
    {
        public void ConfigureServices(IServiceCollection services)
        {
            services.AddControllers();
            services.AddCors(options =>
            {
                options.AddPolicy("AllowAll", builder =>
                {
                    builder.AllowAnyOrigin()
                           .AllowAnyMethod()
                           .AllowAnyHeader();
                });
            });
        }

        public void Configure(IApplicationBuilder app, IWebHostEnvironment env)
        {
            if (env.IsDevelopment())
            {
                app.UseDeveloperExceptionPage();
            }

            app.UseCors("AllowAll");
            app.UseRouting();
            app.UseEndpoints(endpoints =>
            {
                endpoints.MapControllers();
            });
        }
    }

    [ApiController]
    [Route("api/[controller]")]
    public class VoiceController : ControllerBase
    {
        private readonly VoiceSynthesisService _voiceService;
        private readonly HttpClient _httpClient;

        public VoiceController()
        {
            _voiceService = new VoiceSynthesisService();
            _httpClient = new HttpClient();
        }

        [HttpGet("health")]
        public IActionResult Health()
        {
            return Ok(new
            {
                status = "healthy",
                timestamp = DateTime.UtcNow.ToString("yyyy-MM-ddTHH:mm:ssZ"),
                service = "C# Voice Service",
                capabilities = new[] { "text_to_speech", "voice_synthesis", "audio_generation" }
            });
        }

        [HttpPost("synthesize")]
        public async Task<IActionResult> SynthesizeVoice([FromBody] VoiceRequest request)
        {
            try
            {
                var result = await _voiceService.SynthesizeVoiceAsync(request.Text, request.VoiceType, request.Language);
                return Ok(result);
            }
            catch (Exception ex)
            {
                return BadRequest(new { error = ex.Message });
            }
        }

        [HttpPost("chat-with-voice")]
        public async Task<IActionResult> ChatWithVoice([FromBody] ChatVoiceRequest request)
        {
            try
            {
                // Get AI response from other services
                var aiResponse = await GetAIResponse(request.Message, request.Context);
                
                // Synthesize voice
                var voiceResult = await _voiceService.SynthesizeVoiceAsync(
                    aiResponse.Text, 
                    request.VoiceType ?? "tutien_female", 
                    request.Language ?? "vi-VN"
                );

                return Ok(new
                {
                    ai_response = aiResponse,
                    voice_result = voiceResult,
                    timestamp = DateTime.UtcNow.ToString("yyyy-MM-ddTHH:mm:ssZ")
                });
            }
            catch (Exception ex)
            {
                return BadRequest(new { error = ex.Message });
            }
        }

        [HttpGet("voices")]
        public IActionResult GetAvailableVoices()
        {
            var voices = _voiceService.GetAvailableVoices();
            return Ok(voices);
        }

        [HttpPost("emotion")]
        public async Task<IActionResult> SynthesizeWithEmotion([FromBody] EmotionalVoiceRequest request)
        {
            try
            {
                var result = await _voiceService.SynthesizeWithEmotionAsync(
                    request.Text, 
                    request.Emotion, 
                    request.VoiceType, 
                    request.Language
                );
                return Ok(result);
            }
            catch (Exception ex)
            {
                return BadRequest(new { error = ex.Message });
            }
        }

        private async Task<AIResponse> GetAIResponse(string message, Dictionary<string, object> context)
        {
            try
            {
                // Try Python AI first
                var pythonResponse = await CallPythonAI(message, context);
                if (pythonResponse != null) return pythonResponse;

                // Try Java AI
                var javaResponse = await CallJavaAI(message, context);
                if (javaResponse != null) return javaResponse;

                // Try Ruby AI
                var rubyResponse = await CallRubyAI(message, context);
                if (rubyResponse != null) return rubyResponse;

                // Default response
                return new AIResponse
                {
                    Text = "Xin lỗi! Tôi đang gặp chút khó khăn. Hãy thử lại sau nhé!",
                    Type = "error",
                    Mood = "confused",
                    CultivationLevel = "Nguyên Anh Tầng 3",
                    SpecialAbility = "Đọc tâm ý người khác",
                    WisdomLevel = 88,
                    MysteryLevel = 80,
                    Timestamp = DateTime.UtcNow.ToString("yyyy-MM-ddTHH:mm:ssZ"),
                    AiName = "Linh Nhi"
                };
            }
            catch (Exception ex)
            {
                return new AIResponse
                {
                    Text = "Có lỗi xảy ra khi xử lý tin nhắn của bạn.",
                    Type = "error",
                    Mood = "confused",
                    CultivationLevel = "Nguyên Anh Tầng 3",
                    SpecialAbility = "Đọc tâm ý người khác",
                    WisdomLevel = 88,
                    MysteryLevel = 80,
                    Timestamp = DateTime.UtcNow.ToString("yyyy-MM-ddTHH:mm:ssZ"),
                    AiName = "Linh Nhi"
                };
            }
        }

        private async Task<AIResponse> CallPythonAI(string message, Dictionary<string, object> context)
        {
            try
            {
                var requestData = new { message = message, context = context };
                var json = JsonSerializer.Serialize(requestData);
                var content = new StringContent(json, Encoding.UTF8, "application/json");

                var response = await _httpClient.PostAsync("http://localhost:5000/api/ai/chat", content);
                if (response.IsSuccessStatusCode)
                {
                    var responseContent = await response.Content.ReadAsStringAsync();
                    return JsonSerializer.Deserialize<AIResponse>(responseContent);
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Python AI error: {ex.Message}");
            }
            return null;
        }

        private async Task<AIResponse> CallJavaAI(string message, Dictionary<string, object> context)
        {
            try
            {
                var requestData = new { message = message, context = context };
                var json = JsonSerializer.Serialize(requestData);
                var content = new StringContent(json, Encoding.UTF8, "application/json");

                var response = await _httpClient.PostAsync("http://localhost:8080/api/ai/chat", content);
                if (response.IsSuccessStatusCode)
                {
                    var responseContent = await response.Content.ReadAsStringAsync();
                    return JsonSerializer.Deserialize<AIResponse>(responseContent);
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Java AI error: {ex.Message}");
            }
            return null;
        }

        private async Task<AIResponse> CallRubyAI(string message, Dictionary<string, object> context)
        {
            try
            {
                var requestData = new { message = message, context = context };
                var json = JsonSerializer.Serialize(requestData);
                var content = new StringContent(json, Encoding.UTF8, "application/json");

                var response = await _httpClient.PostAsync("http://localhost:4567/api/v1/ai/chat", content);
                if (response.IsSuccessStatusCode)
                {
                    var responseContent = await response.Content.ReadAsStringAsync();
                    return JsonSerializer.Deserialize<AIResponse>(responseContent);
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Ruby AI error: {ex.Message}");
            }
            return null;
        }
    }

    public class VoiceSynthesisService
    {
        private readonly Dictionary<string, VoiceProfile> _voiceProfiles;

        public VoiceSynthesisService()
        {
            _voiceProfiles = InitializeVoiceProfiles();
        }

        private Dictionary<string, VoiceProfile> InitializeVoiceProfiles()
        {
            return new Dictionary<string, VoiceProfile>
            {
                ["tutien_female"] = new VoiceProfile
                {
                    Name = "Linh Nhi",
                    Gender = "Female",
                    Age = "Young Adult",
                    Language = "vi-VN",
                    Characteristics = new[] { "gentle", "wise", "mysterious", "caring" },
                    Pitch = 0.8f,
                    Speed = 0.9f,
                    Volume = 0.85f
                },
                ["tutien_male"] = new VoiceProfile
                {
                    Name = "Thiên Tôn",
                    Gender = "Male",
                    Age = "Adult",
                    Language = "vi-VN",
                    Characteristics = new[] { "authoritative", "wise", "calm", "powerful" },
                    Pitch = 0.6f,
                    Speed = 0.8f,
                    Volume = 0.9f
                },
                ["elder_female"] = new VoiceProfile
                {
                    Name = "Tiên Cô",
                    Gender = "Female",
                    Age = "Elder",
                    Language = "vi-VN",
                    Characteristics = new[] { "ancient", "mysterious", "wise", "ethereal" },
                    Pitch = 0.7f,
                    Speed = 0.7f,
                    Volume = 0.8f
                }
            };
        }

        public async Task<VoiceResult> SynthesizeVoiceAsync(string text, string voiceType, string language)
        {
            try
            {
                var voiceProfile = _voiceProfiles.GetValueOrDefault(voiceType, _voiceProfiles["tutien_female"]);
                
                // Simulate voice synthesis processing
                await Task.Delay(1000);

                var result = new VoiceResult
                {
                    Success = true,
                    AudioData = GenerateMockAudioData(text, voiceProfile),
                    Duration = CalculateDuration(text),
                    VoiceType = voiceType,
                    Language = language,
                    Timestamp = DateTime.UtcNow.ToString("yyyy-MM-ddTHH:mm:ssZ"),
                    Metadata = new VoiceMetadata
                    {
                        TextLength = text.Length,
                        VoiceProfile = voiceProfile.Name,
                        Characteristics = voiceProfile.Characteristics,
                        Quality = "High"
                    }
                };

                return result;
            }
            catch (Exception ex)
            {
                return new VoiceResult
                {
                    Success = false,
                    Error = ex.Message,
                    Timestamp = DateTime.UtcNow.ToString("yyyy-MM-ddTHH:mm:ssZ")
                };
            }
        }

        public async Task<VoiceResult> SynthesizeWithEmotionAsync(string text, string emotion, string voiceType, string language)
        {
            try
            {
                var voiceProfile = _voiceProfiles.GetValueOrDefault(voiceType, _voiceProfiles["tutien_female"]);
                
                // Adjust voice parameters based on emotion
                AdjustVoiceForEmotion(voiceProfile, emotion);

                // Simulate voice synthesis processing
                await Task.Delay(1200);

                var result = new VoiceResult
                {
                    Success = true,
                    AudioData = GenerateMockAudioData(text, voiceProfile),
                    Duration = CalculateDuration(text),
                    VoiceType = voiceType,
                    Language = language,
                    Emotion = emotion,
                    Timestamp = DateTime.UtcNow.ToString("yyyy-MM-ddTHH:mm:ssZ"),
                    Metadata = new VoiceMetadata
                    {
                        TextLength = text.Length,
                        VoiceProfile = voiceProfile.Name,
                        Characteristics = voiceProfile.Characteristics,
                        Emotion = emotion,
                        Quality = "High"
                    }
                };

                return result;
            }
            catch (Exception ex)
            {
                return new VoiceResult
                {
                    Success = false,
                    Error = ex.Message,
                    Timestamp = DateTime.UtcNow.ToString("yyyy-MM-ddTHH:mm:ssZ")
                };
            }
        }

        public List<VoiceInfo> GetAvailableVoices()
        {
            return _voiceProfiles.Select(kvp => new VoiceInfo
            {
                Id = kvp.Key,
                Name = kvp.Value.Name,
                Gender = kvp.Value.Gender,
                Age = kvp.Value.Age,
                Language = kvp.Value.Language,
                Characteristics = kvp.Value.Characteristics
            }).ToList();
        }

        private void AdjustVoiceForEmotion(VoiceProfile profile, string emotion)
        {
            switch (emotion.ToLower())
            {
                case "happy":
                    profile.Pitch = Math.Min(1.0f, profile.Pitch + 0.1f);
                    profile.Speed = Math.Min(1.2f, profile.Speed + 0.1f);
                    break;
                case "sad":
                    profile.Pitch = Math.Max(0.5f, profile.Pitch - 0.1f);
                    profile.Speed = Math.Max(0.6f, profile.Speed - 0.1f);
                    break;
                case "angry":
                    profile.Pitch = Math.Min(1.0f, profile.Pitch + 0.05f);
                    profile.Volume = Math.Min(1.0f, profile.Volume + 0.1f);
                    break;
                case "calm":
                    profile.Speed = Math.Max(0.7f, profile.Speed - 0.1f);
                    profile.Volume = Math.Max(0.7f, profile.Volume - 0.05f);
                    break;
                case "excited":
                    profile.Pitch = Math.Min(1.0f, profile.Pitch + 0.15f);
                    profile.Speed = Math.Min(1.3f, profile.Speed + 0.2f);
                    break;
            }
        }

        private string GenerateMockAudioData(string text, VoiceProfile profile)
        {
            // In a real implementation, this would generate actual audio data
            // For now, we'll return a mock base64 encoded audio data
            var mockAudioData = Convert.ToBase64String(Encoding.UTF8.GetBytes($"AUDIO_DATA_FOR: {text}"));
            return mockAudioData;
        }

        private double CalculateDuration(string text)
        {
            // Estimate duration based on text length (roughly 150 words per minute)
            var wordsPerMinute = 150;
            var wordCount = text.Split(' ').Length;
            return (wordCount / (double)wordsPerMinute) * 60; // Duration in seconds
        }
    }

    // Data models
    public class VoiceRequest
    {
        public string Text { get; set; }
        public string VoiceType { get; set; }
        public string Language { get; set; }
    }

    public class ChatVoiceRequest
    {
        public string Message { get; set; }
        public Dictionary<string, object> Context { get; set; }
        public string VoiceType { get; set; }
        public string Language { get; set; }
    }

    public class EmotionalVoiceRequest
    {
        public string Text { get; set; }
        public string Emotion { get; set; }
        public string VoiceType { get; set; }
        public string Language { get; set; }
    }

    public class VoiceResult
    {
        public bool Success { get; set; }
        public string AudioData { get; set; }
        public double Duration { get; set; }
        public string VoiceType { get; set; }
        public string Language { get; set; }
        public string Emotion { get; set; }
        public string Timestamp { get; set; }
        public string Error { get; set; }
        public VoiceMetadata Metadata { get; set; }
    }

    public class VoiceMetadata
    {
        public int TextLength { get; set; }
        public string VoiceProfile { get; set; }
        public string[] Characteristics { get; set; }
        public string Emotion { get; set; }
        public string Quality { get; set; }
    }

    public class VoiceProfile
    {
        public string Name { get; set; }
        public string Gender { get; set; }
        public string Age { get; set; }
        public string Language { get; set; }
        public string[] Characteristics { get; set; }
        public float Pitch { get; set; }
        public float Speed { get; set; }
        public float Volume { get; set; }
    }

    public class VoiceInfo
    {
        public string Id { get; set; }
        public string Name { get; set; }
        public string Gender { get; set; }
        public string Age { get; set; }
        public string Language { get; set; }
        public string[] Characteristics { get; set; }
    }

    public class AIResponse
    {
        public string Text { get; set; }
        public string Type { get; set; }
        public string Mood { get; set; }
        public string CultivationLevel { get; set; }
        public string SpecialAbility { get; set; }
        public int WisdomLevel { get; set; }
        public int MysteryLevel { get; set; }
        public string Timestamp { get; set; }
        public string AiName { get; set; }
    }
}
