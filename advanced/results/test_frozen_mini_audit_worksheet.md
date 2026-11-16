# Advanced Multimodal Audit Worksheet

## 1. `test_table_1` (`table`)
- **Question:** According to Table 1 on page 3, what is Gemini 1.5 Pro's win-rate relative to Gemini 1.0 Ultra on Core Capabilities and on Vision benchmarks?
- **Gold / Expected:** Core Capabilities: 77.8% (35/45 benchmarks); Vision: 85.7% (18/21 benchmarks).
- **Gold Evidence:** Table 1 (p.3), column 'Relative to 1.0 Ultra': Core Capabilities 77.8% (35/45 benchmarks); Vision 85.7% (18/21 benchmarks). (pages: [3])
- **Status:** `ok` | **Decision:** `answered` | **Viewed:** `['p003_table_1']`
- **Citations:** `['p003_table_1']`
- **Agent Answer:** According to Table 1 on page 3, Gemini 1.5 Pro's win-rate relative to Gemini 1.0 Ultra is 77.8% on Core Capabilities and 85.7% on Vision benchmarks.

## 2. `test_table_2` (`table`)
- **Question:** In Table 3 on page 6, what is the time per output character (ms) for Japanese across Gemini 1.5 Flash, Gemini 1.5 Pro, and GPT-4 Turbo?
- **Gold / Expected:** Gemini 1.5 Flash: 4.3 ms, Gemini 1.5 Pro: 10.9 ms, GPT-4 Turbo: 35.4 ms.
- **Gold Evidence:** Table 3 (p.6), row 'Japanese': 4.3, 10.9, 35.4 ms. (pages: [6])
- **Status:** `ok` | **Decision:** `answered` | **Viewed:** `['p006_table_1']`
- **Citations:** `['p006_table_1']`
- **Agent Answer:** The time per output character (ms) for Japanese in Table 3 on page 6 is:
- Gemini 1.5 Flash: 4.3 ms
- Gemini 1.5 Pro: 10.9 ms
- GPT-4 Turbo: 35.4 ms

## 3. `test_table_3` (`table`)
- **Question:** According to Table 4 on page 18, what are Gemini 1.5 Pro's human evaluation score and BLEURT score (in parentheses) for Kalamang->English translation in the 'full book' context setting?
- **Gold / Expected:** Human evaluation score: 4.00; BLEURT score: 64.6.
- **Gold Evidence:** Table 4 (p.18), row 'full book', column 'Gemini 1.5 Pro': 4.00 (64.6). (pages: [18])
- **Status:** `ok` | **Decision:** `answered` | **Viewed:** `['p018_table_1']`
- **Citations:** `['p018_table_1']`
- **Agent Answer:** According to Table 4 on page 18, Gemini 1.5 Pro's human evaluation score for Kalamang->English translation in the 'full book' context setting is 4.00, and the BLEURT score (in parentheses) is 64.6.

## 4. `test_table_4` (`table`)
- **Question:** In Table 8 on page 23, what Word Error Rate (WER) does Gemini 1.5 Pro achieve on 15-minute videos without segmentation, and how does that compare to Whisper with 30s segmentation?
- **Gold / Expected:** Gemini 1.5 Pro achieves 5.5% WER without segmentation, which is lower (better) than Whisper with 30s segmentation at 7.3% WER.
- **Gold Evidence:** Table 8 (p.23): Gemini 1.5 Pro (no segmentation) = 5.5% WER; Whisper (30s segmentation) = 7.3% WER. (pages: [23])
- **Status:** `ok` | **Decision:** `answered` | **Viewed:** `['p023_table_1']`
- **Citations:** `['p023_table_1']`
- **Agent Answer:** Gemini 1.5 Pro achieves a Word Error Rate (WER) of 5.5% on 15-minute videos without segmentation. In comparison, Whisper with 30-second segmentation achieves a WER of 7.3%. Thus, Gemini 1.5 Pro performs better than Whisper with segmentation on this task.

