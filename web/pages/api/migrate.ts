import { NextApiRequest, NextApiResponse } from 'next';
import { neon } from '@neondatabase/serverless';

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  console.log('🔄 Starting database migration...');
  
  try {
    const sql = neon(process.env.DATABASE_URL!);

    // Create users table
    await sql`
      CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        discord_id VARCHAR(255) UNIQUE NOT NULL,
        username VARCHAR(255) NOT NULL,
        display_name VARCHAR(255),
        avatar_url TEXT,
        wallet_address VARCHAR(255),
        total_fractals INTEGER DEFAULT 0,
        total_wins INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
      )
    `;
    console.log('✅ Users table created');

    // Create fractals table
    await sql`
      CREATE TABLE IF NOT EXISTS fractals (
        id SERIAL PRIMARY KEY,
        thread_id VARCHAR(255) UNIQUE NOT NULL,
        name VARCHAR(255) NOT NULL,
        guild_id VARCHAR(255) NOT NULL,
        facilitator_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
        status VARCHAR(50) DEFAULT 'active',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        completed_at TIMESTAMP
      )
    `;
    console.log('✅ Fractals table created');

    // Create participants table
    await sql`
      CREATE TABLE IF NOT EXISTS participants (
        id SERIAL PRIMARY KEY,
        fractal_id INTEGER REFERENCES fractals(id) ON DELETE CASCADE,
        user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
        level INTEGER NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(fractal_id, user_id, level)
      )
    `;
    console.log('✅ Participants table created');

    // Create voting_rounds table
    await sql`
      CREATE TABLE IF NOT EXISTS voting_rounds (
        id SERIAL PRIMARY KEY,
        fractal_id INTEGER REFERENCES fractals(id) ON DELETE CASCADE,
        level INTEGER NOT NULL,
        winner_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
        total_votes INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        completed_at TIMESTAMP,
        UNIQUE(fractal_id, level)
      )
    `;
    console.log('✅ Voting rounds table created');

    // Create votes table
    await sql`
      CREATE TABLE IF NOT EXISTS votes (
        id SERIAL PRIMARY KEY,
        voting_round_id INTEGER REFERENCES voting_rounds(id) ON DELETE CASCADE,
        voter_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
        candidate_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(voting_round_id, voter_id)
      )
    `;
    console.log('✅ Votes table created');

    // Test the connection
    const userCount = await sql`SELECT COUNT(*) as count FROM users`;
    console.log(`📊 Current users in database: ${userCount[0].count}`);

    res.status(200).json({
      success: true,
      message: 'Database migration completed successfully!',
      userCount: userCount[0].count
    });
    
  } catch (error) {
    console.error('❌ Migration failed:', error);
    res.status(500).json({
      success: false,
      error: 'Migration failed',
      details: (error as Error).message
    });
  }
}
