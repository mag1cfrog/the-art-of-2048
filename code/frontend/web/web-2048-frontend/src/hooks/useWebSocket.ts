import { useState, useEffect, useCallback, useRef } from 'react';

const WS_URL = 'ws://localhost:8000/ws/game';

export const useWebSocket = () => {
  const [connectionStatus, setConnectionStatus] = useState<'Connecting' | 'Connected' | 'Disconnected'>('Connecting');
  const [lastMessage, setLastMessage] = useState<string | null>(null);
  const wsRef = useRef<WebSocket | null>(null);

  const connect = useCallback(() => {
    try {
      const ws = new WebSocket(WS_URL);
      wsRef.current = ws;

      ws.onopen = () => {
        setConnectionStatus('Connected');
        console.log('Connected to WebSocket server');
        // Request initial game state
        ws.send(JSON.stringify({ type: 'init' }));
      };

      ws.onmessage = (event) => {
        console.log('Received message:', event.data);
        setLastMessage(event.data);
      };

      ws.onclose = () => {
        console.log('WebSocket connection closed');
        setConnectionStatus('Disconnected');
        wsRef.current = null;
        setTimeout(connect, 1000); // Attempt to reconnect
      };

      ws.onerror = (error) => {
        console.error('WebSocket error:', error);
        ws.close();
      };
    } catch (err) {
      console.error('WebSocket connection error:', err);
      setConnectionStatus('Disconnected');
      setTimeout(connect, 1000);
    }
  }, []);

  useEffect(() => {
    connect();
    return () => {
      if (wsRef.current) {
        wsRef.current.close();
      }
    };
  }, [connect]);

  const sendMessage = useCallback((data: any) => {
    if (wsRef.current?.readyState === WebSocket.OPEN) {
      console.log('Sending message:', data);
      wsRef.current.send(JSON.stringify(data));
    } else {
      console.warn('WebSocket is not connected');
    }
  }, []);

  return {
    sendMessage,
    lastMessage,
    connectionStatus,
  };
};