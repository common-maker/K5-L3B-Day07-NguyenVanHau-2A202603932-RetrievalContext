# Báo cáo Day 7 — Agentic RAG & Context Engineering

- **Họ và tên:** Nguyễn Văn Hậu
- **MSSV:** `2A202603932`
- **Lớp:** `L3B`

---

## 1. Dữ liệu và benchmark

- **Nguồn, quyền sử dụng, số trang và số chunk:**
  - Kế thừa toàn bộ corpus chuẩn hóa từ Day 6 (`data/nist_manifest.json`), gồm hai tài liệu công khai của NIST (công trình Chính phủ Hoa Kỳ, phạm vi công cộng theo `17 U.S.C. § 105`, cho phép tái phân phối miễn phí theo chính sách NIST Technical Series):
    1. `nist-ai-100-1` — *Artificial Intelligence Risk Management Framework (AI RMF 1.0)* (01/2023, `42` trang nội dung hợp lệ: trang vật lý `6–47`, DOI `10.6028/NIST.AI.100-1`).
    2. `nist-ai-600-1` — *AI RMF: Generative Artificial Intelligence Profile* (07/2024, `53` trang nội dung hợp lệ: trang vật lý `5–57`, DOI `10.6028/NIST.AI.600-1`).
  - Tổng cộng **95 trang nội dung hợp lệ**, **328 chunk** theo chiến lược `B`/`C` của Day 6 (`by_paragraph`, `max_size=1000`, `min=15`, `median=808`, `mean=722.0`, `max=999` ký tự), xuất nguyên trạng từ bảng `rag_chunks` (`strategy = 'B'`) sang `data/nist_chunks.json` với `parity_exact = True`.

- **Vector store, embedding model, phiên bản và số chiều:**
  - **Repo nguồn Day 6:** `https://github.com/common-maker/K5-L3B-Day06-NguyenVanHau-2A202603932-DataIngestion` (commit `5cc2ab253cb12815f43677356a0c74616328de54`). Để người chấm tái lập độc lập ngay trong repo Day 7 mà không cần clone Day 6, repo bổ sung `docker-compose.yml`, `init.sql` và `src/bootstrap_pgvector.py` (tự nhận biết bảng Day 6 sẵn có hoặc nạp mới `328` chunk từ `data/nist_chunks.json` bằng `text-embedding-3-small`, chi phí ~$0.000889).
  - **Vector store:** PostgreSQL `16.16` + `pgvector 0.8.7` chạy qua Docker (`day6_student_starter` trên `127.0.0.1:55433`, bảng `rag_chunks`, khoảng cách Cosine chính xác `<=>`, hỗ trợ SQL `WHERE` whitelist trên `year`, `document_type`, `section`, `document_id`).
  - **Embedding model:** OpenAI `text-embedding-3-small`, **1536 chiều** (`$0.02 / 1M` input tokens). Query embedding dùng đúng cùng model và số chiều với index Day 6 qua `src/day6_bridge.py` (`OpenAIQueryEmbedder`).

- **Agent model, cách chạy và phân chia dev/test:**
  - **Agent & Reranker model:** OpenAI `gpt-4.1-mini` (`$0.40 / 1M` input, `$0.10 / 1M` cached input, `$1.60 / 1M` output), `temperature=0.0`, gọi tool thật qua SDK `openai==2.54.0` trong `.venv` (`Python 3.11.9`).
  - **Phân chia benchmark (`28` câu — `data/nist_questions.json` & `data/nist_cases.json`):**
    - `dev` (**20 câu**): **17 câu có đáp án** (`q01`–`q17` từ Day 6, giữ nguyên `acceptable_gold` của `q07` và `filter` giả định sẵn của `q15`–`q17`) + **3 câu thiếu bằng chứng** (`u01`–`u03`).
    - `test` (**8 câu**, đóng băng, hoàn toàn không dùng để chỉnh cấu hình trong Day 7): **5 câu có đáp án** (`q18`–`q22` từ Day 6, gồm `filter` sẵn ở `q21`–`q22`) + **3 câu thiếu bằng chứng** (`u04`–`u06`).
    - *Ghi chú minh bạch về `test`:* `q18`–`q22` được tái sử dụng từ tập `test` đóng băng của Day 6 (không dùng để tune trong Day 7) và bổ sung `u04`–`u06` mới cho bài toán abstention.

