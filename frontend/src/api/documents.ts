import { API_BASE_URL } from "../config";

export type IndexStats = {
  collection: string;
  vector_count: number;
  embedding_model: string;
};

export type ChunkPreview = {
  index: number;
  content: string;
  metadata: Record<string, unknown>;
};

export type UploadResult = {
  filename: string;
  chunk_count: number;
  chunk_size: number;
  chunk_overlap: number;
  indexed_chunks: number;
  vector_count: number;
  embedding_model: string;
  previews: ChunkPreview[];
};

async function parseError(response: Response): Promise<string> {
  let detail = `HTTP ${response.status}`;
  try {
    const err = (await response.json()) as { detail?: string | { msg: string }[] };
    if (typeof err.detail === "string") {
      detail = err.detail;
    } else if (Array.isArray(err.detail) && err.detail[0]?.msg) {
      detail = err.detail[0].msg;
    }
  } catch {
    /* ignore */
  }
  return detail;
}

export async function fetchDocumentStats(): Promise<IndexStats> {
  const response = await fetch(`${API_BASE_URL}/documents/stats`);
  if (!response.ok) {
    throw new Error(await parseError(response));
  }
  return response.json() as Promise<IndexStats>;
}

export async function uploadDocument(file: File): Promise<UploadResult> {
  const form = new FormData();
  form.append("file", file);

  const response = await fetch(`${API_BASE_URL}/documents/upload`, {
    method: "POST",
    body: form,
  });

  if (!response.ok) {
    throw new Error(await parseError(response));
  }

  return response.json() as Promise<UploadResult>;
}
