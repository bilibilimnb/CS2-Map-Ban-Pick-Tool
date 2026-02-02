import { io, Socket } from 'socket.io-client';

const WS_BASE_URL = import.meta.env.VITE_WS_BASE_URL || 'http://localhost:8000';

class SocketService {
  private socket: Socket | null = null;
  private listeners: Map<string, Function[]> = new Map();

  connect(roomId: string, sessionId: string): void {
    if (this.socket) {
      this.disconnect();
    }

    this.socket = io(WS_BASE_URL, {
      query: { room_id: roomId, session_id: sessionId },
      transports: ['websocket'],
    });

    this.setupEventListeners();
  }

  disconnect(): void {
    if (this.socket) {
      this.socket.disconnect();
      this.socket = null;
    }
    this.listeners.clear();
  }

  private setupEventListeners(): void {
    if (!this.socket) return;

    // 用户加入
    this.socket.on('user_joined', (data) => {
      this.emit('user_joined', data);
    });

    // 用户离开
    this.socket.on('user_left', (data) => {
      this.emit('user_left', data);
    });

    // 队伍信息更新
    this.socket.on('team_updated', (data) => {
      this.emit('team_updated', data);
    });

    // BP 开始
    this.socket.on('bp_started', (data) => {
      this.emit('bp_started', data);
    });

    // BP 阶段变更
    this.socket.on('bp_phase_changed', (data) => {
      this.emit('bp_phase_changed', data);
    });

    // 地图被 Ban
    this.socket.on('map_banned', (data) => {
      this.emit('map_banned', data);
    });

    // 地图被 Pick
    this.socket.on('map_picked', (data) => {
      this.emit('map_picked', data);
    });

    // 计时器更新
    this.socket.on('timer_tick', (data) => {
      this.emit('timer_tick', data);
    });

    // 聊天消息
    this.socket.on('chat_message', (data) => {
      this.emit('chat_message', data);
    });

    // BP 结束
    this.socket.on('bp_finished', (data) => {
      this.emit('bp_finished', data);
    });
  }

  on(event: string, callback: Function): void {
    if (!this.listeners.has(event)) {
      this.listeners.set(event, []);
    }
    this.listeners.get(event)?.push(callback);

    if (this.socket) {
      this.socket.on(event, callback);
    }
  }

  off(event: string, callback?: Function): void {
    if (callback) {
      const callbacks = this.listeners.get(event);
      if (callbacks) {
        const index = callbacks.indexOf(callback);
        if (index > -1) {
          callbacks.splice(index, 1);
        }
      }
    } else {
      this.listeners.delete(event);
    }

    if (this.socket) {
      this.socket.off(event, callback);
    }
  }

  private emit(event: string, data: any): void {
    const callbacks = this.listeners.get(event);
    if (callbacks) {
      callbacks.forEach(cb => cb(data));
    }
  }

  // 发送事件
  emitJoinRoom(roomId: string, sessionId: string): void {
    this.socket?.emit('join_room', { room_id: roomId, session_id: sessionId });
  }

  emitSelectTeam(roomId: string, sessionId: string, team: string): void {
    this.socket?.emit('select_team', { room_id: roomId, session_id: sessionId, team });
  }

  emitUpdateName(roomId: string, sessionId: string, displayName: string): void {
    this.socket?.emit('update_name', { room_id: roomId, session_id: sessionId, display_name: displayName });
  }

  emitReady(roomId: string, sessionId: string, isReady: boolean): void {
    this.socket?.emit('ready', { room_id: roomId, session_id: sessionId, is_ready: isReady });
  }

  emitBanMap(roomId: string, sessionId: string, mapId: string): void {
    this.socket?.emit('ban_map', { room_id: roomId, session_id: sessionId, map_id: mapId });
  }

  emitPickMap(roomId: string, sessionId: string, mapId: string): void {
    this.socket?.emit('pick_map', { room_id: roomId, session_id: sessionId, map_id: mapId });
  }

  emitSendChat(roomId: string, sessionId: string, content: string): void {
    this.socket?.emit('send_chat', { room_id: roomId, session_id: sessionId, content });
  }
}

export const socketService = new SocketService();