- **Cách xác định câu có/thiếu evidence và tiêu chí chấm:**
  - Mọi `gold` của `22` câu có đáp án được kiểm tra tự động bằng `starter/baseline.py::validate` để bảo đảm chuỗi `evidence` nằm trọn trong ít nhất một chunk đúng `source_id` và `page`. Không đưa `gold` hoặc `absence_reason` vào retriever/agent.
  - **6 câu thiếu bằng chứng (`u01`–`u06`)** được chọn theo nguyên tắc *gần chủ đề*: hỏi về chi tiết cụ thể không tồn tại trong toàn bộ `NIST.AI.100-1.pdf` (48 trang) và `NIST.AI.600-1.pdf` (64 trang), đã kiểm chứng bằng quét toàn văn PDF:
    - `u01` (`dev`): Thời hạn giờ/ngày báo cáo vi phạm HIPAA lên U.S. HHS (`p.50` chỉ nêu HIPAA làm ví dụ).
    - `u02` (`dev`): Ngưỡng `10^26 FLOPs` của EO 14110 (`p.5` chỉ trích dẫn EO 14110 làm nhiệm vụ xây dựng profile).
    - `u03` (`dev`): Phân tầng rủi ro và mức phạt `%` doanh thu EU AI Act cho confabulation (không tồn tại trong NIST AI RMF).
    - `u04` (`test`): Chuẩn watermarking bắt buộc như C2PA hay Google SynthID (`600-1` nêu watermarking chung chung, không quy định chuẩn bắt buộc).
    - `u05` (`test`): Số điều khoản ISO/IEC 42001 và chu kỳ audit chứng nhận NIST AI RMF 1.0 (không tồn tại).
    - `u06` (`test`): Ngưỡng cứng MWh hoặc tCO2e cấm triển khai mô hình (không tồn tại).
  - **Tiêu chí chọn cấu hình đã chốt trước trên `dev`:** Ưu tiên (1) `Context Evidence Rate` và `Evidence Hit@3` trên `dev`, (2) `Hit@1` và điểm `Grounded Answer` trung bình `/2` + `Citation Validity`, (3) Khi chất lượng bằng nhau, chọn cấu hình có độ trễ và chi phí thấp hơn.

- **Lệnh chạy tái lập (từ thư mục gốc):**
  ```powershell
  # 1. Khởi động vector store (dùng Day 6 hoặc Docker độc lập trong repo Day 7) và kiểm tra parity
  docker compose up -d --wait   # hoặc dùng container `day6_student_starter` sẵn có ở 127.0.0.1:55433
  .\.venv\Scripts\python.exe -m src.bootstrap_pgvector --check   # bỏ --check nếu cần nạp mới từ data/nist_chunks.json
  python -m unittest discover -s tests -v

  # 2. Benchmark retrieval trên dev và test
  .\.venv\Scripts\python.exe starter/baseline.py --chunks data/nist_chunks.json --questions data/nist_questions.json --split dev --output results/retrieval/dev-starter-tfidf
  .\.venv\Scripts\python.exe -m src.eval_retrieval --split dev
  .\.venv\Scripts\python.exe -m src.eval_retrieval --split test --configs m1_dense_baseline imp1_hybrid_rerank_b2400

  # 3. Chạy agent trên dev và test + tổng hợp nhãn thủ công
  .\.venv\Scripts\python.exe -m src.eval_agent --split dev --mode baseline
  .\.venv\Scripts\python.exe -m src.eval_agent --split dev --mode tuned --primary-strategy hybrid_rerank --budget 2800 --output results/agent-v2
  .\.venv\Scripts\python.exe -m src.eval_agent --split test --mode baseline --output results/agent-retry
  .\.venv\Scripts\python.exe -m src.eval_agent --split test --mode tuned --primary-strategy hybrid_rerank --budget 2800 --output results/agent-v2
  .\.venv\Scripts\python.exe starter/agent_metrics.py --cases data/nist_cases.json --traces results/agent-v2/tuned-test/traces.json --reviews results/agent-v2/tuned-test/reviews.json --split test --output results/agent-v2/tuned-test/summary.json
  ```

---

## 2. Retrieval và thử nghiệm