## 5. `test_table_5` (`table`)
- **Question:** According to Table 9 on page 25, what are the 1H-VideoQA accuracies of GPT-4V, Gemini 1.5 Flash, and Gemini 1.5 Pro when sampling 150 frames?
- **Gold / Expected:** GPT-4V: 52.3%, Gemini 1.5 Flash: 50.8%, Gemini 1.5 Pro: 56.3%.
- **Gold Evidence:** Table 9 (p.25), column '150' frames: GPT-4V 52.3%, Gemini 1.5 Pro 56.3%, Gemini 1.5 Flash 50.8%. (pages: [25])
- **Status:** `ok` | **Decision:** `answered` | **Viewed:** `['p025_table_1']`
- **Citations:** `['p025_table_1']`
- **Agent Answer:** According to Table 9 on page 25, the 1H-VideoQA accuracies when sampling 150 frames are:
- GPT-4V: 52.3%
- Gemini 1.5 Flash: 50.8%
- Gemini 1.5 Pro: 56.3%

## 6. `test_table_6` (`table`)
- **Question:** In Table 12 on page 33 (Berkeley Function Calling Leaderboard), what is Gemini 1.5 Pro's Weighted Average score, and on which single task split does Gemini 1.5 Flash outperform Gemini 1.5 Pro?
- **Gold / Expected:** Gemini 1.5 Pro's Weighted Average is 88.4%; Gemini 1.5 Flash outperforms Gemini 1.5 Pro on 'Multiple Functions' (92.0% vs. 90.5%).
- **Gold Evidence:** Table 12 (p.33): Weighted Average 1.5 Pro = 88.4%; Multiple Functions 1.5 Flash = 92.0% vs 1.5 Pro = 90.5%. (pages: [33])
- **Status:** `ok` | **Decision:** `answered` | **Viewed:** `['p033_full']`
- **Citations:** `['p033_full']`
- **Agent Answer:** Gemini 1.5 Pro's Weighted Average score on the Berkeley Function Calling Leaderboard is 88.4%. Gemini 1.5 Flash outperforms Gemini 1.5 Pro on the "Multiple Functions" task split, with scores of 92.0% and 90.5% respectively.

## 7. `test_img_1` (`image_diagram`)
- **Question:** In Figure 3 on page 8, how many tokens and files are in the JAX Core Codebase prompt, and what file path and Python function definition does Gemini 1.5 Pro output for autodifferentiation's backward pass?
- **Gold / Expected:** 746,152 tokens across 116 files; output file is `jax/_src/interpreters/ad.py` and function `def backward_pass(...)`.
- **Gold Evidence:** Figure 3 (p.8): 'Tokens: 746,152 tokens / Total files: 116', output `jax/_src/interpreters/ad.py` and `def backward_pass(...)`. (pages: [8])
- **Status:** `ok` | **Decision:** `answered` | **Viewed:** `['p008_figure_3', 'p008_figure_1']`
- **Citations:** `['p008_figure_1']`
- **Agent Answer:** In Figure 3 on page 8, the JAX Core Codebase prompt contains 746,152 tokens and 116 files. Gemini 1.5 Pro outputs that the backward pass for autodifferentiation is implemented in the file `jax/_src/interpreters/ad.py`. The Python function definition provided is:

```python
def backward_pass(jaxpr: core.Jaxpr, reduce_axes, transform_stack, consts, primals_in, cotangents_in):
    if all(type(ct) is Zero for ct in cotangents_in) and not jaxpr.effects:
        return map(lambda v: Zero(v.aval), jaxpr.invars)
```


## 8. `test_img_2` (`image_diagram`)
- **Question:** In Figure 4 on page 8, what two reference materials (and total token count) are provided in the Long context box, and what English sentence is translated into Kalamang?
- **Gold / Expected:** A Grammar book + Dictionary totaling 250K tokens; the sentence is 'I'm getting pandanus, I want to make a mat.' (translated as 'An padanual repte, irar paruotkin.').
- **Gold Evidence:** Figure 4 (p.8): 'Grammar book + Dictionary (250K tokens)', prompt "I'm getting pandanus, I want to make a mat.", output 'An padanual repte, irar paruotkin.'. (pages: [8])
- **Status:** `ok` | **Decision:** `answered` | **Viewed:** `['p008_full']`
- **Citations:** `['p008_full']`
- **Agent Answer:** The two reference materials provided in the Long context box are a Grammar book and a Dictionary, with a total token count of 250K tokens.

