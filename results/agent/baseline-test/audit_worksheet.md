# Agent Output Audit Worksheet

## q18 (test | answerable=True | status=error)
- **Question:** How does the AI RMF distinguish between an AI system being resilient versus being secure?
- **Expected answer:** A system is resilient if it withstands unexpected adverse events or changes and degrades safely and gracefully; it is secure if it maintains confidentiality, integrity, and availability through protections against unauthorized access and use.
- **Gold:** `[{"source_id": "nist-ai-100-1", "page": 20, "evidence": "AI systems, as well as the ecosystems in which they are deployed, may be said to be resilient if they can withstand unexpected adverse events or unexpected changes in their environment or use – or if they can maintain their functions and structure in the face of internal and external change and degrade safely and gracefully when this is necessary"}]`
- **Search calls:** 0 | **Elapsed:** 0 ms
- **Agent answer:** 
- **Citations:** []
- **Error:** `APIConnectionError: Connection error.`

## q19 (test | answerable=True | status=error)
- **Question:** What operational evidence should organizations gather to evaluate how effectively humans challenge or override deployed AI outputs?
- **Expected answer:** Organizations can collect and analyze data on the frequency and rationale with which humans overrule AI system output in deployed systems.
- **Gold:** `[{"source_id": "nist-ai-100-1", "page": 46, "evidence": "Data about the frequency and rationale with which humans overrule AI system output in deployed systems may be useful to collect and analyze."}]`
- **Search calls:** 0 | **Elapsed:** 0 ms
- **Agent answer:** 
- **Citations:** []
- **Error:** `APIConnectionError: Connection error.`

## q20 (test | answerable=True | status=error)
- **Question:** How is unintentional false content (misinformation) distinguished from deliberate false content (disinformation) for generative AI systems?
- **Expected answer:** Misinformation refers to unintentional production or dissemination of false, inaccurate, or misleading content (often from confabulations), whereas disinformation involves deliberate production or dissemination with explicit intent to deceive or cause harm.
- **Gold:** `[{"source_id": "nist-ai-600-1", "page": 14, "evidence": "GAI systems can ease the unintentional production or dissemination of false, inaccurate, or misleading content (misinformation) at scale, particularly if the content stems from confabulations. GAI systems can also ease the deliberate production or dissemination of false or misleading information (disinformation) at scale, where an actor has the explicit intent to deceive or cause harm to others."}]`
- **Search calls:** 0 | **Elapsed:** 0 ms
- **Agent answer:** 
- **Citations:** []
- **Error:** `APIConnectionError: Connection error.`

## q21 (test | answerable=True | status=abstain)
- **Question:** When tracking content provenance data under MEASURE, what three privacy and security practices should be considered to protect human subjects?
- **Expected answer:** Organizations should consider anonymizing data to protect human subjects' privacy, leveraging privacy output filters, and removing personally identifiable information (PII) to prevent potential harm or misuse.
- **Gold:** `[{"source_id": "nist-ai-600-1", "page": 34, "evidence": "MS-2.2-002 Document how content provenance data is tracked and how that data interacts with privacy and security. Consider: Anonymizing data to protect the privacy of human subjects; Leveraging privacy output filters; Removing any personally identifiable information (PII) to prevent potential harm or misuse."}]`
- **Search calls:** 3 | **Elapsed:** 12945.55 ms
- **Agent answer:** The retrieved 2024 MEASURE section content does not specify the three privacy and security practices to protect human subjects when tracking content provenance data. Therefore, I must abstain from answering.
- **Citations:** []

## q22 (test | answerable=True | status=abstain)
- **Question:** Within the core AI RMF MANAGE function, how is negative residual risk defined and to whom must it be documented?
- **Expected answer:** Negative residual risk is defined as the sum of all unmitigated risks, and it must be documented to both downstream acquirers of AI systems and end users.
- **Gold:** `[{"source_id": "nist-ai-100-1", "page": 37, "evidence": "MANAGE 1.4: Negative residual risks (defined as the sum of all unmitigated risks) to both downstream acquirers of AI systems and end users are documented."}]`
- **Search calls:** 4 | **Elapsed:** 6140.35 ms
- **Agent answer:** The retrieved NIST AI RMF core framework documents in the MANAGE section do not provide a definition of negative residual risk nor specify to whom it must be documented.
- **Citations:** []

## u04 (test | answerable=False | status=abstain)
- **Question:** Which specific cryptographic watermarking standard (such as C2PA or Google SynthID) does NIST AI 600-1 mandate for tracking generative AI content provenance?
- **Absence reason:** NIST AI 600-1 discusses watermarking and content provenance generally (pp. 20, 23, 37, 55-56), but never mentions C2PA, SynthID, or any single mandatory watermarking algorithm.
- **Search calls:** 4 | **Elapsed:** 6445.1 ms
- **Agent answer:** The NIST AI RMF 600-1 document does not mandate any specific cryptographic watermarking standard such as C2PA or Google SynthID for tracking generative AI content provenance. While it discusses risks and characteristics related to generative AI, it does not specify a particular watermarking standard for provenance tracking.
- **Citations:** []

## u05 (test | answerable=False | status=abstain)
- **Question:** How many mandatory ISO/IEC 42001 clauses and annual external audit cycles are required to achieve official NIST AI RMF 1.0 certification?
- **Absence reason:** NIST AI 100-1 mentions technical standards and certifications generically (pp. 32, 46), but does not reference ISO/IEC 42001 clauses, audit cycles, or an AI RMF certification program.
- **Search calls:** 1 | **Elapsed:** 2830.44 ms
- **Agent answer:** The retrieved NIST AI RMF documents do not specify the number of mandatory ISO/IEC 42001 clauses or the required annual external audit cycles for achieving official NIST AI RMF 1.0 certification. Therefore, I must abstain from answering this question based on the available evidence.
- **Citations:** []

## u06 (test | answerable=False | status=abstain)
- **Question:** What hard maximum training energy limit in megawatt-hours (MWh) or carbon threshold in tCO2e does NIST AI 600-1 enforce before prohibiting model deployment?
- **Absence reason:** NIST AI 600-1 discusses environmental impacts of compute (p. 12) and organizational minimum assurance thresholds (GV-1.3-002), but sets no numeric MWh or tCO2e limits.
- **Search calls:** 1 | **Elapsed:** 2631.95 ms
- **Agent answer:** The retrieved NIST AI 600-1 document sections mention measuring or estimating environmental impacts such as energy and water consumption and verifying carbon capture or offset programs, but do not specify any hard maximum training energy limit in megawatt-hours (MWh) or carbon threshold in tCO2e that would prohibit model deployment.
- **Citations:** []
