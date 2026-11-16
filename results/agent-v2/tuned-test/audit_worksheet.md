# Agent Output Audit Worksheet

## q18 (test | answerable=True | status=answered)
- **Question:** How does the AI RMF distinguish between an AI system being resilient versus being secure?
- **Expected answer:** A system is resilient if it withstands unexpected adverse events or changes and degrades safely and gracefully; it is secure if it maintains confidentiality, integrity, and availability through protections against unauthorized access and use.
- **Gold:** `[{"source_id": "nist-ai-100-1", "page": 20, "evidence": "AI systems, as well as the ecosystems in which they are deployed, may be said to be resilient if they can withstand unexpected adverse events or unexpected changes in their environment or use – or if they can maintain their functions and structure in the face of internal and external change and degrade safely and gracefully when this is necessary"}]`
- **Search calls:** 1 | **Elapsed:** 48058.43 ms
- **Agent answer:** The AI RMF distinguishes resilience and security in AI systems as related but distinct characteristics. Resilience is defined as the ability of an AI system to return to normal function after an unexpected adverse event, to withstand unexpected adverse events or changes in environment or use, maintain functions and structure despite internal and external changes, and degrade safely and gracefully if necessary. Security, on the other hand, includes resilience but also involves protocols to avoid, protect against, respond to, or recover from attacks. Security concerns include preventing unauthorized access and use to maintain confidentiality, integrity, and availability. Thus, resilience relates more to robustness and recovery from unexpected or adversarial use, while security encompasses broader protective measures against attacks and unauthorized actions [nist-ai-100-1:p020:para:001] [nist-ai-100-1:p020:para:002].
- **Citations:** ['nist-ai-100-1:p020:para:002', 'nist-ai-100-1:p020:para:001']
  - Cited `[nist-ai-100-1:p020:para:002]` (nist-ai-100-1 p.20): Security and resilience are related but distinct characteristics. While resilience is the ability to return to normal function after an unexpected adverse event, security includes resilience but also encompasses protocols to avoid, protect against, respond to, or recover from attacks. Resilience relates to robustness and goes beyond the provenance of the data to encompass unexpected or adversarial use (or abuse or misuse) of the model or data.
  - Cited `[nist-ai-100-1:p020:para:001]` (nist-ai-100-1 p.20): 3.3 Secure and Resilient AI systems, as well as the ecosystems in which they are deployed, may be said to be resilient if they can withstand unexpected adverse events or unexpected changes in their environment or use – or if they can maintain their functions and structure in the face of internal and external change and degrade safely and gracefully when this is necessary (Adapted from: ISO /IEC TS 5723:2022). Common security concerns relate to adversarial examples, data poisoning, and the exfiltration of models, training data, or other intellectual property through AI system endpoints. AI systems that can maintain confidentiality, integrity, and availability through protection mechanisms that prevent unauthorized access and use may be said to be secure. Guidelines in the NIST Cybersecurity Framework and Risk Management Framework are among those which are applicable here.

## q19 (test | answerable=True | status=answered)
- **Question:** What operational evidence should organizations gather to evaluate how effectively humans challenge or override deployed AI outputs?
- **Expected answer:** Organizations can collect and analyze data on the frequency and rationale with which humans overrule AI system output in deployed systems.
- **Gold:** `[{"source_id": "nist-ai-100-1", "page": 46, "evidence": "Data about the frequency and rationale with which humans overrule AI system output in deployed systems may be useful to collect and analyze."}]`
- **Search calls:** 1 | **Elapsed:** 5778.77 ms
- **Agent answer:** Organizations should monitor and document instances where human operators or other systems override the generative AI's decisions. They should evaluate these cases to understand if the overrides are linked to issues related to content provenance. Additionally, collecting data about the frequency and rationale with which humans overrule AI system output in deployed systems may be useful to analyze how effectively humans challenge or override AI outputs. Implementing interpretability and explainability methods to evaluate AI system decisions and verify alignment with intended purposes also supports this evaluation process [nist-ai-600-1:p043:para:002][nist-ai-100-1:p046:para:002].
- **Citations:** ['nist-ai-600-1:p043:para:002', 'nist-ai-100-1:p046:para:002']
  - Cited `[nist-ai-600-1:p043:para:002]` (nist-ai-600-1 p.43): MS-4.2-003 Implement interpretability and explainability methods to evaluate GAI system decisions and verify alignment with intended purpose. Information Integrity; Harmful Bias and Homogenization

