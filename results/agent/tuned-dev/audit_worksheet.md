# Agent Output Audit Worksheet

## q01 (dev | answerable=True | status=answered)
- **Question:** How does the AI RMF define risk tolerance, and does the framework prescribe a specific acceptable risk level?
- **Expected answer:** Risk tolerance is an organization's or AI actor's readiness to bear risk in order to achieve its objectives; the AI RMF does not prescribe risk tolerance because it is contextual and application/use-case specific.
- **Gold:** `[{"source_id": "nist-ai-100-1", "page": 12, "evidence": "While the AI RMF can be used to prioritize risk, it does not prescribe risk tolerance. Risk tolerance refers to the organization’s or AI actor’s (see Appendix A) readiness to bear the risk in order to achieve its objectives."}]`
- **Search calls:** 1 | **Elapsed:** 15126.96 ms
- **Agent answer:** The AI RMF defines risk tolerance as the organization's or AI actor's readiness to bear risk in order to achieve its objectives. It notes that risk tolerance is influenced by legal or regulatory requirements and is highly contextual, varying by application, use case, organizational priorities, and evolving policies and norms. The framework explicitly states that it does not prescribe a specific risk tolerance or acceptable risk level. Instead, it is intended to be flexible and augment existing risk practices aligned with applicable laws, regulations, and norms. Organizations are advised to follow existing regulations and guidelines for risk criteria, tolerance, and response, or define reasonable risk tolerance where such guidelines do not exist, using the AI RMF to manage and document risk management processes accordingly [nist-ai-100-1:p012:para:000][nist-ai-100-1:p012:para:002].
- **Citations:** ['nist-ai-100-1:p012:para:000', 'nist-ai-100-1:p012:para:002']
  - Cited `[nist-ai-100-1:p012:para:000]` (nist-ai-100-1 p.12): 1.2.2 Risk Tolerance

While the AI RMF can be used to prioritize risk, it does not prescribe risk tolerance. Risk tolerance refers to the organization’s or AI actor’s (see Appendix A) readiness to bear the risk in order to achieve its objectives. Risk tolerance can be influenced by legal or regulatory requirements (Adapted from: ISO GUIDE 73). Risk tolerance and the level of risk that is acceptable to organizations or society are highly contextual and application and use-case specific. Risk tolerances can be influenced by policies and norms established by AI system owners, organizations, industries, communities, or policy makers. Risk tolerances are likely to change over time as AI systems, policies, and norms evolve. Different organizations may have varied risk tolerances due to their particular organizational priorities and resource considerations.
  - Cited `[nist-ai-100-1:p012:para:002]` (nist-ai-100-1 p.12): The Framework is intended to be flexible and to augment existing risk practices which should align with applicable laws, regulations, and norms. Organizations should follow existing regulations and guidelines for risk criteria, tolerance, and response established by organizational, domain, discipline, sector, or professional requirements. Some sectors or industries may have established definitions of harm or established documentation, reporting, and disclosure requirements. Within sectors, risk management may depend on existing guidelines for specific applications and use case settings. Where established guidelines do not exist, organizations should define reasonable risk tolerance. Once tolerance is defined, this AI RMF can be used to manage risks and to document risk management processes.

## q02 (dev | answerable=True | status=answered)
- **Question:** Why can attempting to eliminate all negative AI risk completely be counterproductive in practice?
- **Expected answer:** Because not all incidents and failures can be eliminated, and unrealistic risk expectations can lead organizations to allocate resources in ways that make risk triage inefficient, impractical, or wasteful.
- **Gold:** `[{"source_id": "nist-ai-100-1", "page": 12, "evidence": "Attempting to eliminate negative risk entirely can be counterproductive in practice because not all incidents and failures can be eliminated. Unrealistic expectations about risk may lead organizations to allocate resources in a manner that makes risk triage inefficient or impractical or wastes scarce resources."}]`
- **Search calls:** 1 | **Elapsed:** 21504.02 ms
- **Agent answer:** Attempting to eliminate all negative AI risk completely can be counterproductive in practice because not all incidents and failures can be eliminated. Unrealistic expectations about risk may lead organizations to allocate resources inefficiently or impractically, wasting scarce resources. Instead, a risk management culture helps organizations recognize that not all AI risks are the same, allowing purposeful allocation of resources based on assessed risk levels and potential impacts. Prioritizing risks that are highest for AI systems in a given context ensures that the most urgent risks receive thorough management, while lower-risk systems may receive lower prioritization. In cases of unacceptable negative risk, development and deployment should cease safely until risks are managed sufficiently [nist-ai-100-1:p012:para:003][nist-ai-100-1:p013:para:000].
- **Citations:** ['nist-ai-100-1:p012:para:003', 'nist-ai-100-1:p013:para:000']
  - Cited `[nist-ai-100-1:p012:para:003]` (nist-ai-100-1 p.12): 1.2.3 Risk Prioritization Attempting to eliminate negative risk entirely can be counterproductive in practice because not all incidents and failures can be eliminated. Unrealistic expectations about risk may lead organizations to allocate resources in a manner that makes risk triage inefficient or impractical or wastes scarce resources. A risk management culture can help organizations recognize that not all AI risks are the same, and resources can be allocated purposefully. Actionable risk management efforts lay out clear guidelines for assessing trustworthiness of each AI system an organization develops or deploys. Policies and resources should be prioritized based on the assessed risk level and potential impact of an AI system. The extent to which an AI system may be customized or tailored to the specific context of use by the AI deployer can be a contributing factor.
  - Cited `[nist-ai-100-1:p013:para:000]` (nist-ai-100-1 p.13): When applying the AI RMF, risks which the organization determines to be highest for the AI systems within a given context of use call for the most urgent prioritization and most thorough risk management process. In cases where an AI system presents unacceptable negative risk levels – such as where significant negative impacts are imminent, severe harms are actually occurring, or catastrophic risks are present – development and deployment should cease in a safe manner until risks can be sufficiently managed. If an AI system’s development, deployment, and use cases are found to be low-risk in a specific context, that may suggest potentially lower prioritization.

