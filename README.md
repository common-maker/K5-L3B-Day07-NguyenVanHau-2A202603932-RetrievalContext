# Day 7 — Agentic RAG

**Bài cá nhân · Python 3.11+ · tiếp nối Day 6**

Dùng embedding và vector store từ Day 6 để xây một agent biết tìm bằng chứng, trả lời có nguồn và nhận biết khi không đủ thông tin. Bạn tự chọn kiến trúc, số tool và cách tổ chức retrieval.

> **Tùy chọn:** [Gợi ý dùng AI để lập trình](AGENT_SETUP.md) giúp bạn làm lab; phần này không bắt buộc và không tính điểm.

## Bài cần làm

![Agent tìm tài liệu trong kho Day 6 và trả lời có nguồn](assets/retrieval-pipeline.svg)

1. Kết nối dữ liệu, embedding và vector store Day 6.
2. Xây agent dùng model thật và ít nhất một khả năng truy xuất dữ liệu. Agent có thể dùng nhiều tool và nhiều lượt gọi.
3. Thử **ít nhất 3 phương pháp retrieval khác nhau**, trong đó có dense retrieval dùng vector store Day 6. Tự chọn các phương pháp còn lại; xem [gợi ý](GUIDE.md#2-thử-các-phương-pháp-retrieval).
4. Thử nhiều cấu hình, benchmark, phân tích lỗi và chọn cấu hình tốt trên **dev**; sau đó đánh giá trên **test**.

Benchmark tối thiểu có **24 câu**: dev gồm 15 câu có đáp án và 2 câu thiếu bằng chứng; test gồm 5 câu có đáp án và 2 câu thiếu bằng chứng. Xem [benchmark](BENCHMARK.md) và [rubric](RUBRIC.md).

## Thử thách nâng cao · +15 điểm

Index một tài liệu thực tế từ **100 trang** có bảng, ảnh và biểu đồ; xây agent truy xuất và trả lời các câu hỏi về nội dung đó. Hoàn thành [thử thách nâng cao](ADVANCED.md) và đạt **ít nhất 90% benchmark test** để nhận 15 điểm bonus. Phần cơ bản tối đa 85 điểm; toàn bài tối đa 100 điểm.

## Bắt đầu

1. Đọc [hướng dẫn](GUIDE.md), [rubric](RUBRIC.md) và [quy tắc](RULES.md).
2. Tạo repo cá nhân theo [cách nộp bài](SUBMISSION.md), chuẩn bị đầu ra Day 6 và model hỗ trợ tool calling.
3. Dùng hoặc thay thế [starter](starter/README.md); bạn cần kết nối model và vector store thật.
4. Chạy `python -m unittest discover -s tests -v`. Test mock chỉ kiểm tra code, không phải benchmark agent thật.

![Các bước thử nghiệm trên dev và đánh giá trên test](assets/experiment-loop.svg)

Nộp code, cách chạy, cấu hình, benchmark, trace và [báo cáo](report/individual/MSSV_HoTen.md). Thời gian ở [checkpoints](CHECKPOINTS.md) là gợi ý, có thể điều chỉnh theo lớp và phạm vi thử nghiệm.

## Triển khai cá nhân (Day 7)

- **Báo cáo cá nhân:** [2A202603932_NguyenVanHau.md](report/individual/2A202603932_NguyenVanHau.md)
- **Nguồn Day 6 liên kết:** `https://github.com/common-maker/K5-L3B-Day06-NguyenVanHau-2A202603932-DataIngestion` (commit `5cc2ab253cb12815f43677356a0c74616328de54`) — dữ liệu NIST đã xuất sẵn tại `data/nist_chunks.json`, `data/nist_questions.json`, `data/nist_cases.json`, `data/nist_manifest.json`.
- **Code chính:** [src/](src/README.md) · **Docker DB độc lập:** `docker-compose.yml`, `init.sql`
- **Cài đặt môi trường & khởi tạo `pgvector` (không cần clone lại Day 6):**
  ```powershell
  python -m venv .venv
  .\.venv\Scripts\pip.exe install -r requirements.txt
  Copy-Item .env.example .env   # điền DATABASE_URL và OPENAI_API_KEY
  docker compose up -d --wait   # bỏ qua nếu container day6_student_starter đã chạy ở 127.0.0.1:55433
  .\.venv\Scripts\python.exe -m src.bootstrap_pgvector
  ```
- **Chạy kiểm thử & benchmark:**
  ```powershell
  python -m unittest discover -s tests -v
  .\.venv\Scripts\python.exe -m src.eval_retrieval --split dev
  .\.venv\Scripts\python.exe -m src.eval_retrieval --split test --configs m1_dense_baseline imp1_hybrid_rerank_b2400
  .\.venv\Scripts\python.exe -m src.eval_agent --split test --mode tuned --primary-strategy hybrid_rerank --budget 2800 --output results/agent-v2
  ```
