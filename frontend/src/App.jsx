import React from 'react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import Header from './components/Header';
import ChatInterface from './components/ChatInterface';

// Create a client
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 1,
      refetchOnWindowFocus: false,
    },
  },
});

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <div className="min-h-screen bg-background flex flex-col">
        <Header />
        <ChatInterface />
      </div>
    </QueryClientProvider>
  );
}

export default App;