## q03 (dev | answerable=True | status=answered)
- **Question:** What organizational separation of duties is recommended as a best practice between those building AI models and those testing or validating them?
- **Expected answer:** As a best practice in the AI Model dimension, AI actors building and using models should be separated from those verifying and validating the models.
- **Gold:** `[{"source_id": "nist-ai-100-1", "page": 16, "evidence": "Note that AI actors in the AI Model dimension (Figure 2) are separated as a best practice, with those building and using the models separated from those verifying and validating the models."}]`
- **Search calls:** 1 | **Elapsed:** 5819.44 ms
- **Agent answer:** The NIST AI RMF recommends as a best practice that AI actors involved in building and using AI models should be organizationally separated from those responsible for verifying and validating the models. This separation of duties helps ensure independent testing, evaluation, verification, and validation tasks, which are distinct from the development tasks such as model building and interpretation. This organizational separation supports integrity and objectivity in the AI lifecycle, particularly in the AI Model phase where development and TEVV (Test, Evaluation, Verification, and Validation) tasks occur separately.[nist-ai-100-1:p016:para:000] [nist-ai-100-1:p040:para:002]
- **Citations:** ['nist-ai-100-1:p016:para:000', 'nist-ai-100-1:p040:para:002']
  - Cited `[nist-ai-100-1:p016:para:000]` (nist-ai-100-1 p.16): Fig. 3. AI actors across AI lifecycle stages. See Appendix A for detailed descriptions of AI actor tasks, including details about testing, evaluation, verification, and validation tasks. Note that AI actors in the AI Model dimension (Figure 2) are separated as a best practice, with those building and using the models separated from those verifying and validating the models.
  - Cited `[nist-ai-100-1:p040:para:002]` (nist-ai-100-1 p.40): AI Development tasks are performed during the AI Model phase of the lifecycle in Figure

2. AI Development actors provide the initial infrastructure of AI systems and are responsible for model building and interpretation tasks, which involve the creation, selection, calibration, training, and/or testing of models or algorithms. AI actors in this category include machine learning experts, data scientists, developers, third-party entities, legal and privacy governance experts, and experts in the socio-cultural and contextual factors associated with the deployment setting.

## q04 (dev | answerable=True | status=answered)
- **Question:** Beyond performing accurately under expected uses, what must a robust AI system do when operating in an unexpected setting?
- **Expected answer:** It should perform in ways that minimize potential harms to people if operating in an unexpected setting.
- **Gold:** `[{"source_id": "nist-ai-100-1", "page": 19, "evidence": "Robustness requires not only that the system perform exactly as it does under expected uses, but also that it should perform in ways that minimize potential harms to people if it is operating in an unexpected setting."}]`
- **Search calls:** 1 | **Elapsed:** 5707.87 ms
- **Agent answer:** A robust AI system must not only perform accurately under expected uses but also maintain its level of performance under a variety of circumstances, including unexpected settings. Specifically, it should perform in ways that minimize potential harms to people if operating in an unexpected setting, ensuring appropriate functionality beyond anticipated uses. This aligns with the definition of robustness as the ability to maintain performance under diverse conditions and circumstances, including unanticipated uses of AI systems [nist-ai-100-1:p019:para:001].
- **Citations:** ['nist-ai-100-1:p019:para:001']
  - Cited `[nist-ai-100-1:p019:para:001]` (nist-ai-100-1 p.19): Robustness or generalizability is defined as the “ability of a system to maintain its level of performance under a variety of circumstances” (Source: ISO /IEC TS 5723:2022). Robustness is a goal for appropriate system functionality in a broad set of conditions and circumstances, including uses of AI systems not initially anticipated. Robustness requires not only that the system perform exactly as it does under expected uses, but also that it should perform in ways that minimize potential harms to people if it is operating in an unexpected setting.

## q05 (dev | answerable=True | status=answered)
- **Question:** What distinct question does each of transparency, explainability, and interpretability answer for an AI system?
- **Expected answer:** Transparency answers 'what happened' in the system, explainability answers 'how' a decision was made, and interpretability answers 'why' a decision was made and its meaning or context to the user.
- **Gold:** `[{"source_id": "nist-ai-100-1", "page": 22, "evidence": "Transparency can answer the question of “what happened” in the system. Explainability can answer the question of “how” a decision was made in the system. Interpretability can answer the question of “why” a decision was made by the system and its meaning or context to the user."}]`
- **Search calls:** 1 | **Elapsed:** 6488.5 ms
- **Agent answer:** Transparency, explainability, and interpretability each answer distinct questions for an AI system: Transparency answers "what happened" in the system; explainability answers "how" a decision was made in the system; and interpretability answers "why" a decision was made by the system and its meaning or context to the user. Explainability refers to the representation of the mechanisms underlying AI systems' operation, while interpretability refers to the meaning of AI systems' output in the context of their designed functional purposes. Together, they help users and operators gain deeper insights into the system's functionality and trustworthiness [nist-ai-100-1:p022:para:000] [nist-ai-100-1:p021:para:003].
- **Citations:** ['nist-ai-100-1:p022:para:000', 'nist-ai-100-1:p021:para:003']
  - Cited `[nist-ai-100-1:p022:para:000]` (nist-ai-100-1 p.22): Risks to interpretability often can be addressed by communicating a description of why an AI system made a particular prediction or recommendation. (See “Four Principles of Explainable Artificial Intelligence” and “Psychological Foundations of Explainability and Interpretability in Artificial Intelligence” found here.) Transparency, explainability, and interpretability are distinct characteristics that support each other. Transparency can answer the question of “what happened” in the system. Explainability can answer the question of “how” a decision was made in the system. Interpretability can answer the question of “why” a decision was made by the system and its meaning or context to the user.
  - Cited `[nist-ai-100-1:p021:para:003]` (nist-ai-100-1 p.21): 3.5 Explainable and Interpretable Explainability refers to a representation of the mechanisms underlying AI systems’ operation, whereas interpretability refers to the meaning of AI systems’ output in the context of their designed functional purposes. Together, explainability and interpretability assist those operating or overseeing an AI system, as well as users of an AI system, to gain deeper insights into the functionality and trustworthiness of the system, including its outputs. The underlying assumption is that perceptions of negative risk stem from a lack of ability to make sense of, or contextualize, system output appropriately. Explainable and interpretable AI systems offer information that will help end users understand the purposes and potential impact of an AI system.

