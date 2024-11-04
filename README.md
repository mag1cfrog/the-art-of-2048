# The Art of 2048: A Modern Take on a Classic Game

## Introduction
2048 is an addictive sliding tile puzzle game that took the world by storm in 2014. Originally created by Gabriele Cirulli ([original source code](https://github.com/gabrielecirulli/2048)), the game is elegantly simple yet deeply engaging - merge tiles with the same numbers to reach the coveted 2048 tile. The original implementation was written in JavaScript using a 2D array to represent the game grid.

## Game Architecture: A Modern Modular Approach

Our implementation takes this classic game and rebuilds it with modern software engineering practices, splitting it into distinct components:

### Backend Architecture
- **Core Game Logic**: Implemented in Python, maintaining game state and rules
- **Multiple Storage Implementations**:
  - Traditional 2D array (like the original)
  - Optimized bit-based implementation (experimental)
    - Uses 4 bits per cell to store number exponents
    - Entire 4x4 grid fits in a single 64-bit integer
    - Faster operations through bitwise manipulation
    - Trade-off: Higher complexity vs Better performance

### Communication Layer
- Flexible interface supporting:
  - In-process communication for local play
  - WebSocket API for networked gameplay
  - Easy to extend for new protocols

### Frontend Implementations
1. **CLI Interface**
   - Lightweight development/testing interface
   - Quick feedback loop for backend changes

2. **Modern Web Interface**
   - Built with Vite + React + TypeScript
   - Responsive design using Tailwind CSS
   - Smooth animations with Framer Motion
   - Clean, intuitive UI inspired by the original

## Technical Deep Dives

### Bit-based Grid Implementation
Instead of storing actual numbers (2,4,8,16...), we store their exponents (1,2,3,4...), each requiring only 4 bits:
```python
# Example bit representation for a 4x4 grid
# 2048 (exponent 11) in top-left, 4 (exponent 2) in center
grid = 0b1011_0000_0010_0000_0000_0000_0000_0000
```
This method optimizes memory usage and accelerates computations through bitwise manipulation, albeit with increased implementation complexity.

### WebSocket Communication Protocol
A clean, efficient JSON-based protocol facilitates seamless communication between frontend and backend:
```json
// Client -> Server (Move)
{"type": "move", "direction": 0}

// Server -> Client (State Update)
{
  "grid": [[2, null, 4, 8], ...],
  "score": 256,
  "over": false
}
```

## Deployment & Playing

The game is containerized using Docker and deployed on Oracle Cloud. Experience it live at:
[http://165.1.78.70:8000/](http://165.1.78.70:8000/)

### Docker Setup
A single multi-stage Dockerfile combines:
- **Frontend Build**: Compiles the React application.
- **Backend Setup**: Installs Python dependencies and game logic.
- **Final Image**: Merges frontend and backend, optimized for size and startup time.

## AI Solver: Mastering 2048

Exploring artificial intelligence for solving 2048, we've implemented algorithms like depth-first alpha-beta search:
- **Why It Works**:
  - Efficiently explores possible moves.
  - Evaluates game states based on factors like monotonicity and potential merges.
- **Demo**: Check out a [JavaScript visualization of the AI](https://ovolve.github.io/2048-AI/) created a decade ago.

## Future Improvements

- **Multiplayer Mode**: Compete or collaborate with others.
- **Advanced AI Strategies**: Incorporate machine learning techniques.
- **Mobile Optimization**: Enhance touch controls for mobile devices.
- **Progressive Web App (PWA)**: Allow offline play and better performance.

## Additional Highlights

- **Local Storage Management**: Utilizes JSON files to persist game state and best scores, ensuring a seamless user experience across sessions.
- **Modular Codebase**: Organized into clearly defined services and components, making maintenance and scalability straightforward.
- **Responsive Design**: Tailwind CSS ensures the game looks great on all devices.

## Contributing

Contributions are welcome! Please check our [contribution guidelines](CONTRIBUTING.md) and [code of conduct](CODE_OF_CONDUCT.md) for more details.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.