// API 基础配置
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

// 获取 token
const getToken = () => {
  if (typeof window !== 'undefined') {
    return localStorage.getItem('token');
  }
  return null;
};

// 通用请求函数
async function fetchApi<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const url = `${API_BASE_URL}${endpoint}`;
  const token = getToken();

  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    ...((options.headers as Record<string, string>) || {}),
  };

  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  const response = await fetch(url, {
    ...options,
    headers,
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(error.message || `请求失败: ${response.status}`);
  }

  const result = await response.json();
  // 处理后端统一响应格式 { code: 200, msg: "success", data: {...} }
  if (result && result.code === 200 && result.data !== undefined) {
    return result.data;
  }
  return result;
}

// 用户相关 API
export interface UserInfo {
  id: string;
  name: string;
  email: string;
  phone?: string;
  company?: string;
  role: string;
  createdAt: string;
}

export interface UpdateUserInfoData {
  name?: string;
  phone?: string;
  email?: string;
}

// 获取用户信息
export async function getUserInfo(): Promise<UserInfo> {
  return fetchApi<UserInfo>('/user/info');
}

// 更新用户信息
export async function updateUserInfo(data: UpdateUserInfoData): Promise<UserInfo> {
  return fetchApi<UserInfo>('/user/info', {
    method: 'PUT',
    body: JSON.stringify(data),
  });
}

// 登录
export interface LoginData {
  email: string;
  password: string;
}

export interface LoginResponse {
  token: string;
  user: UserInfo;
}

export async function login(data: LoginData): Promise<LoginResponse> {
  return fetchApi<LoginResponse>('/auth/login', {
    method: 'POST',
    body: JSON.stringify(data),
  });
}

// 注册
export interface RegisterData {
  name: string;
  email: string;
  password: string;
  userType?: number;
}

export async function register(data: RegisterData): Promise<LoginResponse> {
  return fetchApi<LoginResponse>('/auth/register', {
    method: 'POST',
    body: JSON.stringify(data),
  });
}
