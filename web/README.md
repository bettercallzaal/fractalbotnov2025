# ZAO Fractal Web Dashboard

A modern web interface for the ZAO Fractal Voting System, built with Next.js and deployed on Vercel.

## 🌟 Features

### **🔐 Authentication**
- Discord OAuth integration
- Automatic user profile creation
- Secure session management

### **📊 Dashboard**
- Real-time fractal monitoring
- User statistics and participation history
- Live voting progress tracking
- Beautiful, responsive UI

### **💰 Wallet Integration**
- Connect crypto wallets (MetaMask, WalletConnect)
- Track participation for future rewards
- User profile with wallet addresses

### **📱 Mobile Responsive**
- Works perfectly on all devices
- Touch-friendly interface
- Progressive Web App capabilities

## 🚀 Quick Start

### **1. Environment Setup**
```bash
# Copy environment template
cp .env.example .env.local

# Fill in your values:
DATABASE_URL="postgresql://..."           # Neon database URL
DISCORD_CLIENT_ID="..."                  # Discord app client ID
DISCORD_CLIENT_SECRET="..."              # Discord app secret
NEXTAUTH_URL="https://your-app.vercel.app"
NEXTAUTH_SECRET="random-secret-key"
WEBHOOK_SECRET="secret-for-bot-webhook"
```

### **2. Database Setup**
```bash
# Install dependencies
npm install

# Generate database schema
npm run db:generate

# Push schema to Neon
npm run db:push
```

### **3. Development**
```bash
# Start development server
npm run dev

# Open http://localhost:3000
```

### **4. Deploy to Vercel**
```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel --prod
```

## 📁 Project Structure

```
web/
├── pages/
│   ├── api/
│   │   ├── auth/[...nextauth].ts    # Discord OAuth
│   │   ├── fractals/               # Fractal CRUD API
│   │   └── webhook.ts              # Discord bot integration
│   ├── index.tsx                   # Main dashboard
│   └── _app.tsx                    # App configuration
├── components/
│   └── ui/                         # Reusable UI components
├── utils/
│   ├── database.ts                 # Database connection
│   ├── schema.ts                   # Database schema
│   └── cn.ts                       # Utility functions
└── styles/
    └── globals.css                 # Global styles
```

## 🗄️ Database Schema

### **Users Table**
- Discord user information
- Wallet addresses and types
- Participation statistics
- Achievement tracking

### **Fractals Table**
- Fractal session details
- Status and progress tracking
- Facilitator and participant info

### **Voting System**
- Detailed vote recording
- Round-by-round results
- Historical data for analysis

## 🔗 API Endpoints

### **Authentication**
- `GET /api/auth/signin` - Discord OAuth login
- `GET /api/auth/signout` - User logout

### **Fractals**
- `GET /api/fractals` - List all fractals
- `POST /api/fractals` - Create new fractal
- `GET /api/fractals/[id]` - Get fractal details

### **Webhook**
- `POST /api/webhook` - Discord bot integration

## 🎨 UI Components

Built with **Radix UI** and **Tailwind CSS**:
- Beautiful, accessible components
- Dark/light mode support
- Consistent design system
- Mobile-first responsive design

## 🔧 Configuration

### **Discord App Setup**
1. Create Discord application at https://discord.com/developers/applications
2. Add OAuth2 redirect: `https://your-app.vercel.app/api/auth/callback/discord`
3. Copy Client ID and Secret to environment variables

### **Neon Database Setup**
1. Create account at https://neon.tech
2. Create new database
3. Copy connection string to `DATABASE_URL`

### **Vercel Deployment**
1. Connect GitHub repository
2. Set environment variables in Vercel dashboard
3. Deploy automatically on push

## 🚀 Discord Bot Integration

The web app receives real-time updates from the Discord bot via webhooks:

- **Fractal Started** - New fractal creation
- **Vote Cast** - Real-time vote tracking
- **Round Complete** - Level progression
- **Fractal Complete** - Final results

## 📊 Analytics & Monitoring

### **User Analytics**
- Participation history
- Win/loss ratios
- Voting patterns
- Achievement progress

### **Server Analytics**
- Active fractal counts
- Participation trends
- Popular voting times
- Community engagement metrics

## 🔒 Security

- **OAuth Authentication** - Secure Discord login
- **JWT Sessions** - Encrypted session management
- **Webhook Verification** - Signed bot communications
- **Environment Variables** - Secure credential storage

## 🎯 Future Features

- **Real-time Updates** - WebSocket integration
- **Mobile App** - React Native companion
- **NFT Integration** - Fractal completion badges
- **Governance Tools** - Community decision making
- **Analytics Dashboard** - Advanced metrics

## 📝 License

MIT License - see LICENSE file for details.

---

**Built with ❤️ for the ZAO community**
