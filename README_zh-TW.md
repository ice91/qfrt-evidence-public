# QFRT 證據倉庫（Artifact-First）

本倉庫是整理後的**技術證據錨點**，用途是提供：

- 凍結的報表與摘要，
- 可追溯的輕量中繼資料，
- 導出面向提交與審查 bundle 的工具，
- 對證據內容的文件化說明。

本倉庫**不是**完整實驗執行環境。

---

## 範圍

包含：

- `docs/`：證據解讀與圖表對照說明
- `artifacts/reporting/`：整理後的報告快照
- `artifacts/index/`：run 索引中繼資料
- `artifacts/manifest.json`：整體指向資訊
- `scripts/export_*.py`：導出工具

不包含（不作為本倉庫執行合約）：

- 完整 benchmark 執行堆疊
- 大型原始 run 輸出目錄
- 與特定機器綁定的絕對路徑

---

## 目錄

- `docs/`：證據導向文件
- `artifacts/`：凍結報告與可追溯中繼資料
- `scripts/`：面向提交與審查的導出工具

---

## 使用方式

請把本倉庫當作 **讀取 + 導出** 介面：

1. 從 `artifacts/reporting/` 讀取整理後的摘要與表格
2. 用 `artifacts/index/` 與 `artifacts/manifest.json` 做來源核對
3. 使用導出工具產出便於審查的 bundle

需要大量重跑或完整執行流程時，請使用對應的私有執行環境。

---

## 發布前規則

- 路徑需保持 repo-local 與可攜。
- 若仍有未解決依賴，必須以 TODO/placeholder 明示。
- 本倉庫以 BSD 3-Clause License 發布。