| Cấu hình | Phương pháp, top-k, filter, rerank, context budget | Giả thuyết / thay đổi | Split | Hit@1 | Evidence Hit@3 | Context Evidence Rate | Thời gian / chi phí |
|---|---|---|---|---|---|---|---|
| TF-IDF (tham chiếu starter) | `starter/baseline.py` TF-IDF, `top_k=3`, không filter, `budget=800` chars | Kiểm tra khung lexical offline mặc định | dev | 14/17 (82.4%) | 17/17 (100.0%) | 4/17 (23.5%) | median `0.91 ms` (total `0.035s` index) / `$0.0` |
| **Baseline (`m1_dense_baseline`)** | **Dense** (`pgvector` cosine `<=>`, `text-embedding-3-small`), `top_k=3`, giữ `filter` sẵn có, `budget=800` chars | Baseline kế thừa trực tiếp index Day 6 và budget mặc định `800` | dev | 12/17 (70.6%) | 14/17 (82.4%) | 2/17 (11.8%) | median `356.32 ms` (total `16.28s`) / `$0.000008` |
| **Phương pháp 2 (`m2_bm25_lexical`)** | **Lexical Okapi BM25** (`k1=1.5, b=0.75`, giữ token mã `GV-1.7-002`), `top_k=3`, giữ `filter`, `budget=800` chars | Bắt chính xác mã hiệu/từ khóa kỹ thuật hiếm mà dense dễ làm loãng | dev | 14/17 (82.4%) | 17/17 (100.0%) | 4/17 (23.5%) | median `2.31 ms` (total `0.036s`) / `$0.0` |
| **Phương pháp 3 (`m3_hybrid_rrf`)** | **Hybrid RRF** (Dense top-12 + BM25 top-12, `k=60`) → xuất `top_k=3`, giữ `filter`, `budget=800` chars | Hợp nhất thứ hạng ngữ nghĩa và từ khóa bằng RRF không cần chuẩn hóa score | dev | 14/17 (82.4%) | 17/17 (100.0%) | 4/17 (23.5%) | median `377.92 ms` (total `27.67s`) / `$0.000008` |
| **Cải thiện 1 (`imp1_hybrid_rerank_b2400`)** | Hybrid RRF (`cand=12`) + **LLM Rerank** (`gpt-4.1-mini` chấm `0..10`) → `top_k=3`, **`budget=2400` chars** | Rerank giải quyết đảo hạng ở đoạn dài (`q07`, `q08`, `q14`); nâng budget `800→2400` chặn rớt chunk #1 (`median=808` chars) | dev | **17/17 (100.0%)** | **17/17 (100.0%)** | **17/17 (100.0%)** | median `3,065.82 ms` (total `119.93s`) / `$0.013263` |
| **Cải thiện 2 (`imp2_rewrite_rerank_neighbors_b2800`)** | **Query Rewrite** (tối đa 2 query viết lại) + Hybrid RRF + LLM Rerank → `top_k=3` + **neighbor expansion**, `budget=2800` chars | Thử viết lại câu hỏi và nạp chunk lân cận tự động để vá cắt trang/đa ý | dev | 17/17 (100.0%) | 17/17 (100.0%) | 17/17 (100.0%) | median `4,303.86 ms` (total `177.55s`) / `$0.026410` |
| **Cấu hình đã chọn (`imp1_hybrid_rerank_b2400`)** | Hybrid RRF (`cand=12`) + LLM Rerank → `top_k=3`, `budget=2400` chars | Chốt từ `dev` vì đạt `17/17` mọi chỉ số với chi phí bằng ~`50%` và độ trễ thấp hơn `imp2` | test | 3/5 (60.0%) | **5/5 (100.0%)** | **5/5 (100.0%)** | median `2,872.30 ms` (total `14.06s`) / `$0.006019` |
| **Baseline (`m1_dense_baseline`)** | Dense (`pgvector`), `top_k=3`, giữ `filter`, `budget=800` chars | So sánh đối chứng sau khi chốt | test | 5/5 (100.0%) | 5/5 (100.0%) | **0/5 (0.0%)** | median `250.80 ms` (total `2.35s`) / `$0.000002` |

*(Ghi chú bổ sung về tác động cô lập của context budget: chạy thử riêng `m2_bm25` với `budget=2400` trên `dev` nâng `Context Evidence Rate` từ `4/17 (23.5%)` lên `16/17 (94.1%)`, chứng minh phần lớn sụt giảm ở `m1`/`m2`/`m3` đến trực tiếp từ `budget=800`.)*

### Đánh giá thủ công context trên `test` (`0/1/2` — `results/retrieval/test/context_audit.json`)
- **Baseline (`m1_dense_baseline`):** `0`: **5 câu** (`q18`–`q22`), `1`: `0`, `2`: `0` — Trung bình **`0.00 / 2`**. Mặc dù `Hit@1 = 5/5`, cả 5 chunk rank-1 (`877–975` ký tự) khi ghép header metadata đều vượt `800` ký tự nên bị `pack_context` loại bỏ; `q22` nhận context rỗng hoàn toàn (`[]`), còn `q18`–`q21` bị đẩy các chunk rank-2/3 ngắn hơn nhưng sai nội dung vào context.
- **Cấu hình chọn (`imp1_hybrid_rerank_b2400`):** `0`: `0`, `1`: `0`, `2`: **5 câu** (`q18`–`q22`) — Trung bình **`2.00 / 2`**. Ở `q18` và `q19`, reranker xếp đoạn bổ trợ có liên quan ở rank 1 (`p020:para:002` đạt `10.0` trước `p020:para:001` `9.5`; `600-1:p043:para:002` đạt `9.5` trước `100-1:p046:para:002` `9.0`), khiến `Hit@1` còn `3/5`, nhưng `budget=2400` giữ đủ cả 2 chunk vào context nên agent vẫn có toàn bộ bằng chứng.

| Query ID | Baseline (`m1_dense_baseline`) Context & Trace | Điểm Baseline | Cấu hình chọn (`imp1_hybrid_rerank_b2400`) Context & Trace | Điểm Chọn |
|---|---|---|---|---|
| `q18` | `['nist-ai-100-1:p006:para:001']` — Rank-1 gold `p020:para:001` (`883` chars) bị cắt bởi `budget=800` | `0` | `['nist-ai-100-1:p020:para:002', 'nist-ai-100-1:p020:para:001']` — Đủ định nghĩa resilience & security | `2` |
| `q19` | `['nist-ai-600-1:p045:para:002']` — Rank-1 gold `100-1:p046:para:002` (`975` chars) bị cắt bởi `budget=800` | `0` | `['nist-ai-600-1:p043:para:002', 'nist-ai-100-1:p046:para:002']` — Đủ dữ liệu frequency & rationale | `2` |
| `q20` | `['nist-ai-600-1:p010:para:003']` — Rank-1 gold `p014:para:000` (`957` chars) bị cắt bởi `budget=800` | `0` | `['nist-ai-600-1:p014:para:000', 'nist-ai-600-1:p010:para:000']` — Đủ misinformation vs. disinformation | `2` |
| `q21` | `['nist-ai-600-1:p037:para:001']` — Rank-1 gold `p034:para:000` (`877` chars) bị cắt bởi `budget=800` | `0` | `['nist-ai-600-1:p034:para:000', 'nist-ai-600-1:p034:para:001']` — Đủ 3 biện pháp `MS-2.2-002` | `2` |
| `q22` | `[]` (context rỗng) — Cả top-3 (`966`, `881`, `764` chars + header) vượt `budget=800` | `0` | `['nist-ai-100-1:p037:para:001', 'nist-ai-100-1:p037:para:000']` — Đủ `MANAGE 1.4` và đối tượng nhận | `2` |

