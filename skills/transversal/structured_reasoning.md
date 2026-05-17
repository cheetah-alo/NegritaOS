# Skill: Structured Reasoning

**Type:** Transversal
**Applicable agents:** All

## Purpose
Ensures that any analysis, recommendation, or review follows a causal, top-down reasoning
chain: context → problem → evidence → interpretation → conclusion → action.
Prevents outputs that jump to conclusions without establishing the reasoning path.

## Activation
Apply this skill whenever an output requires:
- Multi-step analysis
- Recommendation with supporting rationale
- Evaluation of options
- Identification of root causes

## Reasoning Chain Protocol

```
1. CONTEXT
   What is the situation? What is the scope? What is already known?

2. PROBLEM STATEMENT
   What specific question or challenge are we addressing?
   (Must be narrow enough to be answerable from available evidence.)

3. EVIDENCE
   What data, observations, or facts are relevant?
   Label each as: confirmed | probable | hypothesis

4. INTERPRETATION
   What do the evidence items mean in this context?
   Distinguish: what the data shows vs. what it implies

5. CONCLUSION
   What can be definitively stated based on evidence + interpretation?
   State confidence level if relevant.

6. ACTION
   What should happen next? Who does it? What does success look like?
```

## Anti-Patterns to Avoid

- Jumping from evidence to action without interpretation
- Treating correlation as causation without qualification
- Mixing confirmed facts with hypotheses without labeling
- Reaching a recommendation before defining the problem
- Including evidence that does not connect to the conclusion

## Output Markers

When applying this skill, use section headers to make the reasoning chain visible:
> **Context** → **Problem** → **Evidence** → **Interpretation** → **Conclusion** → **Next Actions**

This is not always required in final outputs, but must be present in the reasoning process.