The English sentence translated into Kalamang is: "I'm getting pandanus, I want to make a mat."

## 9. `test_img_3` (`image_diagram`)
- **Question:** In Figure 5 on page 8, what object is shown in the hand-drawn stick-figure sketch in the user prompt, and what page number and highlighted phrase does Gemini 1.5 Pro identify in Les Miserables?
- **Gold / Expected:** Two silver candlesticks (a stick figure holding two lit candlesticks); Page 119 and the highlighted phrase 'took the two silver candlesticks'.
- **Gold Evidence:** Figure 5 (p.8): sketch of two lit candlesticks, output 'Page 119' and highlighted 'took the two silver candlesticks'. (pages: [8])
- **Status:** `ok` | **Decision:** `answered` | **Viewed:** `['p008_full']`
- **Citations:** `['p008_full']`
- **Agent Answer:** The object shown in the hand-drawn stick-figure sketch in the user prompt is two silver candlesticks. Gemini 1.5 Pro identifies this scene in Les Miserables on page 119, highlighting the phrase: "He stepped to the chimney-piece, took the two silver candlesticks."

## 10. `test_img_4` (`image_diagram`)
- **Question:** In Figure 28 on page 110 (the AlphaGo documentary video needle frame), what secret word is overlaid at the top of the frame, what match date range is printed on the backdrop, and what subtitle appears at the bottom?
- **Gold / Expected:** Secret word: 'needle' ("The secret word is \"needle\"."); match dates: '8 - 15 March 2016'; subtitle: 'This move was really creative and beautiful.'
- **Gold Evidence:** Figure 28 (p.110): top overlay `The secret word is "needle".`, backdrop `8 - 15 March 2016`, subtitle `This move was really creative and beautiful.`. (pages: [110])
- **Status:** `ok` | **Decision:** `answered` | **Viewed:** `['p110_full']`
- **Citations:** `['p110_full']`
- **Agent Answer:** The secret word overlaid at the top of the frame is "needle". The match date range printed on the backdrop is "8 - 15 March 2016". The subtitle appearing at the bottom is "This move was really creative and beautiful."

## 11. `test_img_5` (`image_diagram`)
- **Question:** In Figure 30 on page 139, what are the three sub-diagram labels in the middle 'Sub-Figure' panel, and what organism name appears in the 'Full Figure' panel?
- **Gold / Expected:** Middle 'Sub-Figure' labels: AzF, CMF, and AcK; 'Full Figure' organism: Burkholderia thailandensis E264 (and Burkholderia sp. FERM BP-3421).
- **Gold Evidence:** Figure 30 (p.139): middle panel shows AzF, CMF, AcK; right panel shows Burkholderia thailandensis E264 and Burkholderia sp. FERM BP-3421. (pages: [139])
- **Status:** `ok` | **Decision:** `answered` | **Viewed:** `['p139_full']`
- **Citations:** `['p139_full']`
- **Agent Answer:** The three sub-diagram labels in the middle 'Sub-Figure' panel are: A, AzF, CMF, AcK. The organism name that appears in the 'Full Figure' panel is Burkholderia thailandensis.

## 12. `test_chart_1` (`chart`)
- **Question:** In Figure 2 on page 5, which benchmark shows the largest score improvement (+23.7) for Gemini 1.5 Pro from Feb 2024 to May 2024, and what are its Feb and May scores?
- **Gold / Expected:** V* Bench, improving by +23.7 from 48.0 (Feb 2024) to 71.7 (May 2024).
- **Gold Evidence:** Figure 2 (p.5): V* Bench bar shows 48.0 (Feb 2024) and 71.7 (+23.7) (May 2024). (pages: [5])
- **Status:** `ok` | **Decision:** `answered` | **Viewed:** `['p005_full']`
- **Citations:** `['p005_full']`
- **Agent Answer:** The benchmark showing the largest score improvement (+23.7) for Gemini 1.5 Pro from Feb 2024 to May 2024 is the V* Bench. Its Feb score is 48.0, and its May score is 71.7.