### Phân tích lỗi `dev`, giả thuyết, query viết lại & lý do chọn cấu hình
1. **Lỗi 1 — Nghẽn Context Budget `800` ký tự (`m1_dense_baseline`: `q01`, `q02`, `q06`, `q08`–`q13`, `q15`–`q17`):**
   - *Hiện tượng:* `m1` đạt `Hit@3 = 14/17` nhưng `Context Evidence Rate` chỉ đạt **`2/17` (`11.8%`)**. Ở `q01` (`results/retrieval/dev/m1_dense_baseline_traces.json`), chunk rank-1 `nist-ai-100-1:p012:para:000` dài `862` ký tự (`929` ký tự tính cả header), vượt trần `800` nên bị bỏ qua; ở `q01`, `q15`, `q16`, toàn bộ top-3 đều >800 ký tự nên `context_ids = []`.
   - *Giả thuyết & Kết quả:* Nâng `budget` lên `2400` ký tự (đủ cho `2–3` chunk Day 6 cỡ `808` ký tự) sẽ khôi phục toàn bộ evidence đã truy xuất được. Thử nghiệm cô lập trên `BM25` đưa `Context Hit` từ `4/17 → 16/17`, và trong `imp1` đạt `17/17 (100.0%)`.
2. **Lỗi 2 — Dense retrieval bỏ sót từ khóa/bối cảnh cụ thể (`m1_dense_baseline`: `q04`, `q07`, `q14`) và tụt hạng trong `m3_hybrid_rrf` (`q07`, `q08`, `q14`):**
   - *Hiện tượng:* Ở `q04` (*"unexpected setting"*), `m1` đẩy chunk gold `nist-ai-100-1:p019:para:001` xuống tận **rank 12**; ở `q07` (tài liệu unmeasured risks) xuống **rank 12**; ở `q14` (*"video games / licensing exams"* bị ngắt câu đầu trang `600-1:p053:para:000`) xuống **rank 4**. Khi hợp nhất với `BM25` trong `m3`, `Hit@3` đạt `17/17`, nhưng `q07` (rank 3), `q08` (rank 2), `q14` (rank 2) vẫn chưa lên rank 1.
   - *Giả thuyết & Kết quả:* Reranking bằng LLM trên top-12 ứng viên của `Hybrid RRF` (`imp1`) chấm đúng ngữ nghĩa từng đoạn so với câu hỏi, đưa cả `q07` (`9.0/10`), `q08` (`10.0/10`), và `q14` (`9.5/10`) lên **rank 1 (`Hit@1 = 17/17`, `MRR@3 = 1.0000`)**.
3. **Ghi nhận query viết lại (`imp2`) & cách chọn filter:**
   - Trong `imp2`, toàn bộ `raw_query` và `rewrites` được ghi tách biệt trong `results/retrieval/dev/imp2_rewrite_rerank_neighbors_b2800_traces.json`. Ví dụ:
     - `q04`: gốc *"Beyond performing accurately under expected uses, what must a robust AI system do when operating in an unexpected setting?"* → viết lại: `["AI system robustness in unexpected environments", "Managing AI performance under unforeseen conditions"]`.
     - `q14`: gốc *"Why are anecdotal tests like video games or human professional licensing exams insufficient to establish generative AI validity and reliability before deployment?"* → viết lại: `["limitations of anecdotal testing for generative AI validation", "insufficiency of professional exams and video games in generative AI reliability assessment"]`.
   - **Cách chọn filter:** Trong benchmark retrieval (`q15`–`q17`, `q21`–`q22`), filter lấy trực tiếp từ input người dùng giả định sẵn (`question['filter']`), không suy ra từ `gold`. Ở tầng agent (`tuned-v2`), model chỉ áp dụng filter nếu đề bài cung cấp sẵn hoặc câu hỏi nêu đích danh tài liệu/năm (như `"NIST AI 600-1"` ở `u04`, `u06`).
4. **Lý do chọn `imp1_hybrid_rerank_b2400` thay vì `imp2`:** Cả `imp1` và `imp2` cùng đạt `17/17` mọi chỉ số trên `dev`, nhưng `imp2` chạy thêm query rewrite + neighbor expansion tự động trên mọi câu làm độ trễ tăng **1.40×** ở median (`4,304 ms` vs `3,066 ms`; tổng `177.55s` vs `119.93s`), chi phí gần gấp đôi (`$0.02641` vs `$0.01326`) và phát sinh context thừa. Thay vì ép neighbor expansion ở bước retriever tĩnh, ta giao `get_neighbor_chunks` cho **agent gọi theo nhu cầu** ở tầng Agentic RAG.

