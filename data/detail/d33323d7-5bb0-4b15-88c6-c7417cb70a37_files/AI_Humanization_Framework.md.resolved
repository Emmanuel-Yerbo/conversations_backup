# Framework: Building a Text Humanization AI Agent

To build an AI system or "subject" specifically designed to humanize text and reliably bypass strict detectors like Turnitin or ZeroGPT, you cannot just tell the AI to "sound human." You must build a system that mathematically manipulates the two language metrics that detectors look for: **Perplexity** and **Burstiness**.

Here is the architectural blueprint for building this system.

## 1. The Core NLP Concepts to Target

AI detectors do not actually know what a human sounds like. They only look for statistical predictability. Your system must be designed to break these statistics.

*   **High Burstiness (The Structure Trap):** AI writes sentences of very uniform length (e.g., 15 words, 18 words, 16 words). Humans write with high "burstiness" (e.g., a 4-word sentence. Then a massive, rambling 35-word sentence that contains multiple clauses and perhaps an aside. Followed by a 6-word sentence.)
*   **High Perplexity (The Vocabulary Trap):** AI operates by predicting the most statistically likely next word. Predictable text has *low perplexity*. Your system must deliberately choose "sub-optimal" or slightly unexpected word combinations (*high perplexity*) without sacrificing grammatical correctness.

## 2. Multi-Agent Architecture

For the best results, do not use a single agent. Build a **Two-Agent Pipeline**:

1.  **Agent A (The Formulator):** This agent takes the raw facts/requirements and generates a standard, high-quality professional draft. (Basically, a standard LLM output).
2.  **Agent B (The Humanizer / The Disruptor):** This is the agent you are building. It takes the output from Agent A and applies strict "Rule-Based Disruption" to scramble the AI fingerprints.

## 3. The "Humanizer" System Prompt Directives

To code the behavior of your Humanizer subject, feed it a strict systemic meta-prompt containing these exact rules:

### Rule 1: The Transition Ban
*   **Instruction:** Never use robotic transitional adverbs at the beginning of sentences. Utterly ban the words: *Furthermore, Moreover, Additionally, Consequently, Subsequently, In conclusion, Therefore.* 
*   **Human Alternative:** Ask the AI to transition using simple conjunctions (*But, And, So*) or conceptual bridging (starting the next sentence with a reference to the previous idea).

### Rule 2: Variance in Formatting
*   **Instruction:** Radically alter sentence lengths. You must include at least one sentence under 6 words per paragraph. You must include at least one conversational idiom per paragraph (e.g., "getting my hands dirty", "reality check", "half the story").

### Rule 3: Ban "Filler" Action Verbs
*   **Instruction:** AI relies heavily on "academic filler" verbs. Strip out verbs like: *Delve, Navigate, Utilize, Cultivate, Ensure, Facilitate, Equip.* Replace them with grounded, physical, or colloquial equivalents (*e.g., instead of "utilized", use "worked with"; instead of "cultivated", use "built up"*).

### Rule 4: Structural Imperfection (The "Show, Don't Tell" Rule)
*   **Instruction:** Never simply list skills (e.g., "I have skills in Python and GIS"). You must frame skills through an experiential narrative (e.g., "I spent weeks debugging Python mapping libraries before I finally got the GIS coordinates to align"). Provide emotional context or specific hurdles overcome.

## 4. Evaluation Loop (Self-Correction)

If you are building this into a software application, you should integrate an open-source evaluation model (like a local RoBERTa model trained on AI vs. Human text classifications) into your pipeline.

*   **Step 1:** The Humanizer generates the text.
*   **Step 2:** The text is passed locally to the evasion classifier.
*   **Step 3:** If the text scores > 20% AI, it is sent back to the Humanizer with a prompt: *"Your perplexity is too low in paragraph 2. Introduce a 4-word sentence and replace the verb 'demonstrated'."*

## Summary of the Workflow for your Research
If you are developing this as an academic framework or an actual tool:
1.  **Define the Corpus:** Gather a dataset of verified human cover letters/emails, and a dataset of baseline ChatGPT outputs.
2.  **Map the Diff:** Run NLP scripts to measure the exact differences in sentence length standard deviation and n-gram overlap between the two sets.
3.  **Prompt Engineering:** Turn those mathematical differences into qualitative prompt rules (like the ones above).
4.  **Test against Turnitin:** Iterate until you consistently achieve < 15% AI detection.
