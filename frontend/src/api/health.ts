import { API_BASE_URL } from "../config";

export type HealthResponse = {
  status: string;
  message: string;
};

export async function fetchHealth(): Promise<HealthResponse> {
  const response = await fetch(`${API_BASE_URL}/health`);
  if (!response.ok) {
    throw new Error(`健康检查失败: HTTP ${response.status}`);
  }
  return response.json() as Promise<HealthResponse>;
}