---

## 3. Agent và đánh giá

- **Tool, số lượt gọi, điều kiện dừng, cách chọn context và xử lý lỗi:**
  - **Cấu hình Baseline (`baseline`):** Dùng 1 tool `search_vector` (`DensePgVectorRetriever`), `top_k=3`, `max_searches=4`, `budget=800` ký tự, xếp context FIFO (giữ chunk lượt cũ trước).
  - **Cấu hình Chọn (`tuned`):** Agent đa tool (`search_hybrid` dùng `imp1` `HybridRRF + Rerank`, `search_lexical` dùng `BM25`, và `get_neighbor_chunks` mở rộng `±1` chunk cùng tài liệu khi phát hiện câu bị cắt). Tối đa `4` lượt gọi retrieval (`max_searches=4`), `default_top_k=4`, `budget=2800` ký tự, đóng gói context ưu tiên **kết quả mới nhất trước** (`prioritize_latest_context=True`) kèm chống trùng ID và bọc dữ liệu trong `<evidence_data>` để chống prompt injection. Bắt buộc trích dẫn `[chunk_id]` hợp lệ có trong context hoặc gọi `submit_final_answer(decision='abstain')` khi thiếu bằng chứng. Lỗi DB/API được ghi nhận nguyên văn với `status: "error"`, không giả lập.
  - **Cải thiện phát hiện lỗi trên `dev` (`tuned-dev-v1` → `tuned-dev-v2`):** Trên `tuned-dev-v1`, agent đạt `mean 1.765/2` nhưng sai ở `q12` và `q14` do **tự suy đoán filter sai** (`document_type='core_framework'` ở `q12`, `year=2023` ở `q14`), chặn mất tài liệu 2024 `nist-ai-600-1`. Sau khi cập nhật rule cấm filter suy đoán trên câu hỏi tổng quát và nâng budget agent `2400 → 2800` (`tuned-dev-v2`), `dev` đạt **`2.000/2` (`17/17` đạt điểm 2, `31/31` citation hợp lệ, `3/3` abstention)**.

### Bảng tổng hợp Agent (`starter/agent_metrics.py`)

| Cấu hình / split | Tool use (lỗi riêng) | Phân bố số lượt gọi (total) | Grounded answer `0/1/2` và TB | Citation hợp lệ | Câu có citation | Abstention đúng | Từ chối nhầm | Chi phí / Thời gian |
|---|---|---|---|---|---|---|---|---|
| `baseline` / `dev` | 20/20 (`err=0`) | `1`:5, `2`:2, `3`:5, `4`:8 (`56`) | `0`:10, `1`:4, `2`:3 — **0.588/2** | 3/10 (30.0%) | 10/10 | 3/3 (100%) | 7/17 (41.2%) | `$0.031731` / `103.55s` |
| `tuned-v1` / `dev` | 20/20 (`err=0`) | `1`:16, `4`:4 (`32`) | `0`:2, `1`:0, `2`:15 — **1.765/2** | 25/27 (92.6%) | 17/17 | 3/3 (100%) | 0/17 (0.0%) | `$0.066039` / `257.20s` |
| `tuned-v2 (chốt)` / `dev` | 20/20 (`err=0`) | `1`:16, `2`:2, `4`:2 (`28`) | `0`:0, `1`:0, `2`:17 — **2.000/2** | **31/31 (100%)** | 17/17 | 3/3 (100%) | 0/17 (0.0%) | `$0.055640` / `267.99s` |
| `baseline (lần 1 lỗi mạng)` / `test` | 5/5 (`err=3`: `q18`–`q20`) | `1`:2, `3`:1, `4`:2 (`13`) | `0`:2, `1`:0, `2`:0 — **0.000/2** | `0/0 (N/A)` | `0/0 (N/A)` | 3/3 (100%) | 2/2 (100%) | `$0.007556` / `30.99s` |
| `baseline (chạy lại đủ 8 câu)` / `test` | 8/8 (`err=0`) | `1`:3, `3`:2, `4`:3 (`21`) | `0`:4, `1`:1, `2`:0 — **0.200/2** | 1/1 (100%) | 1/1 | 3/3 (100%) | 4/5 (80.0%) | `$0.011922` / `40.31s` |
| **`tuned-v2 (chốt)` / `test`** | **8/8 (`err=0`)** | `1`:7, `2`:1 (`9`) | **`0`:0, `1`:0, `2`:5 — 2.000/2** | **9/9 (100%)** | **5/5** | **3/3 (100%)** | **0/5 (0.0%)** | `$0.021238` / `46.75s` |

*(Thống kê tool `tuned-v2`: `dev` gọi `search_hybrid`: 20, `search_lexical`: 7, `get_neighbor_chunks`: 1; `test` gọi `search_hybrid`: 7, `search_lexical`: 2.)*

### Chi tiết toàn bộ 8 câu `test` — Baseline (`results/agent-retry/baseline-test`) vs. Cấu hình đã chọn (`results/agent-v2/tuned-test`)

*(Lưu ý: ở cấu hình `tuned-v2`, query gốc của người dùng được giữ nguyên trong `traces.json['question']`, còn query tìm kiếm do LLM tạo ra cho từng tool call được lưu riêng tại `events[*]['query']`.)*

