// 本地存储工具

const SESSION_ID_KEY = 'cs2_bp_session_id';
const USER_ID_KEY = 'cs2_bp_user_id';

export const storage = {
  // 获取会话ID
  getSessionId(): string {
    let sessionId = localStorage.getItem(SESSION_ID_KEY);
    if (!sessionId) {
      sessionId = generateSessionId();
      localStorage.setItem(SESSION_ID_KEY, sessionId);
    }
    return sessionId;
  },

  // 设置会话ID
  setSessionId(sessionId: string): void {
    localStorage.setItem(SESSION_ID_KEY, sessionId);
  },

  // 获取用户ID
  getUserId(): string | null {
    return localStorage.getItem(USER_ID_KEY);
  },

  // 设置用户ID
  setUserId(userId: string): void {
    localStorage.setItem(USER_ID_KEY, userId);
  },

  // 清除用户数据
  clearUserData(): void {
    localStorage.removeItem(USER_ID_KEY);
  },
};

function generateSessionId(): string {
  return `${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
}
