# Quick Test Scenarios - CPSU Health Assistant Rasa

Use these test conversations to verify the chatbot is working correctly.

## ✅ Basic Symptom Reporting

```
User: Hi
Bot: Hello! I'm the CPSU Virtual Health Assistant...

User: I have fever
Bot: I've noted: fever
Bot: Are there any other symptoms you're experiencing?

User: yes, I also have cough and headache
Bot: I've noted: cough, headache
Bot: Let me confirm - you're experiencing: fever, cough, headache. Is that correct?

User: yes
Bot: Thank you. Let me analyze your symptoms...
Bot: [Shows diagnosis with confidence and precautions]
```

## 🚨 Emergency Detection

```
User: I have severe chest pain and difficulty breathing
Bot: 🚨 **EMERGENCY ALERT** 🚨
     Your symptoms may require immediate medical attention!
     PLEASE DO ONE OF THE FOLLOWING IMMEDIATELY:
     1. Visit the CPSU Health Clinic NOW
     ...
```

## 💬 Natural Language Variations

All these should be recognized:

### Fever Synonyms
- "I have a high temperature"
- "I'm running a fever"
- "I feel hot"
- "I have mild fever"

### Headache Variations
- "My head hurts"
- "I have a splitting headache"
- "Head is pounding"
- "Migraine"

### Stomach Pain
- "Stomach ache"
- "Belly pain"
- "Tummy hurts"
- "Abdominal cramps"

### Breathing Issues
- "Can't breathe properly"
- "Shortness of breath"
- "Difficulty breathing"
- "Hard to breathe"

## 🧪 Test Commands

### Interactive Shell
```bash
cd Rasa
rasa shell --debug
```

### API Test
```bash
curl -X POST http://localhost:5005/webhooks/rest/webhook \
  -H "Content-Type: application/json" \
  -d '{
    "sender": "test123",
    "message": "I have fever, cough, and fatigue"
  }' | jq
```

### Test Story Validation
```bash
rasa test
```

## 📊 Expected Behavior

### ✅ Should Work
- Recognizing 132+ symptoms with synonyms
- Extracting multiple symptoms from one message
- Accumulating symptoms across turns
- Calling Django ML API for predictions
- Showing confidence scores and LLM validation
- Providing precautions
- Emergency detection

### ❌ Should NOT Work (Expected Limitations)
- Medical advice beyond symptom assessment
- Prescription recommendations
- Diagnoses not in the 41-disease training set
- Non-health related queries

## 🔍 Debug Mode

```bash
rasa shell --debug
```

Look for:
- Intent recognition confidence
- Entity extraction
- Slot values
- Action calls to Django
- API responses

## 📝 Conversation Examples

### Example 1: Flu-like Symptoms
```
User: I'm not feeling well
Bot: I'm here to help. What symptoms are you experiencing?

User: fever, body ache, and cough
Bot: I've noted: fever, muscle_pain, cough
Bot: Are there any other symptoms?

User: no
Bot: Analyzing your symptoms...
Bot: **Condition**: Influenza (Flu)
     **Confidence**: 89% ✅ (AI Validated)
     ...
```

### Example 2: Correction Flow
```
User: I have headache and fever
Bot: I've noted: headache, fever
Bot: Let me confirm - you're experiencing: headache, fever. Is that correct?

User: no, I meant stomach ache, not headache
Bot: What symptoms are you experiencing?

User: fever and stomach ache
Bot: I've noted: fever, abdominal_pain
Bot: [Proceeds with analysis]
```

### Example 3: Emergency Keywords
```
User: emergency! chest pain!
Bot: 🚨 **EMERGENCY ALERT** 🚨
     [Shows emergency instructions]
```

## 🎯 Key Test Points

1. **Synonym Recognition**: Try different ways to say the same symptom
2. **Multi-symptom Extraction**: "I have A, B, and C"
3. **Symptom Accumulation**: Add symptoms over multiple turns
4. **Confidence Threshold**: Ensure bot asks for confirmation when unsure
5. **Django Integration**: Verify API calls succeed (check Django logs)
6. **LLM Validation**: Confirm "AI Validated" appears in high-confidence results
7. **Emergency Detection**: Test critical symptoms trigger alerts
8. **Precautions**: Verify disease-specific advice is shown

## 🐛 Common Issues & Fixes

### Issue: "Action server not running"
**Fix**: Start action server in separate terminal
```bash
rasa run actions
```

### Issue: Symptoms not recognized
**Fix**: Check if synonym exists in `data/nlu.yml`, add if missing, retrain

### Issue: Low confidence
**Fix**: Add more training examples for that symptom combination

### Issue: Django API error
**Fix**: Ensure Django is running on port 8000, ML model exists

## 📈 Success Metrics

- Intent recognition: >90% accuracy
- Entity extraction: >85% accuracy  
- End-to-end symptom → diagnosis: >80% success rate
- Emergency detection: 100% (critical)
- Response time: <2 seconds (with Django)
