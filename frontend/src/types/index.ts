// 房间相关类型
export interface Room {
  id: string;
  room_code: string;
  team_a_name: string;
  team_a_icon: string;
  team_b_name: string;
  team_b_icon: string;
  status: RoomStatus;
  mappool: MapPoolConfig;
}

export type RoomStatus = 'waiting' | 'rolling' | 'ban1' | 'ban2' | 'pick1' | 'decider' | 'finished';

export interface MapPoolConfig {
  map01_name: string;
  map01_icon: string;
  map02_name: string;
  map02_icon: string;
  map03_name: string;
  map03_icon: string;
  map04_name: string;
  map04_icon: string;
  map05_name: string;
  map05_icon: string;
  map06_name: string;
  map06_icon: string;
  map07_name: string;
  map07_icon: string;
}

// 用户相关类型
export interface User {
  id: string;
  session_id: string;
  room_id: string | null;
  team: 'team_a' | 'team_b' | null;
  display_name: string | null;
  is_ready: boolean;
}

// BP相关类型
export interface MapCard {
  id: string;
  name: string;
  icon: string;
  status: 'available' | 'banned' | 'picked' | 'decider';
  picked_by?: string;
  banned_by?: string;
  order?: number;
  is_current?: boolean;
  teammate_intent?: string;
}

export interface BPState {
  phase: number;
  current_team: string | null;
  current_user: string | null;
  remaining_time: number;
  maps: MapCard[];
  roll_result: RollResult | null;
  result: BPResult | null;
}

export interface RollResult {
  roll_a: number;
  roll_b: number;
}

export interface BPResult {
  phase_1_ban: { map_id: string; team: string };
  phase_2_ban: { map_id: string; team: string };
  phase_3_pick: { map_id: string; team: string };
  phase_4_pick: { map_id: string; team: string };
  phase_5_ban: { map_id: string; team: string };
  phase_6_ban: { map_id: string; team: string };
  decider: { map_id: string };
}

// 聊天相关类型
export interface Message {
  team: string;
  user_name: string;
  content: string;
  timestamp: string;
}