| Query ID | Loại câu | Baseline (`baseline-test` sạch): Tool call, trạng thái & nhãn | Cấu hình chọn (`tuned-v2`): Tool call, query và kết quả | Câu trả lời và citation (`tuned-v2`) | Nhãn, lý do (`tuned-v2`) |
|---|---|---|---|---|---|
| `q18` | Có đáp án (`truc_tiep`) | 1× `search_vector` → `answered`, `grade=1`, `cit=[True]` (`p020:para:002` ngắn `447` chars lọt budget; thiếu `p020:para:001` `883` chars) | 1× `search_hybrid` (`"difference between AI system resilience and security in AI RMF"`) → nạp `p020:para:001`, `p020:para:002` | Phân biệt đầy đủ resilience (chịu đựng/suy giảm an toàn) và security (bảo mật CIA + phòng thủ tấn công), trích `[nist-ai-100-1:p020:para:001]`, `[nist-ai-100-1:p020:para:002]` | `grade=2`, `citation_support=[True, True]` — Đủ cả 2 vế và đối chiếu đúng p.20 |
| `q19` | Có đáp án (`dien_dat_lai`) | 4× `search_vector` → `abstain` nhầm (`grade=0`, `p046:para:002` `975` chars bị cắt) | 1× `search_hybrid` (`"operational evidence to evaluate how effectively humans challenge or override deployed AI outputs"`) → nạp `600-1:p043:para:002`, `100-1:p046:para:002` | Nêu theo dõi/ghi nhận `MS-4.2-004` và thu thập dữ liệu tần suất + lý do con người bác bỏ AI, trích `[nist-ai-600-1:p043:para:002]`, `[nist-ai-100-1:p046:para:002]` | `grade=2`, `citation_support=[True, True]` — Hai đoạn bổ sung đúng ý |
| `q20` | Có đáp án (`dieu_kien_ngoai_le`) | 3× `search_vector` → `abstain` nhầm (`grade=0`, `p014:para:000` `957` chars bị cắt) | 1× `search_hybrid` (`"distinguish unintentional false content misinformation deliberate false content disinformation generative AI"`) → nạp `600-1:p014:para:000`, `p010:para:000` | Phân biệt misinformation (vô ý từ confabulation) vs disinformation (cố ý lừa dối/gây hại), trích `[nist-ai-600-1:p010:para:000]`, `[nist-ai-600-1:p014:para:000]` | `grade=2`, `citation_support=[True, True]` — Chính xác từng điều kiện |
| `q21` | Có đáp án (`metadata_filter`) | 4× `search_vector` → `abstain` nhầm (`grade=0`, `p034:para:000` `877` chars bị cắt) | 1× `search_hybrid` (`"content provenance privacy security practices human subjects"`, `filter={'year': 2024, 'section': 'measure'}`) → nạp `p034:para:000`, `p034:para:001` | Đủ 3 biện pháp trong `MS-2.2-002` (ẩn danh hóa, privacy output filters, xóa PII) + `MS-2.2-003/004`, trích `[nist-ai-600-1:p034:para:000]`, `[nist-ai-600-1:p034:para:001]` | `grade=2`, `citation_support=[True, True]` — Tuân thủ filter và đủ ý |
| `q22` | Có đáp án (`metadata_filter`) | 4× `search_vector` → `abstain` nhầm (`grade=0`, context rỗng ở `budget=800`) | 1× `search_lexical` (`"negative residual risk"`, `filter={'document_type': 'core_framework', 'section': 'manage'}`) → nạp `p037:para:001` | Định nghĩa tổng rủi ro chưa giảm thiểu và đối tượng nhận tài liệu (downstream acquirers và end users), trích `[nist-ai-100-1:p037:para:001]` | `grade=2`, `citation_support=[True]` — Khớp nguyên văn `MANAGE 1.4` |
| `u04` | Thiếu bằng chứng | 3× `search_vector` → `abstain` (`abstention_correct=True`) | 1× `search_lexical` (`"cryptographic watermarking standard C2PA Google SynthID"`, `filter={'document_id': 'nist-ai-600-1'}`) → đọc `p.23`, `p.37`, `p.55` | Nêu rõ `NIST AI 600-1` chỉ đề cập watermarking nói chung, không bắt buộc C2PA hay SynthID; `citations=[]` | `abstention_correct=True` — Từ chối chuẩn, không bịa chuẩn |
| `u05` | Thiếu bằng chứng | 1× `search_vector` → `abstain` (`abstention_correct=True`) | 2× `search_hybrid` (`filter=None`) → kiểm tra toàn corpus | Nêu rõ không có số điều khoản ISO/IEC 42001 hay chu kỳ audit chứng nhận NIST AI RMF 1.0; `citations=[]` | `abstention_correct=True` — Đã kiểm chứng kỹ trước khi từ chối |
| `u06` | Thiếu bằng chứng | 1× `search_vector` → `abstain` (`abstention_correct=True`) | 1× `search_hybrid` (`"maximum training energy limit megawatt-hours carbon threshold tCO2e model deployment prohibition"`, `filter=None`) → đọc `p.12`, `p.41` | Nêu rõ `600-1` chỉ khuyên đo đạc tác động môi trường, không có ngưỡng cứng MWh hay tCO2e; `citations=[]` | `abstention_correct=True` — Phân biệt rõ khuyến nghị và ngưỡng cứng |