## q06 (dev | answerable=True | status=answered)
- **Question:** What three categories of AI bias are identified, and does their presence require prejudice or discriminatory intent?
- **Expected answer:** The three categories are systemic, computational and statistical, and human-cognitive bias; each can occur even in the absence of prejudice, partiality, or discriminatory intent.
- **Gold:** `[{"source_id": "nist-ai-100-1", "page": 23, "evidence": "NIST has identified three major categories of AI bias to be considered and managed: systemic, computational and statistical, and human-cognitive. Each of these can occur in the absence of prejudice, partiality, or discriminatory intent."}]`
- **Search calls:** 1 | **Elapsed:** 18297.41 ms
- **Agent answer:** The three categories of AI bias identified by NIST are systemic bias, computational and statistical bias, and human-cognitive bias. Systemic bias can be present in AI datasets, organizational norms, practices, processes, and broader society. Computational and statistical biases arise from systematic errors such as non-representative samples in datasets and algorithmic processes. Human-cognitive biases relate to how individuals or groups perceive AI system information and make decisions or fill in missing information. Importantly, each of these biases can occur without any prejudice, partiality, or discriminatory intent being present.[nist-ai-100-1:p023:para:000]
- **Citations:** ['nist-ai-100-1:p023:para:000']
  - Cited `[nist-ai-100-1:p023:para:000]` (nist-ai-100-1 p.23): Bias is broader than demographic balance and data representativeness. NIST has identified three major categories of AI bias to be considered and managed: systemic, computational and statistical, and human-cognitive. Each of these can occur in the absence of prejudice, partiality, or discriminatory intent. Systemic bias can be present in AI datasets, the organizational norms, practices, and processes across the AI lifecycle, and the broader society that uses AI systems. Computational and statistical biases can be present in AI datasets and algorithmic processes, and often stem from systematic errors due to non-representative samples. Human-cognitive biases relate to how an individual or group perceives AI system information to make a decision or fill in missing information, or how humans think about purposes and functions of an AI system.

## q07 (dev | answerable=True | status=answered)
- **Question:** When certain AI risks or trustworthiness characteristics cannot or will not be measured, what must be done with them?
- **Expected answer:** Risks or trustworthiness characteristics that will not or cannot be measured must be properly documented (along with explanations as to why some risks cannot be measured).
- **Gold:** `[{"source_id": "nist-ai-100-1", "page": 34, "evidence": "The risks or trustworthiness characteristics that will not – or cannot – be measured are properly documented."}, {"source_id": "nist-ai-600-1", "page": 33, "evidence": "MS-1.1-009 Track and document risks or opportunities related to all GAI risks that cannot be measured quantitatively, including explanations as to why some risks cannot be measured (e.g., due to technological limitations, resource constraints, or trustworthy considerations)."}]`
- **Search calls:** 1 | **Elapsed:** 6129.7 ms
- **Agent answer:** When certain AI risks or trustworthiness characteristics cannot or will not be measured, they must be properly documented, including explanations as to why some risks cannot be measured (e.g., due to technological limitations, resource constraints, or trustworthy considerations). These unmeasured risks should be tracked and documented as marginal risks. [nist-ai-600-1:p032:para:001] [nist-ai-600-1:p033:para:001]
- **Citations:** ['nist-ai-600-1:p032:para:001', 'nist-ai-600-1:p033:para:001']
  - Cited `[nist-ai-600-1:p032:para:001]` (nist-ai-600-1 p.32): MEASURE 1.1: Approaches and metrics for measurement of AI risks enumerated during the MAP function are selected for implementation starting with the most significant AI risks. The risks or trustworthiness characteristics that will not – or cannot – be measured are properly documented.

Action ID Suggested Action GAI Risks

MS-1.1-001 Employ methods to trace the origin and modifications of digital content. Information Integrity

MS-1.1-002 Integrate tools designed to analyze content provenance and detect data anomalies, verify the authenticity of digital signatures, and identify patterns associated with misinformation or manipulation.

Information Integrity

MS-1.1-003 Disaggregate evaluation metrics by demographic factors to identify any discrepancies in how content provenance mechanisms work across diverse populations.

Information Integrity; Harmful Bias and Homogenization
  - Cited `[nist-ai-600-1:p033:para:001]` (nist-ai-600-1 p.33): MS-1.1-009 Track and document risks or opportunities related to all GAI risks that cannot be measured quantitatively, including explanations as to why some risks cannot be measured (e.g., due to technological limitations, resource constraints, or trustworthy considerations). Include unmeasured risks in marginal risks.

Information Integrity

