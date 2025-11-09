import { SessionProvider } from 'next-auth/react';
import type { AppProps } from 'next/app';
import '../styles/globals.css';

export default function App({
  Component,
  pageProps: { session, ...pageProps },
}: AppProps) {
  console.log('🔍 App Component Debug:', {
    hasSession: !!session,
    sessionKeys: session ? Object.keys(session) : null,
    componentName: Component.name,
    timestamp: new Date().toISOString()
  });

  return (
    <SessionProvider session={session}>
      <Component {...pageProps} />
    </SessionProvider>
  );
}