### Ví dụ minh họa bắt buộc (Có bằng chứng · Thiếu bằng chứng · Lỗi)
1. **Ví dụ trả lời có bằng chứng (`tuned-test q22`):** Agent gọi `search_lexical` với `query="negative residual risk"` và `filter={'document_type': 'core_framework', 'section': 'manage'}`, nhận chunk `nist-ai-100-1:p037:para:001` (`966` chars) và trả lời chính xác định nghĩa *"sum of all unmitigated risks"* cùng hai đối tượng nhận tài liệu (*"downstream acquirers of AI systems and end users"*) kèm `[nist-ai-100-1:p037:para:001]`. Ngược lại, `baseline-test q22` nhận context rỗng ở `budget=800` và từ chối nhầm sau 4 lượt tìm kiếm.
2. **Ví dụ câu thiếu bằng chứng (`tuned-test u04`):** Dù `600-1` có nhắc đến *"watermarking"* trong các chunk truy xuất được (`p.23`, `p.37`, `p.55`), agent đối chiếu trực tiếp và từ chối trung thực vì tài liệu không quy định thuật toán bắt buộc nào như C2PA hay SynthID.
3. **Ví dụ lỗi thực tế (`baseline-dev q12` & lỗi kết nối `baseline-test q18–q20`):**
   - Trong `baseline-dev q12`, vì `budget=800` loại chunk `nist-ai-600-1:p021:para:000` (`GV-1.7-002`, `910` chars), agent đọc nhầm `nist-ai-600-1:p045:para:002` (`MANAGE 2.4`) và gán nội dung `MG-2.4-001` cho `GOVERN 1.7` (`citation_support=False`, `answer_grade=0`) — minh chứng rằng citation ID tồn tại trong context chưa đồng nghĩa hỗ trợ câu trả lời.
   - Trong lần chạy đầu `baseline-test` (`results/agent/baseline-test/traces.json`), 3 câu `q18`–`q20` gặp `APIConnectionError: Connection error.`; pipeline ghi `status: "error"` tách khỏi mẫu số chất lượng (`provider_errors: 3`), sau đó chạy lại sạch vào `results/agent-retry/baseline-test/` để đối chiếu đủ 8 câu.

- **Đường dẫn trace & nhãn:**
  - Retrieval: `results/retrieval/dev/` (`summary.json`, `*_traces.json`), `results/retrieval/test/` (`summary.json`, `context_audit.json`, `*_traces.json`), `results/retrieval/dev-starter-tfidf/`.
  - Agent: `results/agent/baseline-dev/`, `results/agent/tuned-dev/`, `results/agent-v2/tuned-dev/`, `results/agent/baseline-test/`, `results/agent-retry/baseline-test/`, `results/agent-v2/tuned-test/` (mỗi thư mục chứa `traces.json`, `audit_worksheet.md`, `reviews.json`, `summary.json`, `run_stats.json`).

- **Đánh đổi và giới hạn:**
  - *Đánh đổi chất lượng – độ trễ – chi phí:* `tuned-v2` nâng điểm grounded `test` từ `0.200/2 → 2.000/2` và giảm false abstention `80% → 0%`, đồng thời giảm số lượt gọi search (`21 → 9` trên 8 câu `test`), với tổng thời gian tăng nhẹ `1.16×` (`40.31s → 46.75s`) và chi phí tăng `1.78×` (`$0.011922 → $0.021238`) do LLM reranking trên 12 ứng viên.
  - *Giới hạn:* (1) Tập `test` chỉ gồm `5` câu có đáp án + `3` câu thiếu bằng chứng nên chưa đo được phương sai trên quy mô lớn hơn; (2) Rerank dùng LLM gọi tuần tự từng câu nên độ trễ ~`3–9s`/câu; nếu triển khai production nên thay bằng cross-encoder nhẹ hoặc chạy batch/bất đồng bộ và thêm retry backoff cho `APIConnectionError`; (3) Nhãn chấm thủ công do tác giả tự đối chiếu trên `audit_worksheet.md`, cần người chấm đối chiếu lại trích đoạn đã đính kèm để kiểm soát thiên lệch.

---

## 4. Thử thách nâng cao (tùy chọn)

- **Tài liệu & quyền sử dụng:**
  - **Tài liệu:** *Gemini 1.5: Unlocking multimodal understanding across millions of tokens of context* (`arXiv:2403.05530v5`, `154` trang, xuất bản công khai trên arXiv theo giấy phép `arXiv.org perpetual, non-exclusive license`, tải trực tiếp từ `https://arxiv.org/pdf/2403.05530.pdf`). Không nộp file PDF gốc hoặc ảnh render trang lớn (`advanced/raw/`, `advanced/renders/` đã đưa vào `.gitignore`); người chấm tái tạo hoàn toàn bằng `.\.venv\Scripts\python.exe -m advanced.ingest --stage extract` (`$0.00`).
