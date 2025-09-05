package com.tutien.ai;

public class MessageAnalysis {
    private String sentiment;
    private String urgency;
    private String intent;
    private double confidence;
    private boolean cultivationQuestion;
    private boolean helpRequest;
    private boolean emotional;
    private boolean greeting;
    
    public MessageAnalysis() {
        this.sentiment = "neutral";
        this.urgency = "normal";
        this.intent = "general";
        this.confidence = 0.5;
        this.cultivationQuestion = false;
        this.helpRequest = false;
        this.emotional = false;
        this.greeting = false;
    }
    
    public MessageAnalysis(String sentiment, String urgency, String intent, double confidence) {
        this.sentiment = sentiment;
        this.urgency = urgency;
        this.intent = intent;
        this.confidence = confidence;
        this.cultivationQuestion = false;
        this.helpRequest = false;
        this.emotional = false;
        this.greeting = false;
    }
    
    public String getSentiment() {
        return sentiment;
    }
    
    public void setSentiment(String sentiment) {
        this.sentiment = sentiment;
    }
    
    public String getUrgency() {
        return urgency;
    }
    
    public void setUrgency(String urgency) {
        this.urgency = urgency;
    }
    
    public String getIntent() {
        return intent;
    }
    
    public void setIntent(String intent) {
        this.intent = intent;
    }
    
    public double getConfidence() {
        return confidence;
    }
    
    public void setConfidence(double confidence) {
        this.confidence = confidence;
    }
    
    public boolean isCultivationQuestion() {
        return cultivationQuestion;
    }
    
    public void setCultivationQuestion(boolean cultivationQuestion) {
        this.cultivationQuestion = cultivationQuestion;
    }
    
    public boolean isHelpRequest() {
        return helpRequest;
    }
    
    public void setHelpRequest(boolean helpRequest) {
        this.helpRequest = helpRequest;
    }
    
    public boolean isEmotional() {
        return emotional;
    }
    
    public void setEmotional(boolean emotional) {
        this.emotional = emotional;
    }
    
    public boolean isGreeting() {
        return greeting;
    }
    
    public void setGreeting(boolean greeting) {
        this.greeting = greeting;
    }
}
