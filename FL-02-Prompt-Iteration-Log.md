# Prompt Iteration Log: Fundamentals on Real Tasks (FL-02)

## The Task
**From my FL-01 Audit:** Drafting weekly Student Union (SU) event promotion emails to the American University in Cairo (AUC) student body.

---

## Baseline: The Naive Prompt
**Prompt:** "Write an email to students about our next Student Union event on campus."
**Output Excerpt:** *"Dear Students, We hope this email finds you well. The Student Union is pleased to announce our upcoming event on campus. Please join us for a fun-filled day of activities..."*
**Note on Output:** The output is incredibly robotic. It sounds like a letter from the university administration, not an exciting promotion from the Student Union. It completely lacks identity and event details.

---

## Iteration 1: Role Assignment
**Prompt:** "Act as the Marketing Head for the American University in Cairo (AUC) Student Union. Write an email to students about our next Student Union event on campus."
**Output Excerpt:** *"Hey AUCians! I’m the Head of Marketing for your SU, and I’m thrilled to announce our next big campus event. You won't want to miss what we have planned for you..."*
**Note on Output:** Adding the role shifted the tone drastically. It correctly identified the target audience as "AUCians" and dropped the stiff administrative tone, but it's still hallucinating vague details because I didn't give it any event context.

---

## Iteration 2: Context and Motivation
**Prompt:** "Act as the Marketing Head for the American University in Cairo (AUC) Student Union. We are hosting a massive 'Midterms Unplugged' acoustic concert on the Bartlett Plaza next Thursday at 6 PM. The goal of this email is to drive ticket sales and get students excited to de-stress. Write an email to the student body."
**Output Excerpt:** *"Hey AUCians! Midterms got you stressed? Come de-stress at the 'Midterms Unplugged' acoustic concert next Thursday at 6 PM on the Bartlett Plaza. Buy your tickets now so we can sell out!"*
**Note on Output:** Providing the actual motivation (driving ticket sales/de-stressing) stopped the AI from rambling. The output is now highly relevant and actionable, but it’s a giant wall of text that students will definitely skim past.

---

## Iteration 3: Output Structure
**Prompt:** "Act as the Marketing Head for the American University in Cairo (AUC) Student Union. We are hosting a massive 'Midterms Unplugged' acoustic concert on the Bartlett Plaza next Thursday at 6 PM. The goal of this email is to drive ticket sales and get students excited to de-stress. 
Structure the email as follows: 
1) An attention-grabbing subject line 
2) A short 'Why you should care' hook 
3) A bulleted list of event details (Time, Location, Price) 
4) A direct Call-to-Action to buy tickets."
**Output Excerpt:** 
*"**Subject:** 🎸 Drop the textbooks. Midterms Unplugged is here.
**Why you should care:** You've been living in the library for two weeks. It's time to breathe.
**Details:** 
- When: Thursday, 6 PM
- Where: Bartlett Plaza
**Action:** Get your tickets at the SU booth today."*
**Note on Output:** The output became instantly scannable. By defining the structure, I stopped the AI from writing long paragraphs and forced it to organize the logistics in a way Gen-Z students actually read.

---

## Iteration 4: Few-Shot Examples
**Prompt:** "[Same prompt as Iteration 3], PLUS: Here is an example of our SU brand voice from a past email: 'Hey AUCians, sick of staring at your laptops? Drop the highlighters and come grab free Red Bull at the SU lounge today. No RSVPs, just show up.' Use this exact conversational, punchy tone."
**Output Excerpt:** *"Subject: 🎸 Drop the highlighters. Midterms Unplugged is here.
Hey AUCians, your brain is fried. We get it. Stop staring at Canvas and come vibe at Bartlett Plaza next Thursday..."*
**Note on Output:** This was the biggest leap in quality. Feeding it our actual SU slang ("Drop the highlighters", "Canvas") completely killed the "AI voice". It now perfectly mimics how my student volunteers actually speak to our campus.

---

## Iteration 5: Step Decomposition
**Prompt:** "Act as the Marketing Head for the AUC Student Union writing an event promo email. 
Step 1: Draft three exciting subject lines for a 'Midterms Unplugged' concert. 
Step 2: Write a 2-sentence hook acknowledging how stressful midterms are, using our brand voice ('Hey AUCians, drop the highlighters...').
Step 3: Output a clean bulleted list for the event (Thursday 6 PM, Bartlett Plaza, 150 EGP).
Step 4: End with a one-sentence call to action telling them exactly where the ticket booth is."
**Output Excerpt:** 
*"Step 1 Subject Lines: 1. Unplug from midterms. 2. Bartlett Plaza Acoustic Night. 3. Stop studying. Start listening.
[Followed by the exact sections broken out perfectly]."*
**Note on Output:** Breaking the prompt into strict execution steps made the AI act like a junior copywriter rather than an email generator. It gave me options for the subject line to choose from, rather than just locking me into one choice.

---

## Cross-Model Comparison: Claude vs. ChatGPT
I ran Iteration 5 through both Claude 3.5 Sonnet and ChatGPT (GPT-4o).
- **Tone & Accuracy:** Claude handled the "Few-Shot Example" (our brand voice) much better. It stayed grounded and conversational without being cringe. ChatGPT over-indexed on the "youth marketing" prompt, throwing in about 8 emojis and sounding a bit like a cheesy summer camp counselor trying too hard to relate to students.
- **Structure:** ChatGPT won on structure. It followed the "Step Decomposition" flawlessly on the first try, clearly separating Step 1, 2, 3, and 4. Claude tried to merge Step 2 (the hook) and Step 3 (the bullets) into a single paragraph, requiring a follow-up prompt to fix the formatting.

---

## The Final Reusable Template
*Anyone on the marketing team can use this to generate a perfect campus promo email.*

> Act as the **[Your Role/Organization, e.g., Marketing Head for AUC Student Union]**. 
> We are hosting **[Event Name and 1-sentence description]**. The goal of this email is to **[Primary Goal, e.g., drive ticket sales / get RSVPs]**.
> 
> Please use this exact tone/voice: **[Insert 1-2 sentences of your best past writing as an example]**.
> 
> Execute this task in the following steps:
> **Step 1:** Draft 3 punchy, attention-grabbing subject lines.
> **Step 2:** Write a 2-sentence hook explaining why the audience should care.
> **Step 3:** Output a clean bulleted list of the logistics: **[Insert Date, Time, Location, Price]**.
> **Step 4:** Write a clear, 1-sentence Call to Action telling them exactly how/where to take action: **[Insert CTA link or physical booth location]**.