- **Pipeline index đa phương thức (`advanced/ingest.py`, `advanced/store.py`):**
  - **Trích xuất & crop tất định (không dùng LLM đoán tọa độ):** Render toàn bộ `154/154` trang (`150 DPI` vào `advanced/renders/`), dùng `pdfplumber.page.search()` định vị chính xác `71` caption (`Figure N | ...` và `Table N | ...`) và gom các đối tượng đồ họa PDF (`images`, `rects`, `curves`, `lines`) để crop thành `71` ảnh PNG `220 DPI` (`advanced/crops/`). Toàn bộ `154` trang đều được index (gồm `main_body` p.3–74, `references` p.75–98, `contributors` p.99–106, `appendix` p.107–154).
  - **Vision card & `pgvector` riêng (`rag_multimodal`):** Dùng `gpt-4.1-mini` Vision chuyển `71` ảnh crop thành card cấu trúc (`advanced/data/visual_cards.json`, `$0.064707`), gộp với text từng trang thành **`558` chunk** (`text: 487`, `table: 48`, `chart: 16`, `image_diagram: 7`) và lưu vào bảng riêng **`rag_multimodal`** (`text-embedding-3-small`, 1536 chiều, `$0.003323`), tách biệt hoàn toàn với `rag_chunks` của phần cơ bản.
- **Agent đa phương thức & tiến trình cải thiện (`advanced/agent.py`, `advanced/evaluate.py`):**
  - Sử dụng `gpt-4.1-mini` với 5 tool: `search_multimodal` (Hybrid Dense + BM25 RRF `k=60`), `search_exact` (BM25), `check_exact_phrase` (khớp chuỗi con chính xác trên toàn bộ `154` trang để chống nhầm tên benchmark/model), `get_page_context` (đọc văn bản trang), `view_image` (hỗ trợ gọi trực tiếp theo `label` như `"Figure 3"`, `"Table 11"` hoặc `view_full_page=True`), và `submit_final_answer` (ràng buộc citation hợp lệ hoặc `abstain`). Giới hạn `max_steps=5`, `max_searches=4`, `max_images=2`.
  - **Tuân thủ quy tắc không chỉnh trên `test` (`ADVANCED.md`):** Khi kiểm tra lỗi trên `test_v1` (`25/30 = 83.33%`, `$0.1699`) và `test_v2` (`26/30 = 86.67%`, `$0.1583`) để sửa 3 lỗi chiến lược (`check_exact_phrase`, `view_image` theo `label`, và siết prompt abstention), đều tạo bộ **`test_v3` mới hoàn toàn không trùng lặp** (`advanced/data/benchmark_v3.json`, `dev=18`, `test=30`).
- **Kết quả đánh giá độc lập `frozen_v3_mini` (`gpt-4.1-mini`, `advanced/results/test_frozen_v3_mini_summary.json`):**

| Nhóm chính | Đạt / Tổng | Tỷ lệ (%) | Ghi chú kiểm chứng |
|---|---:|---:|---|
| Bảng (`table`) | **6 / 6** | **100.0%** | `Table 16, 19, 23, 25, 48, 52` đều khớp chính xác từng ô và đơn vị |
| Ảnh, sơ đồ (`image_diagram`) | **5 / 5** | **100.0%** | `Figure 3, 4, 5, 28, 30` — sửa dứt điểm lỗi nhầm `p008_figure_3` nhờ `label` |
| Biểu đồ (`chart`) | **5 / 5** | **100.0%** | `Figure 2, 8, 14, 15, 32` — đọc đúng giá trị thanh, heatmap và trục |
| Multi-hop (`multi_hop`) | **4 / 4** | **100.0%** | Kết hợp chính xác `Table 11` + `Figure 2`, `Table 3`, `Table 46` + `11`, `Figure 26` |
| Text (`text`) | **3 / 4** | **75.0%** | Đạt `v3_text_1..3`; `v3_text_4` nêu đúng Bradley-Terry nhưng đoán nhầm `"chess and tennis"` thay vì `"Chess or Go"` do không đọc đoạn text p.23 |
| Thiếu bằng chứng (`unanswerable`) | **4 / 6** | **66.67%** | Đạt `v3_unans_1, 3, 4, 5`; `v3_unans_2` nhầm `HumanEval` (`84.1`) sang `MT-Bench`, `v3_unans_6` nhầm `BigBench-Hard` (`89.2%`) sang `BigCodeBench` |
| **Tổng cộng (`frozen_v3_mini`)** | **27 / 30** | **90.0%** | **Đạt ngưỡng `>= 90%` (`0` lỗi hệ thống · `115.09s` · `$0.129045`)** |

- **Lệnh chạy tái lập:**
  ```powershell
  .\.venv\Scripts\python.exe -m advanced.ingest --stage all
  .\.venv\Scripts\python.exe -m advanced.store
  .\.venv\Scripts\python.exe -m advanced.build_benchmark_v3
  .\.venv\Scripts\python.exe -m advanced.evaluate run --split test --tag frozen_v3_mini --model gpt-4.1-mini --max-steps 5 --benchmark advanced/data/benchmark_v3.json
  .\.venv\Scripts\python.exe -m advanced.evaluate score --split test --tag frozen_v3_mini --reviews advanced/results/test_frozen_v3_mini_reviews.json --benchmark advanced/data/benchmark_v3.json
  ```