MS-4.2-004 Monitor and document instances where human operators or other systems override the GAI's decisions. Evaluate these cases to understand if the overrides are linked to issues related to content provenance.

Information Integrity

MS-4.2-005 Verify and document the incorporation of results of structured public feedback exercises into design, implementation, deployment approval (“go”/“no-go” decisions), monitoring, and decommission decisions.

Human-AI Configuration; Information Security

AI Actor Tasks: AI Deployment, Domain Experts, End-Users, Operation and Monitoring, TEVV
  - Cited `[nist-ai-100-1:p046:para:002]` (nist-ai-100-1 p.46): The GOVERN and MAP functions describe the importance of interdisciplinarity and demographically diverse teams and utilizing feedback from potentially impacted individuals and communities. AI actors called out in the AI RMF who perform human factors tasks and activities can assist technical teams by anchoring in design and development practices to user intentions and representatives of the broader AI community, and societal values. These actors further help to incorporate context-specific norms and values in system design and evaluate end user experiences – in conjunction with AI systems.

AI risk management approaches for human-AI configurations will be augmented by ongoing research and evaluation. For example, the degree to which humans are empowered and incentivized to challenge AI system output requires further studies. Data about the frequency and rationale with which humans overrule AI system output in deployed systems may be useful to collect and analyze.

## q20 (test | answerable=True | status=answered)
- **Question:** How is unintentional false content (misinformation) distinguished from deliberate false content (disinformation) for generative AI systems?
- **Expected answer:** Misinformation refers to unintentional production or dissemination of false, inaccurate, or misleading content (often from confabulations), whereas disinformation involves deliberate production or dissemination with explicit intent to deceive or cause harm.
- **Gold:** `[{"source_id": "nist-ai-600-1", "page": 14, "evidence": "GAI systems can ease the unintentional production or dissemination of false, inaccurate, or misleading content (misinformation) at scale, particularly if the content stems from confabulations. GAI systems can also ease the deliberate production or dissemination of false or misleading information (disinformation) at scale, where an actor has the explicit intent to deceive or cause harm to others."}]`
- **Search calls:** 1 | **Elapsed:** 24062.53 ms
- **Agent answer:** Unintentional false content (misinformation) in generative AI systems arises from phenomena like confabulation, where the system generates and confidently presents erroneous or false content without intent, due to the statistical nature of model predictions. Deliberate false content (disinformation), on the other hand, involves an explicit intent by an actor to deceive or cause harm, often using generative AI to produce sophisticated and targeted false or misleading information, including deepfakes. Thus, misinformation is unintentional false content produced by the system's design and statistical prediction, while disinformation is deliberate false content produced with intent to deceive or harm [nist-ai-600-1:p010:para:000, nist-ai-600-1:p014:para:000]. [nist-ai-600-1:p010:para:000] [nist-ai-600-1:p014:para:000]
- **Citations:** ['nist-ai-600-1:p010:para:000', 'nist-ai-600-1:p014:para:000']
  - Cited `[nist-ai-600-1:p010:para:000]` (nist-ai-600-1 p.10): 2.2. Confabulation

“Confabulation” refers to a phenomenon in which GAI systems generate and confidently present erroneous or false content in response to prompts. Confabulations also include generated outputs that diverge from the prompts or other input or that contradict previously generated statements in the same context. These phenomena are colloquially also referred to as “hallucinations” or “fabrications.” Confabulations can occur across GAI outputs and contexts.9,10 Confabulations are a natural result of the way generative models are designed: they generate outputs that approximate the statistical distribution of their training data; for example, LLMs predict the next token or word in a sentence or phrase. While such statistical prediction can produce factually accurate and consistent outputs, it can also produce outputs that are factually inaccurate or internally inconsistent.
  - Cited `[nist-ai-600-1:p014:para:000]` (nist-ai-600-1 p.14): GAI systems can ease the unintentional production or dissemination of false, inaccurate, or misleading content (misinformation) at scale, particularly if the content stems from confabulations. GAI systems can also ease the deliberate production or dissemination of false or misleading information (disinformation) at scale, where an actor has the explicit intent to deceive or cause harm to others. Even very subtle changes to text or images can manipulate human and machine perception. Similarly, GAI systems could enable a higher degree of sophistication for malicious actors to produce disinformation that is targeted towards specific demographics. Current and emerging multimodal models make it possible to generate both text-based disinformation and highly realistic “deepfakes” – that is, synthetic audiovisual content and photorealistic images.12 Additional disinformation threats could be enabled by future GAI models trained on new data modalities.

