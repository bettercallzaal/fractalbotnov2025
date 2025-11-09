import { NextApiRequest, NextApiResponse } from 'next';

export default function handler(req: NextApiRequest, res: NextApiResponse) {
  console.log('🔍 Health Check API called:', {
    method: req.method,
    url: req.url,
    timestamp: new Date().toISOString(),
    headers: Object.keys(req.headers)
  });

  // Check environment variables
  const envCheck = {
    hasDiscordClientId: !!process.env.DISCORD_CLIENT_ID,
    hasDiscordClientSecret: !!process.env.DISCORD_CLIENT_SECRET,
    hasNextAuthUrl: !!process.env.NEXTAUTH_URL,
    hasNextAuthSecret: !!process.env.NEXTAUTH_SECRET,
    hasDatabaseUrl: !!process.env.DATABASE_URL,
    hasWebhookSecret: !!process.env.WEBHOOK_SECRET,
    nodeEnv: process.env.NODE_ENV,
  };

  console.log('🔍 Environment Variables Check:', envCheck);

  res.status(200).json({
    status: 'healthy',
    timestamp: new Date().toISOString(),
    environment: envCheck,
    message: 'FractalBot API is running'
  });
}