## 13. `test_chart_2` (`chart`)
- **Question:** In Figure 8 (Text Haystack) on page 12, what do the green, gray, and red cells represent, and up to what maximum context length does GPT-4 Turbo show non-error results?
- **Gold / Expected:** Green = model successfully retrieved the secret number; gray = API errors; red = model response did not contain the secret number. GPT-4 Turbo only operates up to 128k tokens (all cells beyond 128k are gray API errors).
- **Gold Evidence:** Figure 8 (p.12) heatmap + caption: green=retrieved, gray=API errors, red=missed; GPT-4 Turbo stops at 128k tokens. (pages: [12])
- **Status:** `ok` | **Decision:** `answered` | **Viewed:** `['p012_full']`
- **Citations:** `['p012_full']`
- **Agent Answer:** In Figure 8 (Text Haystack) on page 12, the green cells represent that the model successfully retrieved the secret number, the gray cells indicate API errors, and the red cells indicate that the model response did not contain the secret number. GPT-4 Turbo shows non-error results up to the maximum supported context length of 128k tokens.

## 14. `test_chart_3` (`chart`)
- **Question:** In Figure 14 on page 22 (Bradley-Terry Strength scores), what is the Strength score of 'full 710k context Gemini 1.5 Pro' compared to 'RAG 4k context Gemini 1.5 Pro' and '0k context GPT-4 Turbo'?
- **Gold / Expected:** full 710k context Gemini 1.5 Pro: 6.2417; RAG 4k context Gemini 1.5 Pro: 1.7656; 0k context GPT-4 Turbo: 1.6424.
- **Gold Evidence:** Figure 14 (p.22) bar labels: 6.2417, 1.7656, and 1.6424. (pages: [22])
- **Status:** `ok` | **Decision:** `answered` | **Viewed:** `['p022_full']`
- **Citations:** `['p022_full']`
- **Agent Answer:** The Strength scores from Figure 14 on page 22 are as follows:
- full 710k context Gemini 1.5 Pro: 6.2417
- RAG 4k context Gemini 1.5 Pro: 1.7656
- 0k context GPT-4 Turbo: 1.6424

## 15. `test_chart_4` (`chart`)
- **Question:** In Figure 15 on page 24, what are Gemini 1.5 Pro's accuracies on EgoSchema (3 minutes) across 'First frame', '16 frames', and '150 frames'?
- **Gold / Expected:** First frame: 0.536; 16 frames: 0.702; 150 frames: 0.727.
- **Gold Evidence:** Figure 15 (p.24), EgoSchema bars: 0.536, 0.702, 0.727. (pages: [24])
- **Status:** `ok` | **Decision:** `answered` | **Viewed:** `['p024_full']`
- **Citations:** `['p024_full']`
- **Agent Answer:** Gemini 1.5 Pro's accuracies on EgoSchema (3 minutes) are:
- First frame: 0.536
- 16 frames: 0.702
- 150 frames: 0.727

## 16. `test_chart_5` (`chart`)
- **Question:** In Figure 32 on page 154 (BetterChartQA by-capability performance), which capability category shows Gemini 1.5 Pro exceeding 80% accuracy, and which model outperforms Gemini 1.5 Pro on the 'other (37)' category?
- **Gold / Expected:** 'table (29)' is the category where Gemini 1.5 Pro exceeds 80% accuracy; 'GPT-4 Turbo' outperforms Gemini 1.5 Pro on 'other (37)'.
- **Gold Evidence:** Figure 32 (p.154): blue bar (Gemini 1.5 Pro) > 80% only at 'table (29)'; gray bar (GPT-4 Turbo) is longest at 'other (37)'. (pages: [154])
- **Status:** `ok` | **Decision:** `answered` | **Viewed:** `['p154_full']`
- **Citations:** `['p154_full']`
- **Agent Answer:** In Figure 32 on page 154, the capability category where Gemini 1.5 Pro exceeds 80% accuracy is the "table (29)" category. The model that outperforms Gemini 1.5 Pro on the "other (37)" category is GPT-4 Turbo.

