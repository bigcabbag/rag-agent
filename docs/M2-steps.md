# M2 分步指南：基础 RAG

M2 拆成 3 小步，从简到难。**当前进度：M2.1 已完成代码，待你验收。**

---

## M2.1 上传 PDF → 切块（当前）

**目标**：把 PDF 变成很多小文本块（Document），还不做向量检索。

### RAG 链路里的位置

```
Load → Split → Embed → Store → Retrieve → Generate
 ↑       ↑
M2.1   M2.1
```

### 新增文件

| 文件 | 作用 |
|------|------|
| `app/rag/loader.py` | PyPDFLoader 读 PDF + RecursiveCharacterTextSplitter 切块 |
| `POST /documents/upload` | 接收 PDF，保存到 `data/uploads/`，返回块数和预览 |

### 怎么验收

1. 启动：`uv run python main.py`
2. 打开 http://127.0.0.1:8000/docs
3. 找到 `POST /documents/upload`，上传一份 **2～10 页** 的 PDF
4. 期望返回：
   - `chunk_count` > 0
   - `previews` 里能看到前几块的文字片段和 `metadata`（含 `page` 页码）

### 面试 3 题（M2.1）

1. **为什么要切块（chunk）？**  
   整篇 PDF 太长，超过 LLM 上下文窗口；检索也需要「段落级」粒度才能命中相关片段。

2. **chunk_size 和 chunk_overlap 是什么？**  
   `chunk_size` 每块最大字符数；`overlap` 相邻块重叠字符数，避免一句话被切在边界上丢失语义。

3. **RecursiveCharacterTextSplitter 做了什么？**  
   按 `\n\n` → `\n` → 空格 → 字符 的优先级递归切分，尽量在段落/句子边界断开。

---

## M2.2 Embedding + Chroma（下一步）

**目标**：把每块文本变成向量，存入本地 Chroma。

说「继续 M2.2」开始。

---

## M2.3 检索 + RAG 问答（最后）

**目标**：用户提问 → 检索相关块 → 拼进 prompt → `/chat` 生成带引用的回答。

说「继续 M2.3」开始。