AI Actor Tasks: AI Development, Domain Experts, TEVV

MEASURE 1.3: Internal experts who did not serve as front-line developers for the system and/or independent assessors are involved in regular assessments and updates. Domain experts, users, AI Actors external to the team that developed or deployed the AI system, and affected communities are consulted in support of assessments as necessary per organizational risk tolerance.

Action ID Suggested Action GAI Risks

## q08 (dev | answerable=True | status=answered)
- **Question:** Even though pre-trained models and transfer learning can boost accuracy, what risks do they introduce compared to traditional software?
- **Expected answer:** They can increase statistical uncertainty and create challenges with bias management, scientific validity, reproducibility, and predicting failure modes of emergent properties.
- **Gold:** `[{"source_id": "nist-ai-100-1", "page": 43, "evidence": "Use of pre-trained models that can advance research and improve performance can also increase levels of statistical uncertainty and cause issues with bias management, scientific validity, and reproducibility."}]`
- **Search calls:** 1 | **Elapsed:** 6127.2 ms
- **Agent answer:** Pre-trained models and transfer learning introduce several risks compared to traditional software, including increased statistical uncertainty, challenges in bias management, scientific validity, and reproducibility. They also present a higher difficulty in predicting failure modes due to emergent properties of large-scale models. Privacy risks arise from enhanced data aggregation capabilities. AI systems using these models may require more frequent maintenance due to data, model, or concept drift. There is increased opacity and concerns about reproducibility, underdeveloped software testing standards, and difficulties in performing regular AI-based software testing. Additionally, the data used may not represent the intended context accurately, and harmful biases or data quality issues can affect trustworthiness. Changes during training can fundamentally alter performance, and datasets may become outdated or detached from their original context. The scale and complexity of AI systems, often containing billions or trillions of decision points, add to these risks compared to traditional software [nist-ai-100-1:p043:para:002][nist-ai-100-1:p043:para:001].
- **Citations:** ['nist-ai-100-1:p043:para:002', 'nist-ai-100-1:p043:para:001']
  - Cited `[nist-ai-100-1:p043:para:002]` (nist-ai-100-1 p.43): • Use of pre-trained models that can advance research and improve performance can also increase levels of statistical uncertainty and cause issues with bias management, scientific validity, and reproducibility.

• Higher degree of difficulty in predicting failure modes for emergent properties of large-scale pre-trained models.

• Privacy risk due to enhanced data aggregation capability for AI systems.

• AI systems may require more frequent maintenance and triggers for conducting corrective maintenance due to data, model, or concept drift.

• Increased opacity and concerns about reproducibility.

• Underdeveloped software testing standards and inability to document AI-based practices to the standard expected of traditionally engineered software for all but the simplest of cases.

• Difficulty in performing regular AI-based software testing, or determining what to test, since AI systems are not subject to the same controls as traditional code development.
  - Cited `[nist-ai-100-1:p043:para:001]` (nist-ai-100-1 p.43): • The data used for building an AI system may not be a true or appropriate representation of the context or intended use of the AI system, and the ground truth may either not exist or not be available. Additionally, harmful bias and other data quality issues can affect AI system trustworthiness, which could lead to negative impacts.

• AI system dependency and reliance on data for training tasks, combined with increased volume and complexity typically associated with such data.

• Intentional or unintentional changes during training may fundamentally alter AI system performance.

• Datasets used to train AI systems may become detached from their original and intended context or may become stale or outdated relative to deployment context.

• AI system scale and complexity (many systems contain billions or even trillions of decision points) housed within more traditional software applications.

## q09 (dev | answerable=True | status=answered)
- **Question:** What is confabulation in generative AI, and why does it occur naturally in models like LLMs?
- **Expected answer:** Confabulation is when GAI systems confidently generate erroneous or false content (or outputs diverging from prompts/context); it arises naturally because models approximate statistical training distributions (e.g., LLMs predicting the next token).
- **Gold:** `[{"source_id": "nist-ai-600-1", "page": 10, "evidence": "Confabulations are a natural result of the way generative models are designed: they generate outputs that approximate the statistical distribution of their training data; for example, LLMs predict the next token or word in a sentence or phrase."}]`
- **Search calls:** 1 | **Elapsed:** 17509.06 ms
- **Agent answer:** Confabulation in generative AI refers to the phenomenon where generative AI systems produce and confidently present erroneous or false content in response to prompts. This includes outputs that diverge from the prompts or contradict previously generated statements. It is also known as hallucinations or fabrications. Confabulation occurs naturally in models like large language models (LLMs) because these models generate outputs by approximating the statistical distribution of their training data, predicting the next token or word in a sequence. While this statistical prediction can yield accurate outputs, it can also produce factually inaccurate or inconsistent results. This is especially relevant for open-ended prompts requiring long-form responses or domain expertise. The confident nature of these responses can lead users to believe and act on false information, posing risks in critical applications such as healthcare [nist-ai-600-1:p010:para:000][nist-ai-600-1:p010:para:001].
- **Citations:** ['nist-ai-600-1:p010:para:000', 'nist-ai-600-1:p010:para:001']
  - Cited `[nist-ai-600-1:p010:para:000]` (nist-ai-600-1 p.10): 2.2. Confabulation

“Confabulation” refers to a phenomenon in which GAI systems generate and confidently present erroneous or false content in response to prompts. Confabulations also include generated outputs that diverge from the prompts or other input or that contradict previously generated statements in the same context. These phenomena are colloquially also referred to as “hallucinations” or “fabrications.” Confabulations can occur across GAI outputs and contexts.9,10 Confabulations are a natural result of the way generative models are designed: they generate outputs that approximate the statistical distribution of their training data; for example, LLMs predict the next token or word in a sentence or phrase. While such statistical prediction can produce factually accurate and consistent outputs, it can also produce outputs that are factually inaccurate or internally inconsistent.
  - Cited `[nist-ai-600-1:p010:para:001]` (nist-ai-600-1 p.10): This dynamic is particularly relevant when it comes to open-ended prompts for long-form responses and in domains which require highly contextual and/or domain expertise.