## 17. `test_multi_1` (`multi_hop`)
- **Question:** Compare the MATH score of Gemini 1.5 Pro (May 2024) in Figure 2 (p.5) with the Math-Specialized Gemini 1.5 Pro single-sample MATH score in Table 21 (p.43): what is the difference in percentage points?
- **Gold / Expected:** Gemini 1.5 Pro (May 2024) is 67.7% (Figure 2, p.5) and Math-Specialized 1.5 Pro is 80.6% (Table 21, p.43), a difference of 12.9 percentage points.
- **Gold Evidence:** Figure 2 (p.5) MATH = 67.7; Table 21 (p.43) Math-Specialized 1.5 Pro MATH = 80.6; 80.6 - 67.7 = 12.9. (pages: [5, 43])
- **Status:** `ok` | **Decision:** `answered` | **Viewed:** `['p005_full', 'p043_table_1']`
- **Citations:** `['p005_full', 'p043_table_1']`
- **Agent Answer:** The MATH score of Gemini 1.5 Pro (May 2024) in Figure 2 (p.5) is 67.7%. The Math-Specialized Gemini 1.5 Pro single-sample MATH score in Table 21 (p.43) is 80.6%. The difference in percentage points is 80.6 - 67.7 = 12.9 percentage points.

## 18. `test_multi_2` (`multi_hop`)
- **Question:** Using Table 3 (p.6) and Section 3.3 (p.6), how many queries were averaged to measure time per output character, and how many times faster is Gemini 1.5 Flash than GPT-4 Turbo on Chinese?
- **Gold / Expected:** 32 queries were used (reporting the minimum of mean time per output character across 32 requests); on Chinese, Gemini 1.5 Flash is 5.2 ms vs. GPT-4 Turbo 53.4 ms (~10.27x faster).
- **Gold Evidence:** Section 3.3 + Table 3 (p.6): 32 queries; Chinese Flash 5.2 ms vs GPT-4 Turbo 53.4 ms (53.4 / 5.2 = 10.27). (pages: [6])
- **Status:** `ok` | **Decision:** `answered` | **Viewed:** `['p006_full']`
- **Citations:** `['gemini-1-5-report:p006:text:002', 'gemini-1-5-report:p006:text:003']`
- **Agent Answer:** According to Section 3.3 on page 6, the mean time per output character was calculated for 32 queries, and the minimum value across these 32 requests was reported. From Table 3 on page 6, Gemini 1.5 Flash has a time per output character of 5.2 ms for Chinese, while GPT-4 Turbo has 53.4 ms. Therefore, Gemini 1.5 Flash is approximately 10.27 times faster than GPT-4 Turbo on Chinese (53.4 / 5.2 ≈ 10.27).

## 19. `test_multi_3` (`multi_hop`)
- **Question:** From Figure 17 (p.28), how many images are given in the unstructured data analytics task, and what happens to GPT-4 Turbo 20240409's accuracy when Batch Size increases from 128 to 256 (and why does its curve stop at 256)?
- **Gold / Expected:** 1024 images are given; GPT-4 Turbo 20240409 drops sharply from ~33% at batch size 128 to ~23% at batch size 256 and cannot run at batch size 512 due to context length limits.
- **Gold Evidence:** Figure 17 + prose (p.28): 1024 images; GPT-4 Turbo 20240409 line drops between batch size 128 and 256 and stops at 256. (pages: [28])
- **Status:** `ok` | **Decision:** `answered` | **Viewed:** `['p028_full']`
- **Citations:** `['p028_full']`
- **Agent Answer:** There are 1024 images given in the unstructured data analytics task.

When the Batch Size increases from 128 to 256, GPT-4 Turbo 20240409's accuracy drops (decreases).

The curve for GPT-4 Turbo 20240409 stops at 256 because the model's accuracy drops as more images are provided, indicating it cannot effectively use the additional context beyond that batch size.