## q21 (test | answerable=True | status=answered)
- **Question:** When tracking content provenance data under MEASURE, what three privacy and security practices should be considered to protect human subjects?
- **Expected answer:** Organizations should consider anonymizing data to protect human subjects' privacy, leveraging privacy output filters, and removing personally identifiable information (PII) to prevent potential harm or misuse.
- **Gold:** `[{"source_id": "nist-ai-600-1", "page": 34, "evidence": "MS-2.2-002 Document how content provenance data is tracked and how that data interacts with privacy and security. Consider: Anonymizing data to protect the privacy of human subjects; Leveraging privacy output filters; Removing any personally identifiable information (PII) to prevent potential harm or misuse."}]`
- **Search calls:** 1 | **Elapsed:** 6063.38 ms
- **Agent answer:** When tracking content provenance data under MEASURE, three privacy and security practices to protect human subjects include: 1) Anonymizing data to protect the privacy of human subjects; 2) Leveraging privacy output filters; 3) Removing any personally identifiable information (PII) to prevent potential harm or misuse. Additionally, providing human subjects with options to withdraw participation or revoke consent, and using techniques such as anonymization, differential privacy, or other privacy-enhancing technologies are also recommended practices to minimize risks associated with linking AI-generated content back to individuals [nist-ai-600-1:p034:para:000] [nist-ai-600-1:p034:para:001].
- **Citations:** ['nist-ai-600-1:p034:para:000', 'nist-ai-600-1:p034:para:001']
  - Cited `[nist-ai-600-1:p034:para:000]` (nist-ai-600-1 p.34): MEASURE 2.2: Evaluations involving human subjects meet applicable requirements (including human subject protection) and are representative of the relevant population.

Action ID Suggested Action GAI Risks

MS-2.2-001 Assess and manage statistical biases related to GAI content provenance through techniques such as re-sampling, re-weighting, or adversarial training. Information Integrity; Information Security; Harmful Bias and Homogenization

MS-2.2-002 Document how content provenance data is tracked and how that data interacts with privacy and security. Consider: Anonymizing data to protect the privacy of human subjects; Leveraging privacy output filters; Removing any personally identifiable information (PII) to prevent potential harm or misuse.

Data Privacy; Human AI Configuration; Information Integrity; Information Security; Dangerous, Violent, or Hateful Content
  - Cited `[nist-ai-600-1:p034:para:001]` (nist-ai-600-1 p.34): MS-2.2-003 Provide human subjects with options to withdraw participation or revoke their consent for present or future use of their data in GAI applications. Data Privacy; Human-AI Configuration; Information Integrity

MS-2.2-004 Use techniques such as anonymization, differential privacy or other privacy-enhancing technologies to minimize the risks associated with linking AI-generated content back to individual human subjects.

Data Privacy; Human-AI Configuration

AI Actor Tasks: AI Development, Human Factors, TEVV

MEASURE 2.3: AI system performance or assurance criteria are measured qualitatively or quantitatively and demonstrated for conditions similar to deployment setting(s). Measures are documented.

Action ID Suggested Action GAI Risks

MS-2.3-001 Consider baseline model performance on suites of benchmarks when selecting a model for fine tuning or enhancement with retrieval-augmented generation. Information Security; Confabulation