Risks from confabulations may arise when users believe false content – often due to the confident nature of the response – leading users to act upon or promote the false information. This poses a challenge for many real-world applications, such as in healthcare, where a confabulated summary of patient information reports could cause doctors to make incorrect diagnoses and/or recommend the wrong treatments. Risks of confabulated content may be especially important to monitor when integrating GAI into applications involving consequential decision making.

## q10 (dev | answerable=True | status=answered)
- **Question:** What caveat applies when using model distillation or compression to reduce the environmental footprint of generative AI?
- **Expected answer:** While model distillation or compression can reduce environmental impacts at inference time, training and tuning those smaller models may still contribute to environmental impacts.
- **Gold:** `[{"source_id": "nist-ai-600-1", "page": 12, "evidence": "Methods for creating smaller versions of trained models, such as model distillation or compression, could reduce environmental impacts at inference time, but training and tuning such models may still contribute to their environmental impacts."}]`
- **Search calls:** 1 | **Elapsed:** 10118.15 ms
- **Agent answer:** The caveat when using model distillation or compression to reduce the environmental footprint of generative AI is that while these methods can reduce environmental impacts at inference time, the training and tuning of such smaller models may still contribute significantly to their overall environmental impacts. Additionally, there is currently no agreed-upon method to estimate the environmental impacts from generative AI comprehensively.[nist-ai-600-1:p012:para:001]
- **Citations:** ['nist-ai-600-1:p012:para:001']
  - Cited `[nist-ai-600-1:p012:para:001]` (nist-ai-600-1 p.12): Current estimates suggest that training a single transformer LLM can emit as much carbon as 300 round-trip flights between San Francisco and New York. In a study comparing energy consumption and carbon emissions for LLM inference, generative tasks (e.g., text summarization) were found to be more energy-and carbon-i ntensive th an discriminative or non-generative tasks (e.g., text classification). Methods for creating smaller versions of trained models, such as model distillation or compression, could reduce environmental impacts at inference time, but training and tuning such models may still contribute to their environmental impacts. Currently there is no agreed upon method to estimate environmental impacts from GAI.

Trustworthy AI Characteristics: Accountable and Transparent, Safe

2.6. Harmful Bias and Homogenization

## q11 (dev | answerable=True | status=answered)
- **Question:** Do all suggested generative AI risk-management actions apply equally to every AI actor, and how should organizations determine applicability?
- **Expected answer:** No; not every suggested action applies to every AI actor or task (for example, developer actions may not apply to deployers). Applicability must be determined from organizational considerations and unique uses of GAI systems.
- **Gold:** `[{"source_id": "nist-ai-600-1", "page": 17, "evidence": "Not every suggested action applies to every AI Actor14 or is relevant to every AI Actor Task. For example, suggested actions relevant to GAI developers may not be relevant to GAI deployers. The applicability of suggested actions to relevant AI actors should be determined based on organizational considerations and their unique uses of GAI systems."}]`
- **Search calls:** 1 | **Elapsed:** 13864.07 ms
- **Agent answer:** Not every suggested generative AI risk-management action applies equally to every AI actor. For example, actions relevant to generative AI (GAI) developers may not be relevant to GAI deployers. The applicability of suggested actions to relevant AI actors should be determined based on organizational considerations and their unique uses of GAI systems. This means organizations need to assess their specific context, roles, and tasks related to GAI to decide which actions are relevant and necessary for effective risk management.[nist-ai-600-1:p017:para:000][nist-ai-600-1:p051:para:003]
- **Citations:** ['nist-ai-600-1:p017:para:000', 'nist-ai-600-1:p051:para:003']
  - Cited `[nist-ai-600-1:p017:para:000]` (nist-ai-600-1 p.17): • Not every suggested action applies to every AI Actor14 or is relevant to every AI Actor Task. For example, suggested actions relevant to GAI developers may not be relevant to GAI deployers. The applicability of suggested actions to relevant AI actors should be determined based on organizational considerations and their unique uses of GAI systems.

Each table of suggested actions includes:

• Action ID: Each Action ID corresponds to the relevant AI RMF function and subcategory (e.g., GV- 1.1-001 corresponds to the first suggested action for Govern 1.1, GV-1.1-002 corresponds to the second suggested action for Govern 1.1). AI RMF functions are tagged as follows: GV = Govern; MP = Map; MS = Measure; MG = Manage.

• Suggested Action: Steps an organization or AI actor can take to manage GAI risks.

• GAI Risks: Tags linking suggested actions with relevant GAI risks.
  - Cited `[nist-ai-600-1:p051:para:003]` (nist-ai-600-1 p.51): A.1.2. Organizational Governance GAI opportunities, risks and long-term performance characteristics are typically less well-understood than non-generative AI tools and may be perceived and acted upon by humans in ways that vary greatly. Accordingly, GAI may call for different levels of oversight from AI Actors or different human-AI configurations in order to manage their risks effectively. Organizations’ use of GAI systems may also warrant additional human review, tracking and documentation, and greater management oversight. AI technology can produce varied outputs in multiple modalities and present many classes of user interfaces. This leads to a broader set of AI Actors interacting with GAI systems for widely differing applications and contexts of use. These can include data labeling and preparation, development of GAI models, content moderation, code generation and review, text generation and editing, image and video generation, summarization, search, and chat.

