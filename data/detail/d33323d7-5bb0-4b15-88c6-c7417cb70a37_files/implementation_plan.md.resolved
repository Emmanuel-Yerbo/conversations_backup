# Implementation Plan: Academic Humanizer PRO Upgrade

This plan outlines the "Industry Standard" upgrade for the Academic Humanizer. We will transition from a single-model mathematical loop to a **Dual-Agent Adversarial System** using **Groq** and **Gemini 1.5 Flash**.

## User Review Required

> [!IMPORTANT]
> **Performance Impact:** The "Pro" mode will be slower (roughly 5-10 seconds per paragraph) because it requires two different AI models (Groq and Gemini) to "negotiate" and audit each other's work.

## Proposed Changes

### [New Project Components]

#### [MODIFY] [humanizer_agent.py](file:///c:/YERBO/Desktop/cover%20leter/CL/humanizer_agent.py)
Update the LangGraph architecture to support a second LLM:
- **Add Gemini 1.5 Flash:** Using the `langchain-google-genai` library.
- **[NEW] Linguistic Audit Node:** This node uses Gemini Flash to specifically scan for "AI Tells" (e.g., words like *meticulous*, *pivotal*, *delve*, *furthermore*) and overly robotic sentence transitions.
- **[NEW] Dual Routing:** The graph will now only finish if **both** the mathematical Burstiness score is high enough AND the Linguistic Audit says "Human-Like."

#### [MODIFY] [humanizer_app.py](file:///c:/YERBO/Desktop/cover%20leter/CL/humanizer_app.py)
Update the Dashboard to support the Pro features:
- **Pro Toggle:** A switch in the sidebar to enable/disable Gemini Auditing.
- **Audit Logs:** A new visual indicator showing what the "Linguistic Auditor" (Gemini) found and corrected.
- **Key Management:** Separate inputs for Groq and Google API keys.

### [Phase 1: Dependency Setup]
- Install `langchain-google-genai`.

### [Phase 2: Linguistic Auditor Logic]
Creating a highly specialized system prompt for Gemini 1.5 Flash that:
1.  Identifies "AI Clutter" (empty academic fluff).
2.  Suggests "Jitter" techniques (e.g., "Change the middle sentence to passive voice to break the rhythm").
3.  Injects "Perplexity" by selecting less common (but still professional) synonyms.

### [Phase 3: Integration & Looping]
Connecting the new Gemini node into the existing LangGraph cycle.

## Open Questions

- **Adversarial Rigor:** Should Gemini have the power to "Reject" a draft and force a full rewrite from Groq, or should Gemini just provide the final "Polish" layer? (I recommend a full rejection loop for maximum evasion).
- **Temperature Settings:** For the Pro mode, should we increase the model "Temperature" (randomness) to further increase human-like variation?

## Verification Plan

### Automated Tests
- Test a known "robotic" paragraph against the Pro Auditor to see if it correctly identifies the "AI Tells."
- Verify that technical entities are still preserved through the multi-model negotiation.

### Manual Verification
- Compare the "Standard" vs "Pro" output across 3 different paragraphs to see the difference in lexicon diversity.
