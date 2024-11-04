import React from 'react';
import { motion } from 'framer-motion';

const tileColors: Record<number, string> = {
  2: 'bg-purple-200',
  4: 'bg-purple-300',
  8: 'bg-purple-400',
  16: 'bg-purple-500',
  32: 'bg-purple-600',
  64: 'bg-indigo-500',
  128: 'bg-indigo-600',
  256: 'bg-pink-500',
  512: 'bg-pink-600',
  1024: 'bg-rose-500',
  2048: 'bg-rose-600',
};

interface GameGridProps {
  grid: Array<Array<{ position: [number, number]; value: number } | null>>;
}

export const GameGrid: React.FC<GameGridProps> = ({ grid }) => {
  // Transpose the grid to switch rows and columns
  const transposedGrid = grid[0].map((_, colIndex) => grid.map(row => row[colIndex]));

  return (
    <div
      className="grid grid-cols-4 gap-3 bg-white/5 p-3 rounded-lg"
      tabIndex={-1} // Prevent the grid from receiving focus
      onFocus={(e) => e.preventDefault()} // Prevent focus events
    >
      {transposedGrid.map((col, i) => (
        <React.Fragment key={i}>
          {col.map((cell, j) => (
            <div
              key={`${i}-${j}`}
              className="relative aspect-square bg-white/10 rounded-lg"
              tabIndex={-1} // Prevent each tile from receiving focus
              onFocus={(e) => e.preventDefault()} // Prevent focus events
            >
              {cell && (
                <motion.div
                  key={`${cell.position[0]}-${cell.position[1]}-${cell.value}-${j}`} // Include j to ensure uniqueness
                  layout // Enables Framer Motion's layout animations
                  initial={{ scale: 0.8, opacity: 0 }}
                  animate={{ scale: 1, opacity: 1 }}
                  exit={{ scale: 0.8, opacity: 0 }}
                  className={`absolute inset-0 flex items-center justify-center ${
                    tileColors[cell.value] || 'bg-purple-700'
                  } rounded-lg shadow-lg`}
                  transition={{ type: 'spring', stiffness: 500, damping: 30 }}
                >
                  <span className={`text-2xl font-bold ${cell.value >= 8 ? 'text-white' : 'text-gray-800'}`}>
                    {cell.value}
                  </span>
                </motion.div>
              )}
            </div>
          ))}
        </React.Fragment>
      ))}
    </div>
  );
};