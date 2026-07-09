# The Prompt Ladder (FL-02)

## Baseline Prompt
**The Prompt:** "Help me write a sponsorship pitch email to a telecom company."
**Output Excerpt:** *"Dear [Telecom Company] Team, I am writing to propose a mutually beneficial partnership between our organizations. We believe that by synergizing our efforts, we can drive unparalleled engagement..."*
**Notes:**
- **What changed:** N/A (Baseline)
- **What improved:** N/A
- **What failed:** The output is a robot-written, buzzword-filled generic template. No telecom executive would ever read past the first sentence.
- **What to try next:** Add real context so it stops making up generic fill-in-the-blank text.

---

## Version 1: Add Context
**The Prompt:** "Help me write a sponsorship pitch email to Orange Egypt. I am the Marketing Head of the AUC Student Union and we want them to sponsor our Welcome Party in exchange for stage branding."
**Output Excerpt:** *"Dear Orange Egypt Sponsorship Team, I am writing to formally propose that Orange sponsors the upcoming AUC Student Union Welcome Party. In exchange for your financial support, we can offer headline stage branding..."*
**Notes:**
- **What changed:** Added the **Real Context** layer (Who I am, who they are, what the exchange is).
- **What improved:** The AI stopped generating placeholders and actually plugged in our real university and brand names.
- **What still failed:** The tone is incredibly stiff. It sounds like a lawyer wrote a formal cover letter instead of a marketing pitch.
- **What to try next:** Add a defined audience so the AI knows who it's actually speaking to.

---

## Version 2: Define Audience
**The Prompt:** "Help me write a sponsorship pitch email to Orange Egypt. I am the Marketing Head of the AUC Student Union and we want them to sponsor our Welcome Party in exchange for stage branding. Write this specifically to the Director of Youth Marketing."
**Output Excerpt:** *"Hi [Name], I know Orange is always looking to capture the youth market in Egypt. As the Marketing Head of the AUC Student Union, I want to offer you the chance to sponsor our Welcome Party..."*
**Notes:**
- **What changed:** Added the **Defined Audience** layer (Director of Youth Marketing).
- **What improved:** It stopped using phrases like "formally propose" and started talking about "capturing the youth market," which aligns perfectly with what that specific director actually cares about.
- **What still failed:** It’s way too long and rambly. It gives three paragraphs of backstory about the university that a busy director doesn't have time to read.
- **What to try next:** Add a constraint on length to force brevity.

---

## Version 3: Add Constraint (The "Made it Worse" Moment)
**The Prompt:** "Help me write a sponsorship pitch email to Orange Egypt. I am the Marketing Head of the AUC Student Union and we want them to sponsor our Welcome Party in exchange for stage branding. Write this specifically to the Director of Youth Marketing. Keep the entire email under 4 sentences."
**Output Excerpt:** *"Hi [Name], As the Marketing Head of the AUC SU, I want to offer Orange Egypt the headline stage branding for our Welcome Party. This is a unique opportunity to reach thousands of Gen Z students. We are desperately looking for a sponsorship to make this happen. Let's discuss this mutually beneficial partnership soon."*
**Notes:**
- **What changed:** Added a **Constraint** layer (Keep it under 4 sentences).
- **What improved:** The length is finally readable at a glance.
- **What still failed (Made it worse):** By squishing it into exactly 4 sentences, the AI panicked and removed all the actual value. It lost the confident "hook" and made me sound desperate ("looking for a sponsorship to make this happen"). It completely backfired.
- **What to try next:** Drop the strict sentence count constraint and replace it with a specific output structure.

---

## Version 4: Output Format
**The Prompt:** "Help me write a sponsorship pitch email to Orange Egypt. I am the Marketing Head of the AUC Student Union and we want them to sponsor our Welcome Party in exchange for stage branding. Write this specifically to the Director of Youth Marketing. Structure the email as: 1. The Hook (Why they care), 2. The Offer (What we give them), 3. The Ask (What we want), 4. A low-friction Call to Action."
**Output Excerpt:** 
*"Hi [Name], 
Orange has a massive opportunity to capture the Gen-Z demographic at AUC this fall. 
I am offering you the headline stage branding for the AUC Welcome Party, giving you exclusive access to thousands of students. 
We are asking for a cash sponsorship to cover event overhead. 
Do you have 10 minutes next week for a quick call?"*
**Notes:**
- **What changed:** Added an **Output Format** layer (Hook, Offer, Ask, CTA).
- **What improved:** The email became incredibly scannable. Breaking it into specific psychological beats forced the AI to be punchy and structured like a real B2B sales email without sounding desperate.
- **What still failed:** It’s missing hard numbers. It says "thousands of students" instead of actual data, making the pitch sound amateur.
- **What to try next:** Add quality criteria (must include specific metrics and ban AI buzzwords).

---

## Version 5: Quality Criteria (Final Polish)
**The Prompt:** "Help me write a sponsorship pitch email to Orange Egypt. I am the Marketing Head of the AUC Student Union and we want them to sponsor our Welcome Party in exchange for stage branding. Write this specifically to the Director of Youth Marketing. Structure the email as: 1. The Hook (Why they care), 2. The Offer (What we give them), 3. The Ask (What we want), 4. A low-friction Call to Action. Quality Criteria: The email must include hard data (4,500 expected students, 145k Instagram impressions) and must not use the words 'synergy', 'partnership', 'delve', or 'mutually beneficial'."
**Output Excerpt:** 
*"Hi [Name], 
Orange has a massive window to capture the university demographic this fall. 
As Marketing Head for the AUC Student Union, I'm offering you the headline stage branding for our Welcome Party, giving you exclusive access to 4,500 Gen-Z students in a single night and a projected 145k organic Reels impressions. 
We are asking for 100k EGP to cover production overhead. 
Do you have 5 minutes next Tuesday to see if this aligns with your Q3 marketing goals?"*
**Notes:**
- **What changed:** Added a **Quality Criteria** layer (Include specific data, ban specific buzzwords).
- **What improved:** The email finally sounds like a seasoned professional wrote it. Banning the corporate buzzwords killed the "AI voice" entirely, and forcing the hard data into the Offer section made the pitch irresistible.
- **What still failed:** Nothing. It's ready to send.

---

## Final Reusable Prompt (For Anyone to Steal)
*Take this and fill in your own brackets to get a perfect, non-robotic pitch email every time.*

> Write a pitch email to **[Target Company]**. 
> Context: I am **[Your Role/Organization]** offering **[What you are offering]**.
> Audience: Write this specifically to the **[Decision Maker Title]**.
> Structure the email into four strict beats:
> 1. The Hook (Why they should care about this specific demographic/opportunity)
> 2. The Offer (Exactly what we give them)
> 3. The Ask (Exactly what we want)
> 4. A low-friction Call to Action (e.g., asking for a 5-minute call)
> Quality Criteria: You must seamlessly include these specific metrics: **[Insert your hard data/ROI numbers here]**. You must NOT use words like 'synergy', 'partnership', 'mutually beneficial', 'delve', or 'leverage'. Keep the tone direct, confident, and pragmatic.
