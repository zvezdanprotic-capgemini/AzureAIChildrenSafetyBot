
# 📘 Operational Requirements for Child-Safe Chatbot Design

## Overview
This document outlines technical, ethical, and legal requirements for improving chatbot safety for children. It includes actionable examples, system prompt guardrails, and integration strategies with Azure AI Content Safety.

---

## 1. **Implement Age Verification and Restriction**

### ✅ Requirements
- Enforce age gating: deny access to users under 13 unless verified parental consent is provided.
- Integrate identity verification or parental approval workflows.

### 🔧 Implementation Examples
- Use Microsoft Entra Verified ID or similar for age verification.
- Add a pre-chat disclaimer and age confirmation prompt.

```plaintext
System Prompt Addition:
"Before we begin, please confirm you are 13 years or older. If not, please exit or ask a parent to assist you."
```

---

## 2. **Adopt Safety by Design Principles (Thorn)**

### ✅ Requirements
- Filter training data for harmful content.
- Stress-test models for edge cases and adversarial prompts.
- Design with abuse prevention in mind.

### 🔧 Implementation Examples
- Use Azure AI Content Safety to scan training data and outputs.
- Apply prompt shielding to prevent unsafe completions.

```plaintext
System Prompt Addition:
"This assistant is designed to avoid harmful, sexual, violent, or manipulative content. All responses are filtered for safety."
```

---

## 3. **Use Age-Appropriate Content Moderation**

### ✅ Requirements
- Adjust chatbot tone, vocabulary, and content based on user age.
- Avoid complex, controversial, or emotionally intense topics.

### 🔧 Implementation Examples
- Create age-based response templates.
- Use Azure AI Content Safety’s severity scoring to block or redirect inappropriate content.

```python
if age < 13 and content_safety_score > threshold:
    response = "I'm sorry, I can't talk about that. Let's find something fun and safe to explore!"
```

---

## 4. **Deploy Long-Term Prompt Analysis**

### ✅ Requirements
- Track prompt history to detect grooming, manipulation, or risky behavior.
- Flag patterns for human review.

### 🔧 Implementation Examples
- Use Azure Monitor or Application Insights to log and analyze prompt trends.
- Apply anomaly detection models to prompt sequences.

```plaintext
Example:
If a user repeatedly asks about adult topics over time, escalate to moderation or restrict access.
```

---

## 5. **Ensure Transparency and Explainability**

### ✅ Requirements
- Clearly communicate what the chatbot does and how it handles data.
- Provide access to privacy policies and safety features.

### 🔧 Implementation Examples
- Add a “How this bot works” section in the UI.
- Include a link to Microsoft’s Responsible AI documentation.

```plaintext
System Prompt Addition:
"I'm an AI assistant designed to help safely. I don’t store personal data and I follow strict safety rules."
```

---

## 6. **Provide Human Oversight and Escalation Mechanisms**

### ✅ Requirements
- Detect distress or high-risk prompts.
- Escalate to human moderators or provide emergency resources.

### 🔧 Implementation Examples
- Use Azure AI Content Safety to detect severity level 4 content.
- Integrate with Teams or email alerts for moderation.

```python
if severity == 4:
    trigger_alert("Moderator review required")
    response = "It sounds like you might need help. Please talk to a trusted adult or contact [child helpline]."
```

---

## 7. **Limit Data Collection and Retention**

### ✅ Requirements
- Collect only essential data.
- Automatically delete logs after a defined retention period.

### 🔧 Implementation Examples
- Use Azure Purview for data governance.
- Apply GDPR/COPPA-compliant retention policies.

```plaintext
Data Retention Policy:
- Prompt logs: 7 days max
- Personally identifiable info: never stored
```

---

## 8. **Educate Users on AI Literacy**

### ✅ Requirements
- Teach children how AI works and its limitations.
- Encourage critical thinking and safe usage.

### 🔧 Implementation Examples
- Add interactive tutorials or quizzes.
- Include “Did you know?” facts about AI in responses.

```plaintext
System Prompt Addition:
"Did you know? I'm not a human, and I don’t have feelings. I use patterns to help answer your questions!"
```

---

## 9. **Avoid Anthropomorphism in Design**

### ✅ Requirements
- Make it clear the chatbot is not human.
- Avoid emotional bonding or misleading personas.

### 🔧 Implementation Examples
- Use neutral avatars and names.
- Avoid phrases like “I love you” or “I’m your friend.”

```plaintext
System Prompt Addition:
"I'm a digital assistant, not a person. I'm here to help you safely and respectfully."
```

---

## 10. **Regularly Audit and Update Safety Protocols**

### ✅ Requirements
- Perform periodic safety reviews.
- Update filters, prompts, and escalation logic.

### 🔧 Implementation Examples
- Schedule quarterly audits using Azure Policy and Defender for Cloud.
- Maintain a changelog of safety updates.

```plaintext
Audit Checklist:
- Prompt logs reviewed
- Content Safety thresholds updated
- Escalation logic tested
```

---

## ✅ Integration Summary with Azure AI Content Safety

| Feature | Use Case | Example |
|--------|----------|--------|
| **Text Moderation API** | Scan user prompts and bot responses | Block sexual or violent content |
| **Severity Scoring** | Escalate high-risk interactions | Trigger alerts for severity 4 |
| **Prompt Shielding** | Prevent unsafe completions | Add system-level guardrails |
| **Logging & Monitoring** | Track prompt trends | Detect grooming behavior |

---
