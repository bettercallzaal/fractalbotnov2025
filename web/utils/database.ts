import { neon } from '@neondatabase/serverless';
import { drizzle } from 'drizzle-orm/neon-http';
import * as schema from './schema';

console.log('🔍 Database Configuration:', {
  hasDatabaseUrl: !!process.env.DATABASE_URL,
  databaseUrlPrefix: process.env.DATABASE_URL?.substring(0, 20) + '...',
  timestamp: new Date().toISOString()
});

if (!process.env.DATABASE_URL) {
  throw new Error('DATABASE_URL is not set');
}

const sql = neon(process.env.DATABASE_URL!);
export const db = drizzle(sql as any, { schema });

console.log('✅ Database connection initialized');

// Database connection utility
export async function connectDB() {
  try {
    // Test the connection
    await sql`SELECT 1`;
    console.log('✅ Database connected successfully');
    return true;
  } catch (error) {
    console.error('❌ Database connection failed:', error);
    return false;
  }
}