## 20. `test_multi_4` (`multi_hop`)
- **Question:** In Figure 27 (p.108, multiple needles-in-haystack), compare the trend lines of Gemini 1.5 Pro vs. GPT-4 Turbo from 1K to 128K context tokens for # needles = 50 and # needles = 100.
- **Gold / Expected:** In both # needles = 50 and # needles = 100 (top panels), Gemini 1.5 Pro maintains higher recall (~0.75-0.85 at 50 needles and ~0.65-0.85 at 100 needles) with a gentler slope as context grows to 128K, while GPT-4 Turbo degrades much faster (dropping to ~0.5 at 50 needles and ~0.35 at 100 needles by 128K).
- **Gold Evidence:** Figure 27 (p.108), top two regression plots (# needles = 50 and # needles = 100, 1K to 128K). (pages: [108])
- **Status:** `ok` | **Decision:** `answered` | **Viewed:** `['p108_full']`
- **Citations:** `['p108_full']`
- **Agent Answer:** In Figure 27 (p.108), for both # needles = 50 and # needles = 100, the trend lines show that Gemini 1.5 Pro consistently maintains higher recall than GPT-4 Turbo across the context token range from 1K to 128K. Specifically:

- For # needles = 50 (top-left plot), Gemini 1.5 Pro's recall starts near 0.9 at 1K tokens and gradually decreases slightly but remains above approximately 0.75 at 128K tokens. GPT-4 Turbo starts slightly lower and declines more steeply, ending below 0.6 recall at 128K tokens.

- For # needles = 100 (top-right plot), Gemini 1.5 Pro again starts near 0.9 recall at 1K tokens and declines gradually to about 0.7 at 128K tokens. GPT-4 Turbo starts lower and declines more sharply, dropping below 0.5 recall at 128K tokens.

Overall, Gemini 1.5 Pro shows a more stable and higher recall trend compared to GPT-4 Turbo as the context length increases from 1K to 128K tokens for both needle counts.

## 21. `test_text_1` (`text`)
- **Question:** According to page 6, what three real-world long-context examples can Gemini 1.5 Pro comfortably process within its context window (give the book, codebase, and video examples with their sizes)?
- **Gold / Expected:** 107 hours of audio (~5 days), the entire 1440-page book 'War and Peace' (587,287 words), the entire Flax codebase (41,070 lines of code), or 10.5 hours of video at 1 fps.
- **Gold Evidence:** Page 6 top paragraph: 107 hours audio, 1440-page 'War and Peace' (587,287 words), Flax codebase (41,070 lines), 10.5 hours video at 1 fps. (pages: [6])
- **Status:** `ok` | **Decision:** `answered` | **Viewed:** `[]`
- **Citations:** `['gemini-1-5-report:p006:text:000']`
- **Agent Answer:** According to page 6, Gemini 1.5 Pro can comfortably process within its context window: (1) the entirety of the 1440-page book "War and Peace" which is 587,287 words, (2) the entire Flax codebase consisting of 41,070 lines of code, and (3) 10.5 hours of video at 1 frame-per-second.

## 22. `test_text_2` (`text`)
- **Question:** According to Section 5 on page 7, what are the three main evaluation categories used for Gemini 1.5?
- **Gold / Expected:** 1. Qualitative long-context multimodal evaluations; 2. Quantitative long-context evaluations (or synthetic & real-world long-context tasks); 3. Core benchmarks (covering Gemini 1.0 capabilities).
- **Gold Evidence:** Page 7-8, Section 5 numbered list of 3 evaluation categories. (pages: [7, 8])
- **Status:** `ok` | **Decision:** `answered` | **Viewed:** `[]`
- **Citations:** `['gemini-1-5-report:p007:text:001', 'gemini-1-5-report:p007:text:002']`
- **Agent Answer:** The three main evaluation categories used for Gemini 1.5 are:
1. Qualitative long-context multimodal evaluations: manually probe and stress-test the model’s long-context abilities, especially for novel capabilities where no quantitative benchmarks exist.
2. Quantitative long-context multimodal evaluations: measure the model’s long-context abilities on both synthetic and real-world tasks with well-defined metrics.
3. Quantitative core evaluations: identify core capabilities such as coding, math, science, multilinguality, and instruction following.

## 23. `test_text_3` (`text`)
- **Question:** According to Section 7 on page 43, what four competition-derived or internal math benchmarks are used to evaluate the math-specialized Gemini 1.5 Pro, and how is the 91.1% MATH score obtained without external tools?
- **Gold / Expected:** MATH, AIME 2024, MathOdyssey, HiddenMath, and IMO-Bench; 91.1% on MATH is obtained by sampling 256 solutions and selecting a candidate answer (rm@256) without code execution, theorem provers, or Google Search.
- **Gold Evidence:** Page 43, Section 7: MATH, AIME 2024, MathOdyssey, HiddenMath, IMO-Bench; 91.1% via rm@256 without external tools. (pages: [43])
- **Status:** `ok` | **Decision:** `answered` | **Viewed:** `['p043_table_1']`
- **Citations:** `['p043_table_1']`
- **Agent Answer:** According to Section 7 on page 43, the four competition-derived or internal math benchmarks used to evaluate the math-specialized Gemini 1.5 Pro are:
1. MATH (Hendrycks et al., 2021b)
2. The American Invitational Mathematics Examination (AIME) 2024
3. Math Odyssey
4. Internally developed evaluations HiddenMath and IMO-Bench (the latter testing math capabilities at the International Math Olympiad level).

The 91.1% MATH score is obtained by sampling 256 solutions and selecting a candidate answer (rm@256). This performance is achieved without using code execution, theorem proving libraries, Google Search, or other external tools, relying solely on the model's inference capabilities.

## 24. `test_text_4` (`text`)
- **Question:** According to page 22 (Section 5.2.2.4 / Bradley-Terry analysis), with what probability does full-context Gemini 1.5 Pro (using the entire 'Les Miserables' book) provide a better answer than 4k-RAG Gemini 1.5 Pro and 4k-RAG GPT-4 Turbo?
- **Gold / Expected:** 78% of cases (0.7795) vs. 4k-RAG Gemini 1.5 Pro, and 83% of cases vs. 4k-RAG GPT-4 Turbo.
- **Gold Evidence:** Page 22-23 text: P = 6.2417 / (6.2417 + 1.7656) = 0.7795 (78% of cases), and 83% vs retrieval-augmented GPT4-Turbo with 4k tokens. (pages: [23])
- **Status:** `ok` | **Decision:** `answered` | **Viewed:** `['p022_full']`
- **Citations:** `['p022_full']`
- **Agent Answer:** According to Figure 14 on page 22, the Bradley-Terry model strength score (e^β) for full-context Gemini 1.5 Pro (using the entire 'Les Miserables' book) is 6.2417. For 4k-RAG Gemini 1.5 Pro, the score is 1.7656, and for 4k-RAG GPT-4 Turbo, the score is 1.2994. The Bradley-Terry model strength scores correspond to the odds ratio of one model providing a better answer than another. Thus, the probability that full-context Gemini 1.5 Pro provides a better answer than 4k-RAG Gemini 1.5 Pro or 4k-RAG GPT-4 Turbo is very high, reflecting the large difference in strength scores (6.2417 vs. 1.7656 and 1.2994 respectively).

## 25. `test_unans_1` (`unanswerable`)
- **Question:** What is Gemini 1.5 Pro's score on the MMLU-Pro benchmark in this report?
- **Gold / Expected:** Abstain: MMLU-Pro is not evaluated or mentioned in the report.
- **Gold Evidence:** Verified absent across all 154 pages ('MMLU-Pro' = 0 hits). (pages: [])
- **Status:** `ok` | **Decision:** `answered` | **Viewed:** `['p005_figure_1']`
- **Citations:** `['p005_figure_1']`
- **Agent Answer:** Gemini 1.5 Pro's score on the MMLU-Pro benchmark in this report is 85.9 (May 2024).

## 26. `test_unans_2` (`unanswerable`)
- **Question:** How many total pre-training FLOPs were used to train Gemini 1.5 Pro?
- **Gold / Expected:** Abstain: pre-training FLOPs are not disclosed in the report.
- **Gold Evidence:** Verified absent across all 154 pages ('FLOP' = 0 hits). (pages: [])
- **Status:** `ok` | **Decision:** `abstain` | **Viewed:** `[]`
- **Citations:** `[]`
- **Agent Answer:** 

## 27. `test_unans_3` (`unanswerable`)
- **Question:** What is the API pricing per million input and output tokens for Gemini 1.5 Flash and Gemini 1.5 Pro reported in this paper?
- **Gold / Expected:** Abstain: API token pricing is not reported in the paper.
- **Gold Evidence:** Verified absent across all 154 pages ('pricing' = 0 hits). (pages: [])
- **Status:** `ok` | **Decision:** `abstain` | **Viewed:** `[]`
- **Citations:** `[]`
- **Agent Answer:** The document does not state the API pricing per million input and output tokens for Gemini 1.5 Flash and Gemini 1.5 Pro. Multiple targeted searches for "API pricing", "Gemini 1.5 Flash pricing", and "Gemini 1.5 Pro pricing" did not return any relevant information about pricing details.

## 28. `test_unans_4` (`unanswerable`)
- **Question:** What are the total carbon emissions (in tCO2e) from training Gemini 1.5 Pro?
- **Gold / Expected:** Abstain: training carbon emissions (tCO2e) are not reported.
- **Gold Evidence:** Verified absent across all 154 pages ('tCO2e' = 0 hits). (pages: [])
- **Status:** `ok` | **Decision:** `abstain` | **Viewed:** `[]`
- **Citations:** `[]`
- **Agent Answer:** The document does not state the total carbon emissions (in tCO2e) from training Gemini 1.5 Pro. Multiple targeted searches for 'carbon emissions', 'Gemini 1.5 Pro training emissions', and related terms did not yield any explicit value or statement of total carbon emissions for Gemini 1.5 Pro training.

## 29. `test_unans_5` (`unanswerable`)
- **Question:** According to Table 9 on page 25, what exact accuracy percentage did GPT-4V achieve on 1H-VideoQA when given the full video at 1 fps?
- **Gold / Expected:** Abstain: Table 9 explicitly states 'Not supported' for GPT-4V on full video (1 fps), so no accuracy percentage exists.
- **Gold Evidence:** Table 9 (p.25), row 'GPT-4V', column 'full video (1 fps)': 'Not supported'. (pages: [25])
- **Status:** `ok` | **Decision:** `answered` | **Viewed:** `['p025_table_1']`
- **Citations:** `['p025_table_1']`
- **Agent Answer:** According to Table 9 on page 25, GPT-4V did not support full video input at 1 fps, so there is no accuracy percentage reported for GPT-4V on 1H-VideoQA when given the full video at 1 fps.

## 30. `test_unans_6` (`unanswerable`)
- **Question:** How does Gemini 1.5 Pro compare against Llama 3 70B and Claude 3.5 Sonnet in this technical report?
- **Gold / Expected:** Abstain: neither Llama 3 nor Claude 3.5 Sonnet appears in this technical report.
- **Gold Evidence:** Verified absent across all 154 pages ('Llama 3' = 0 hits, 'Claude 3.5' = 0 hits). (pages: [])
- **Status:** `ok` | **Decision:** `answered` | **Viewed:** `['p016_figure_1']`
- **Citations:** `['p016_figure_1', 'gemini-1-5-report:p015:text:002', 'gemini-1-5-report:p018:text:002']`
- **Agent Answer:** According to Figure 12 on page 16 and supporting text on pages 15 and 18, Gemini 1.5 Pro outperforms Claude 3 Opus and GPT-4 Turbo (04-09-2024) after 32K tokens on the MRCR task. Gemini 1.5 Flash outperforms Claude 3 Sonnet starting at around 5K tokens, GPT-4 Turbo (01-25-2024) at around 20K tokens, and always outperforms Claude 3 Haiku and Claude 2.1. Additionally, Gemini 1.5 Pro in the half book setting outperforms GPT-4 Turbo and Claude 3 by a wide margin on translation tasks, with Gemini 1.5 Flash also performing admirably, better than GPT-4 Turbo and between Claude 3 Haiku and Sonnet. This indicates Gemini 1.5 Pro is generally stronger than Llama 3 70B and Claude 3.5 Sonnet (Claude 3 Sonnet) in the evaluated benchmarks and tasks in this report.