## q12 (dev | answerable=True | status=answered)
- **Question:** Under GOVERN 1.7, what factors should organizations consider when decommissioning a generative AI system?
- **Expected answer:** Organizations should consider data retention requirements, post-decommissioning data security and leakage containment, dependencies across upstream/downstream/IoT/AI systems, open-source data or models, and users' emotional entanglement.
- **Gold:** `[{"source_id": "nist-ai-600-1", "page": 21, "evidence": "GV-1.7-002 Consider the following factors when decommissioning GAI systems: Data retention requirements; Data security, e.g., containment, protocols, Data leakage after decommissioning; Dependencies between upstream, downstream, or other data, internet of things (IOT) or AI systems; Use of open-source data or models; Users’ emotional entanglement with GAI functions."}]`
- **Search calls:** 4 | **Elapsed:** 18169.72 ms
- **Agent answer:** Under GOVERN 1.7, organizations should have processes and procedures in place for decommissioning and phasing out AI systems safely and in a manner that does not increase risks or decrease the organization’s trustworthiness. This implies considering safety and risk management factors to ensure that the decommissioning does not introduce new risks or harm the organization's trustworthiness. [nist-ai-100-1:p028:para:000]
- **Citations:** ['nist-ai-100-1:p028:para:000']
  - Cited `[nist-ai-100-1:p028:para:000]` (nist-ai-100-1 p.28): Table 1: Categories and subcategories for the GOVERN function. (Continued)

GOVERN 1.5: Ongoing monitoring and periodic review of the risk management process and its outcomes are planned and organizational roles and responsibilities clearly defined, including determining the frequency of periodic review.

GOVERN 1.6: Mechanisms are in place to inventory AI systems and are resourced according to organizational risk priorities.

GOVERN 1.7: Processes and procedures are in place for decommissioning and phasing out AI systems safely and in a manner that does not increase risks or decrease the organization’s trustworthiness.

GOVERN 2: Accountability structures are in place so that the appropriate teams and individuals are empowered, responsible, and trained for mapping, measuring, and managing AI risks.

## q13 (dev | answerable=True | status=answered)
- **Question:** When evaluating safety under MEASURE 2.6, what failure behavior is required if a generative AI system operates past its knowledge limits?
- **Expected answer:** The system must be demonstrated to be safe, keep residual negative risk within tolerance, and fail safely, particularly if made to operate beyond its knowledge limits.
- **Gold:** `[{"source_id": "nist-ai-600-1", "page": 36, "evidence": "The AI system to be deployed is demonstrated to be safe, its residual negative risk does not exceed the risk tolerance, and it can fail safely, particularly if made to operate beyond its knowledge limits."}]`
- **Search calls:** 1 | **Elapsed:** 2558.55 ms
- **Agent answer:** Under MEASURE 2.6, if a generative AI system operates past its knowledge limits, it is required to fail safely. This means the AI system must be demonstrated to be safe, with residual negative risk not exceeding the risk tolerance, and it must be able to fail safely particularly when operating beyond its knowledge limits. Safety metrics should reflect system reliability and robustness, real-time monitoring, and response times for AI system failures.[nist-ai-100-1:p035:para:000][nist-ai-600-1:p036:para:000]
- **Citations:** ['nist-ai-100-1:p035:para:000', 'nist-ai-600-1:p036:para:000']
  - Cited `[nist-ai-100-1:p035:para:000]` (nist-ai-100-1 p.35): Table 3: Categories and subcategories for the MEASURE function. (Continued)

MEASURE 2.6: The AI system is evaluated regularly for safety risks – as identified in theMAP function. The AI system to be deployed is demonstrated to be safe, its residual negative risk does not exceed the risk tolerance, and it can fail safely, particularly if made to operate beyond its knowledge limits. Safety metrics reflect system reliability and robustness, real-time monitoring, and response times for AI system failures.

MEASURE 2.7: AI system security and resilience – as identified in the MAP function – are evaluated and documented.

MEASURE 2.8: Risks associated with transparency and accountability – as identified in the MAP function – are examined and documented.

MEASURE 2.9: The AI model is explained, validated, and documented, and AI system output is interpreted within its context – as identified in the MAP function – to inform responsible use and governance.
  - Cited `[nist-ai-600-1:p036:para:000]` (nist-ai-600-1 p.36): MEASURE 2.6: The AI system is evaluated regularly for safety risks – as identified in the MAP function. The AI system to be deployed is demonstrated to be safe, its residual negative risk does not exceed the risk tolerance, and it can fail safely, particularly if made to operate beyond its knowledge limits. Safety metrics reflect system reliability and robustness, real-time monitoring, and response times for AI system failures.

Action ID Suggested Action GAI Risks

MS-2.6-001 Assess adverse impacts, including health and wellbeing impacts for value chain or other AI Actors that are exposed to sexually explicit, offensive, or violent information during GAI training and maintenance.

Human-AI Configuration; Obscene, Degrading, and/or Abusive Content; Value Chain and Component Integration; Dangerous, Violent, or Hateful Content

