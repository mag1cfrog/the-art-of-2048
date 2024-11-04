import { useEffect, useState, useCallback } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Gamepad2, RotateCcw, Trophy } from 'lucide-react';
import { GameGrid } from './components/GameGrid';
import { ScoreBoard } from './components/ScoreBoard';
import { useWebSocket } from './hooks/useWebSocket';
import { useKeyboard } from './hooks/useKeyboard';


function App() {
  const [gameState, setGameState] = useState({
    grid: Array(4).fill(null).map(() => Array(4).fill(null)),
    score: 0,
    over: false,
    won: false
  });

  const { sendMessage, lastMessage, connectionStatus } = useWebSocket();

  const handleRestart = useCallback(() => {
    console.log('Restarting game');
    sendMessage({ type: 'restart' });
  }, [sendMessage]);

  const handleMove = useCallback((direction: number) => {
    if (!gameState.over) {
      console.log('Sending move:', direction);
      sendMessage({ type: 'move', direction });
    }
  }, [gameState.over, sendMessage]);

  const handleKeyPress = useCallback((key: string) => {
    switch(key) {
      case 'ArrowUp':
      case 'w':
      case 'W':
        handleMove(0); // Up
        break;
      case 'ArrowRight':
      case 'd':
      case 'D':
        handleMove(1); // Right
        break;
      case 'ArrowDown':
      case 's':
      case 'S':
        handleMove(2); // Down
        break;
      case 'ArrowLeft':
      case 'a':
      case 'A':
        handleMove(3); // Left
        break;
      case 'Escape':
        handleRestart(); // Exit the game
        break;
      default:
        break;
    }
  }, [handleMove, handleRestart]);

  useKeyboard(handleKeyPress);

  useEffect(() => {
    if (lastMessage) {
      try {
        console.log('Processing game state:', lastMessage);
        const newState = JSON.parse(lastMessage);
        setGameState({
          ...newState,
          grid: newState.grid.cells, // Extract cells array
        });
      } catch (e) {
        console.error('Failed to parse game state:', e);
      }
    }
  }, [lastMessage]);

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-900 via-purple-900 to-pink-900 text-white no-caret">
      <div className="container mx-auto px-4 py-8 max-w-2xl">
        <header className="text-center mb-8 no-caret">
          <div className="flex items-center justify-center gap-2 mb-4">
            <Gamepad2 className="w-8 h-8" />
            <h1 className="text-4xl font-bold">2048</h1>
          </div>
          <p className="text-purple-200">Join the numbers and get to the 2048 tile!</p>
        </header>

        <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-6 shadow-xl mb-8 no-caret">
          <ScoreBoard score={gameState.score} />
          
          <div className="relative no-caret">
            <GameGrid grid={gameState.grid} />

            <AnimatePresence>
              {(gameState.over || gameState.won) && (
                <motion.div
                  initial={{ opacity: 0, scale: 0.8 }}
                  animate={{ opacity: 1, scale: 1 }}
                  exit={{ opacity: 0, scale: 0.8 }}
                  className="absolute inset-0 flex items-center justify-center bg-black/70 rounded-lg backdrop-blur-sm no-caret"
                >
                  <div className="text-center p-6 no-caret">
                    {gameState.won && (
                      <div className="flex justify-center mb-4 no-caret">
                        <Trophy className="w-16 h-16 text-yellow-400" />
                      </div>
                    )}
                    <h2 className="text-3xl font-bold mb-4 no-caret">
                      {gameState.won ? 'You Won!' : 'Game Over!'}
                    </h2>
                    <button
                      onClick={handleRestart}
                      className="flex items-center gap-2 px-6 py-3 bg-purple-600 hover:bg-purple-700 rounded-full transition-colors mx-auto focus:outline-none no-caret"
                      onMouseDown={(e) => e.preventDefault()}
                    >
                      <RotateCcw className="w-5 h-5" />
                      Play Again
                    </button>
                  </div>
                </motion.div>
              )}
            </AnimatePresence>
          </div>

          {connectionStatus !== 'Connected' && (
            <div className="text-center mt-4 p-4 bg-red-500/20 rounded-lg no-caret">
              {connectionStatus === 'Connecting' ? 'Connecting to server...' : 'Connection lost. Trying to reconnect...'}
            </div>
          )}
        </div>

        <div className="text-center text-purple-200 no-caret">
          <p className="mb-2">Use arrow keys or WASD to move tiles</p>
          <div className="flex justify-center gap-2 no-caret">
            <button
              onClick={() => handleMove(0)} // Up
              className="p-2 bg-white/10 rounded hover:bg-white/20 transition-colors focus:outline-none"
              onMouseDown={(e) => e.preventDefault()}
            >
              ↑
            </button>
            <button
              onClick={() => handleMove(2)} // Down
              className="p-2 bg-white/10 rounded hover:bg-white/20 transition-colors focus:outline-none"
              onMouseDown={(e) => e.preventDefault()}
            >
              ↓ 
            </button>
            <button
              onClick={() => handleMove(3)} // Left
              className="p-2 bg-white/10 rounded hover:bg-white/20 transition-colors focus:outline-none"
              onMouseDown={(e) => e.preventDefault()}
            >
              ←
            </button>
            <button
              onClick={() => handleMove(1)} // Right
              className="p-2 bg-white/10 rounded hover:bg-white/20 transition-colors focus:outline-none"
              onMouseDown={(e) => e.preventDefault()}
            >
              →
            </button>
          </div>
          <button
            onClick={handleRestart}
            className="mt-4 px-4 py-2 bg-red-500 hover:bg-red-600 rounded focus:outline-none no-caret"
            onMouseDown={(e) => e.preventDefault()}
          >
            Exit Game
          </button>
        </div>
      </div>
    </div>
  );
}

export default App;