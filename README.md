# ZAO Fractal Voting System

A simplified Discord bot for structured group decision-making through fractal voting. Create transparent, democratic voting processes with automatic group management and real-time results.

## Overview

The ZAO Fractal Voting System streamlines group consensus-building with these core features:

- **Simplified Setup**: One command creates everything - no complex forms or setup
- **Auto-Generated Groups**: Smart naming with daily counters per server
- **Progressive Elimination**: Vote through rounds until one winner emerges
- **Public & Transparent**: All votes and results visible to everyone
- **Tie-Breaking**: Automatic random selection for tied votes
- **Multi-Channel Results**: Results posted to both fractal thread and general channel
- **Admin Controls**: Full management tools for moderators

## Key Features

### **🚀 Streamlined User Experience**
- **One-Command Setup**: `/zaofractal` does everything automatically
- **Smart Member Detection**: Pulls members from your current voice channel
- **Quick Confirmation**: Simple ✅/❌ buttons to start or modify participants
- **Auto-Naming**: Groups named "Fractal Group 1 - Nov 2, 2025" with daily counters

### **🎯 Transparent Voting Process**
- **Public Threads**: Everyone can see the voting process for full transparency
- **Real-Time Updates**: Live vote announcements as they happen
- **Vote Changes Allowed**: Participants can modify votes during each round
- **50% Threshold**: Requires majority support to advance (not just plurality)
- **Tie-Breaking**: Random selection when candidates tie with equal votes

### **📊 Comprehensive Results**
- **Round-by-Round Winners**: Clear announcements after each level
- **Final Rankings**: Complete 1st, 2nd, 3rd place results
- **Dual Distribution**: Results in fractal thread + summary in general channel
- **Persistent Archives**: Completed groups remain for future reference

### **🛠️ Admin Management**
- **Force End Groups**: `/admin_end_fractal` for stuck processes
- **List Active Groups**: `/admin_list_fractals` shows all running fractals
- **Cleanup Tools**: `/admin_cleanup` removes old/broken groups
- **Full Oversight**: Admins can manage any fractal group

## Installation

1. **Clone this repository:**
   ```bash
   git clone https://github.com/bettercallzaal/fractalbotV3June2025.git
   cd fractalbotV3June2025
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   ```bash
   # Copy the template
   cp config/.env.template .env
   
   # Edit .env and add your Discord bot token
   DISCORD_TOKEN=your_bot_token_here
   DEBUG=FALSE
   ```

4. **Run the bot:**
   ```bash
   python3 main.py
   ```

5. **Invite to your server:**
   Use the invite link shown in the console output with proper permissions.

## Usage

### **User Commands**
- **`/zaofractal`** - Create a new fractal voting group from your voice channel
- **`/status`** - Show current status of an active fractal group (use in fractal threads)
- **`/endgroup`** - End an active fractal group (facilitator only)

### **Admin Commands** (Requires Administrator permissions)
- **`/admin_end_fractal [thread_id]`** - Force end any fractal group
- **`/admin_list_fractals`** - List all active fractal groups with details
- **`/admin_cleanup`** - Remove old/stuck fractal groups

### **Simplified Voting Process**

1. **Join a voice channel** with 2-6 members
2. **Run `/zaofractal`** in any text channel
3. **Confirm members** with ✅ or modify with ❌
4. **Public thread created** automatically (e.g., "Fractal Group 1 - Nov 2, 2025")
5. **Vote in rounds** by clicking candidate buttons
6. **Winners announced** after each round (requires 50%+ votes)
7. **Ties broken randomly** when candidates have equal votes
8. **Final results** posted to fractal thread and general channel
9. **Thread archived** but remains accessible for reference

## Project Structure

```
fractalbotnov2025/
├── main.py                  # Bot entry point and startup
├── .env                     # Environment variables (tokens)
├── requirements.txt         # Python dependencies
├── config/
│   ├── config.py           # Configuration parameters
│   └── .env.template       # Environment template
├── cogs/
│   ├── base.py             # Base cog with utility methods
│   └── fractal/
│       ├── __init__.py     # Package initialization
│       ├── cog.py          # Slash commands and admin tools
│       ├── group.py        # FractalGroup core voting logic
│       └── views.py        # UI components and member confirmation
└── utils/
    └── logging.py          # Logging configuration
```

## Recent Improvements (v3)

### **🎯 Simplified User Flow**
- Removed complex modal forms - everything is now button-based
- Auto-generated group names eliminate user input requirements
- One-click member confirmation with modification options
- Public threads for full transparency (was private before)

### **🔧 Technical Enhancements**
- Fixed "Unknown Interaction" errors with proper View/Modal patterns
- Added tie-breaking logic with random selection
- Implemented dual results posting (thread + general channel)
- Added comprehensive admin management commands
- Flattened project structure for better organization

### **📈 Reliability Improvements**
- Better error handling for edge cases
- Automatic cleanup of stuck/archived groups
- Improved logging throughout the system
- Persistent group tracking across bot restarts

## Configuration

### **Environment Variables**
```bash
DISCORD_TOKEN=your_bot_token_here    # Required: Your Discord bot token
DEBUG=FALSE                          # Optional: Enable debug logging
```

### **Bot Permissions Required**
- Send Messages
- Embed Links
- Attach Files
- Read Messages
- Manage Messages
- Manage Threads
- Create Public Threads
- Read Message History
- Add Reactions

## Troubleshooting

### **Common Issues**
- **"Unknown Interaction" errors**: Fixed in v3 - update to latest version
- **Missing permissions**: Ensure bot has thread management permissions
- **Stuck fractals**: Use `/admin_cleanup` to remove broken groups
- **No general channel found**: Bot will use first available text channel as fallback

### **Support**
- Check console logs for detailed error information
- Use `/admin_list_fractals` to see active groups
- Restart bot if experiencing persistent issues

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### **Development Setup**
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the terms of the MIT License - see the LICENSE file for details.

---

**Version 3.0** - Simplified, streamlined, and more reliable than ever! 🚀