## q14 (dev | answerable=True | status=answered)
- **Question:** Why are anecdotal tests like video games or human professional licensing exams insufficient to establish generative AI validity and reliability before deployment?
- **Expected answer:** Such anecdotal testing does not guarantee GAI system validity or reliability in those domains, and laboratory benchmarks often fail to extrapolate to real-world contexts due to prompt sensitivity and context heterogeneity.
- **Gold:** `[{"source_id": "nist-ai-600-1", "page": 53, "evidence": "For example, the anecdotal testing of GAI system capabilities through video games or standardized tests designed for humans (e.g., intelligence tests, professional licensing exams) does not guarantee GAI system validity or reliability in those domains."}]`
- **Search calls:** 1 | **Elapsed:** 17474.41 ms
- **Agent answer:** Anecdotal tests like video games or human professional licensing exams are insufficient to establish generative AI validity and reliability before deployment because validity requires confirmation through objective evidence that the AI meets specific intended use requirements, and reliability demands the AI perform correctly without failure under expected conditions over time. Anecdotal tests do not provide the rigorous, documented, and representative evaluations needed to ensure trustworthy AI system performance in deployment settings. Proper validation involves systematic assessments, documentation of test sets and metrics, and evaluations representative of the relevant population and conditions, which anecdotal tests typically lack [nist-ai-100-1:p018:para:003] [nist-ai-100-1:p034:para:001].
- **Citations:** ['nist-ai-100-1:p018:para:003', 'nist-ai-100-1:p034:para:001']
  - Cited `[nist-ai-100-1:p018:para:003]` (nist-ai-100-1 p.18): 3.1 Valid and Reliable Validation is the “confirmation, through the provision of objective evidence, that the requirements for a specific intended use or application have been fulfilled” (Source: ISO 9000:2015). Deployment of AI systems which are inaccurate, unreliable, or poorly generalized to data and settings beyond their training creates and increases negative AI risks and reduces trustworthiness.

Reliability is defined in the same standard as the “ability of an item to perform as required, without failure, for a given time interval, under given conditions” (Source: ISO /IEC TS 5723:2022). Reliability is a goal for overall correctness of AI system operation under the conditions of expected use and over a given period of time, including the entire lifetime of the system.
  - Cited `[nist-ai-100-1:p034:para:001]` (nist-ai-100-1 p.34): MEASURE 1.3: Internal experts who did not serve as front-line developers for the system and/or independent assessors are involved in regular assessments and updates. Domain experts, users, AI actors external to the team that developed or deployed the AI system, and affected communities are consulted in support of assessments as necessary per organizational risk tolerance.

MEASURE 2: AI systems are evaluated for trustworthy characteristics.

MEASURE 2.1: Test sets, metrics, and details about the tools used during TEVV are documented.

MEASURE 2.2: Evaluations involving human subjects meet applicable requirements (including human subject protection) and are representative of the relevant population.

MEASURE 2.3: AI system performance or assurance criteria are measured qualitatively or quantitatively and demonstrated for conditions similar to deployment setting(s). Measures are documented.

## q15 (dev | answerable=True | status=answered)
- **Question:** Under GOVERN 1.2, what transparency and safety evaluation policies should organizations establish for generative AI?
- **Expected answer:** Organizations should establish transparency policies documenting training and generated data origin/history (balancing proprietary training details) and policies for pre-deployment and ongoing internal/external safety evaluations.
- **Gold:** `[{"source_id": "nist-ai-600-1", "page": 18, "evidence": "GV-1.2-001 Establish transparency policies and processes for documenting the origin and history of training data and generated data for GAI applications to advance digital content transparency, while balancing the proprietary nature of training approaches."}]`
- **Search calls:** 1 | **Elapsed:** 14173.91 ms
- **Agent answer:** Under GOVERN 1.2, organizations should establish transparency policies and processes for documenting the origin and history of training data and generated data for generative AI (GAI) applications to advance digital content transparency, while balancing the proprietary nature of training approaches. Additionally, organizations should establish policies to evaluate risk-relevant capabilities of GAI and robustness of safety measures, both prior to deployment and on an ongoing basis, through internal and external evaluations.[nist-ai-600-1:p018:para:000]
- **Citations:** ['nist-ai-600-1:p018:para:000']
  - Cited `[nist-ai-600-1:p018:para:000]` (nist-ai-600-1 p.18): GOVERN 1.2: The characteristics of trustworthy AI are integrated into organizational policies, processes, procedures, and practices.

Action ID Suggested Action GAI Risks

GV-1.2-001 Establish transparency policies and processes for documenting the origin and history of training data and generated data for GAI applications to advance digital content transparency, while balancing the proprietary nature of training approaches.

Data Privacy; Information Integrity; Intellectual Property

GV-1.2-002 Establish policies to evaluate risk-relevant capabilities of GAI and robustness of safety measures, both prior to deployment and on an ongoing basis, through internal and external evaluations.

CBRN Information or Capabilities; Information Security

AI Actor Tasks: Governance and Oversight

GOVERN 1.3: Processes, procedures, and practices are in place to determine the needed level of risk management activities based on the organization’s risk tolerance.

Action ID Suggested Action GAI Risks

## q16 (dev | answerable=True | status=answered)
- **Question:** In the 2023 AI RMF GOVERN section, how are governance roles divided across governing authorities, senior leadership, and management?
- **Expected answer:** Governing authorities set overarching policies for mission, goals, values, culture, and risk tolerance; senior leadership sets the organizational tone and culture for risk management; management aligns technical risk management with policies and operations.
- **Gold:** `[{"source_id": "nist-ai-100-1", "page": 27, "evidence": "Governing authorities can determine the overarching policies that direct an organization’s mission, goals, values, culture, and risk tolerance. Senior leadership sets the tone for risk management within an organization, and with it, organizational culture. Management aligns the technical aspects of AI risk management to policies and operations."}]`
- **Search calls:** 1 | **Elapsed:** 18061.74 ms
- **Agent answer:** In the 2023 AI RMF GOVERN section, governance roles are divided as follows: Governing authorities determine the overarching policies that direct an organization’s mission, goals, values, culture, and risk tolerance. Senior leadership sets the tone for risk management within the organization and influences organizational culture. Management aligns the technical aspects of AI risk management to policies and operations. This division supports strong governance that drives internal practices and norms to facilitate organizational risk culture, with documentation enhancing transparency, human review, and accountability in AI system teams [nist-ai-100-1:p027:para:000].
- **Citations:** ['nist-ai-100-1:p027:para:000']
  - Cited `[nist-ai-100-1:p027:para:000]` (nist-ai-100-1 p.27): GOVERN is a cross-cutting function that is infused throughout AI risk management and enables the other functions of the process. Aspects of GOVERN , especially those related to compliance or evaluation, should be integrated into each of the other functions. Attention to governance is a continual and intrinsic requirement for effective AI risk management over an AI system’s lifespan and the organization’s hierarchy.