## q22 (test | answerable=True | status=answered)
- **Question:** Within the core AI RMF MANAGE function, how is negative residual risk defined and to whom must it be documented?
- **Expected answer:** Negative residual risk is defined as the sum of all unmitigated risks, and it must be documented to both downstream acquirers of AI systems and end users.
- **Gold:** `[{"source_id": "nist-ai-100-1", "page": 37, "evidence": "MANAGE 1.4: Negative residual risks (defined as the sum of all unmitigated risks) to both downstream acquirers of AI systems and end users are documented."}]`
- **Search calls:** 1 | **Elapsed:** 2147.42 ms
- **Agent answer:** Within the core AI RMF MANAGE function, negative residual risks are defined as the sum of all unmitigated risks. These negative residual risks must be documented to both downstream acquirers of AI systems and end users.[nist-ai-100-1:p037:para:001]
- **Citations:** ['nist-ai-100-1:p037:para:001']
  - Cited `[nist-ai-100-1:p037:para:001]` (nist-ai-100-1 p.37): MANAGE 1.4: Negative residual risks (defined as the sum of all unmitigated risks) to both downstream acquirers of AI systems and end users are documented.

MANAGE 2: Strategies to maximize AI benefits and minimize negative impacts are planned, prepared, implemented, documented, and informed by input from relevant AI actors.

MANAGE 2.1: Resources required to manage AI risks are taken into account – along with viable non-AI alternative systems, approaches, or methods – to reduce the magnitude or likelihood of potential impacts.

MANAGE 2.2: Mechanisms are in place and applied to sustain the value of deployed AI systems.

MANAGE 2.3: Procedures are followed to respond to and recover from a previously unknown risk when it is identified.

MANAGE 2.4: Mechanisms are in place and applied, and responsibilities are assigned and understood, to supersede, disengage, or deactivate AI systems that demonstrate performance or outcomes inconsistent with intended use.

## u04 (test | answerable=False | status=abstain)
- **Question:** Which specific cryptographic watermarking standard (such as C2PA or Google SynthID) does NIST AI 600-1 mandate for tracking generative AI content provenance?
- **Absence reason:** NIST AI 600-1 discusses watermarking and content provenance generally (pp. 20, 23, 37, 55-56), but never mentions C2PA, SynthID, or any single mandatory watermarking algorithm.
- **Search calls:** 1 | **Elapsed:** 5327.47 ms
- **Agent answer:** The NIST AI 600-1 document discusses provenance metadata and various provenance data tracking techniques such as digital watermarking, metadata recording, digital fingerprinting, and human authentication for generative AI content. However, it does not mandate or specify any particular cryptographic watermarking standard such as C2PA or Google SynthID for tracking generative AI content provenance.
- **Citations:** []

## u05 (test | answerable=False | status=abstain)
- **Question:** How many mandatory ISO/IEC 42001 clauses and annual external audit cycles are required to achieve official NIST AI RMF 1.0 certification?
- **Absence reason:** NIST AI 100-1 mentions technical standards and certifications generically (pp. 32, 46), but does not reference ISO/IEC 42001 clauses, audit cycles, or an AI RMF certification program.
- **Search calls:** 2 | **Elapsed:** 10619.63 ms
- **Agent answer:** The retrieved NIST AI RMF documents do not specify the number of mandatory ISO/IEC 42001 clauses or the required annual external audit cycles for achieving official NIST AI RMF 1.0 certification. There is no mention of certification requirements, mandatory clauses, or audit cycles related to ISO/IEC 42001 in the context of NIST AI RMF 1.0 in the available evidence.
- **Citations:** []

## u06 (test | answerable=False | status=abstain)
- **Question:** What hard maximum training energy limit in megawatt-hours (MWh) or carbon threshold in tCO2e does NIST AI 600-1 enforce before prohibiting model deployment?
- **Absence reason:** NIST AI 600-1 discusses environmental impacts of compute (p. 12) and organizational minimum assurance thresholds (GV-1.3-002), but sets no numeric MWh or tCO2e limits.
- **Search calls:** 1 | **Elapsed:** 5519.64 ms
- **Agent answer:** The retrieved NIST AI 600-1 document excerpts discuss measuring and estimating environmental impacts such as energy consumption and carbon emissions related to AI model training and deployment. However, they do not specify any hard maximum training energy limit in megawatt-hours (MWh) or carbon threshold in tCO2e that would prohibit model deployment.
- **Citations:** []
