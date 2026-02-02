// BP 阶段配置
export const BP_PHASES = [
  { phase: 1, action: 'ban', instruction: '禁用1张地图' },
  { phase: 2, action: 'ban', instruction: '禁用1张地图' },
  { phase: 3, action: 'pick', instruction: '选择1张地图' },
  { phase: 4, action: 'pick', instruction: '选择1张地图' },
  { phase: 5, action: 'ban', instruction: '禁用1张地图' },
  { phase: 6, action: 'ban', instruction: '禁用1张地图' },
  { phase: 7, action: 'decider', instruction: '决胜图展示' },
] as const;

// 操作时间（秒）
export const OPERATION_TIME = 15;

// 每队最大用户数
export const MAX_USERS_PER_TEAM = 5;

// 房间码长度
export const ROOM_CODE_LENGTH = 8;