Strong governance can drive and enhance internal practices and norms to facilitate organizational risk culture. Governing authorities can determine the overarching policies that direct an organization’s mission, goals, values, culture, and risk tolerance. Senior leadership sets the tone for risk management within an organization, and with it, organizational culture. Management aligns the technical aspects of AI risk management to policies and operations. Documentation can enhance transparency, improve human review processes, and bolster accountability in AI system teams.

## q17 (dev | answerable=True | status=answered)
- **Question:** What warning mechanisms and risk reassessment steps are recommended when adapting a generative AI model to a new domain?
- **Expected answer:** Organizations should re-evaluate risks when adapting GAI models to new domains and establish warning systems to detect usage in a new domain where prior context, security, or safety assumptions may no longer hold.
- **Gold:** `[{"source_id": "nist-ai-600-1", "page": 30, "evidence": "MP-4.1-008 Re-evaluate risks when adapting GAI models to new domains. Additionally, establish warning systems to determine if a GAI system is being used in a new domain where previous assumptions (relating to context of use or mapped risks such as security, and safety) may no longer hold."}]`
- **Search calls:** 1 | **Elapsed:** 6641.78 ms
- **Agent answer:** When adapting a generative AI (GAI) model to a new domain, it is recommended to re-evaluate the risks associated with the adaptation. Additionally, warning systems should be established to detect if the GAI system is being used in a new domain where previous assumptions about the context of use or mapped risks (such as security and safety) may no longer hold. This helps ensure that any changes in risk profiles are identified and managed appropriately. These recommendations are captured in the action MP-4.1-008 from the NIST AI RMF GenAI Profile mapping section. Furthermore, re-evaluation is also advised for models fine-tuned or enhanced on third-party models (MP-4.1-007) to maintain risk awareness and control. [nist-ai-600-1:p030:para:002]
- **Citations:** ['nist-ai-600-1:p030:para:002']
  - Cited `[nist-ai-600-1:p030:para:002]` (nist-ai-600-1 p.30): MP-4.1-007 Re-evaluate models that were fine-tuned or enhanced on top of third-party models. Value Chain and Component Integration

MP-4.1-008 Re-evaluate risks when adapting GAI models to new domains. Additionally, establish warning systems to determine if a GAI system is being used in a new domain where previous assumptions (relating to context of use or mapped risks such as security, and safety) may no longer hold.

CBRN Information or Capabilities; Intellectual Property; Harmful Bias and Homogenization; Dangerous, Violent, or Hateful Content; Data Privacy

MP-4.1-009 Leverage approaches to detect the presence of PII or sensitive data in generated output text, image, video, or audio. Data Privacy

## u01 (dev | answerable=False | status=abstain)
- **Question:** Under NIST AI 600-1, within how many calendar days or hours must a generative AI deployer notify the U.S. Department of Health and Human Services of a HIPAA-covered AI data breach?
- **Absence reason:** NIST AI 600-1 (p. 50, MG-4.1 / MG-4.3 context) mentions HIPAA breach reporting only as an illustrative legal/regulatory compliance example without specifying any notification deadline in hours or calendar days.
- **Search calls:** 4 | **Elapsed:** 4749.62 ms
- **Agent answer:** The NIST AI 600-1 document references the requirement to report generative AI incidents in compliance with legal and regulatory requirements such as HIPAA breach reporting and OCR (2023) guidelines. However, it does not specify the exact timeframe in calendar days or hours within which a generative AI deployer must notify the U.S. Department of Health and Human Services of a HIPAA-covered AI data breach.
- **Citations:** []

## u02 (dev | answerable=False | status=abstain)
- **Question:** What minimum training compute FLOP threshold (such as 10^26 FLOPs) does Executive Order 14110 or NIST AI 600-1 establish for mandatory dual-use foundation model safety reporting?
- **Absence reason:** NIST AI 600-1 (p. 5) references Executive Order 14110 as its mandate and mentions high compute utilization (p. 12), but neither NIST AI 100-1 nor 600-1 states any FLOP count or 10^26 reporting threshold.
- **Search calls:** 4 | **Elapsed:** 31819.3 ms
- **Agent answer:** The retrieved NIST AI RMF documents and EO 14110 references do not specify a minimum training compute FLOP threshold (such as 10^26 FLOPs) for mandatory dual-use foundation model safety reporting. Therefore, there is insufficient evidence to answer this question from the provided documents.
- **Citations:** []

## u03 (dev | answerable=False | status=abstain)
- **Question:** What EU AI Act risk tier and maximum global annual turnover fine percentage apply to generative AI confabulation under the NIST AI RMF?
- **Absence reason:** NIST AI 600-1 defines confabulation (p. 10) and NIST AI 100-1 discusses risk levels, but neither document defines EU AI Act risk tiers or monetary/turnover penalties.
- **Search calls:** 4 | **Elapsed:** 16860.71 ms
- **Agent answer:** The retrieved NIST AI RMF documents describe generative AI confabulation and discuss related risks and governance actions but do not specify the EU AI Act risk tier or the maximum global annual turnover fine percentage applicable to generative AI confabulation.
- **Citations:** []
