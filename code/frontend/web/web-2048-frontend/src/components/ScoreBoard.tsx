import React from 'react';
import { motion } from 'framer-motion';

interface ScoreBoardProps {
  score: number;
}

export const ScoreBoard: React.FC<ScoreBoardProps> = ({ score }) => {
  return (
    <div
      className="flex justify-between items-center mb-6"
      tabIndex={-1} // Prevent the scoreboard from receiving focus
      onFocus={(e) => e.preventDefault()} // Prevent focus events
    >
      <motion.div
        initial={{ scale: 0 }}
        animate={{ scale: 1 }}
        className="bg-white/10 rounded-lg p-4 text-center min-w-[120px]"
        tabIndex={-1} // Prevent inner motion div from receiving focus
        onFocus={(e) => e.preventDefault()} // Prevent focus events
      >
        <div className="text-sm text-purple-200 mb-1">SCORE</div>
        <motion.div
          key={score}
          initial={{ scale: 1.5, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          className="text-2xl font-bold"
          tabIndex={-1} // Prevent score number from receiving focus
          onFocus={(e) => e.preventDefault()} // Prevent focus events
        >
          {score}
        </motion.div>
      </motion.div>
    </div>
  );
};