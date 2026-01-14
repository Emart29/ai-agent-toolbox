import React, { useState, useRef, useEffect } from 'react';
import { useMutation } from '@tanstack/react-query';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Button } from '@/components/ui/button';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Trash2, AlertCircle, Brain } from 'lucide-react';
import { agentAPI } from '@/services/api';
import MessageBubble from './MessageBubble';
import InputArea from './InputArea';
import ReasoningPanel from './ReasoningPanel';

const ChatInterface = () => {
  const [messages, setMessages] = useState([]);
  const [conversationId, setConversationId] = useState(null);
  const [currentReasoning, setCurrentReasoning] = useState([]);
  const [showReasoningPanel, setShowReasoningPanel] = useState(true);
  const [isMobile, setIsMobile] = useState(false);
  const scrollAreaRef = useRef(null);
  const messagesEndRef = useRef(null);

  // Check if mobile on mount and resize
  useEffect(() => {
    const checkMobile = () => {
      setIsMobile(window.innerWidth < 768);
      // On mobile, hide reasoning panel by default
      if (window.innerWidth < 768) {
        setShowReasoningPanel(false);
      }
    };

    checkMobile();
    window.addEventListener('resize', checkMobile);
    return () => window.removeEventListener('resize', checkMobile);
  }, []);

  // Auto-scroll to bottom when new messages arrive
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Agent query mutation
  const agentMutation = useMutation({
    mutationFn: agentAPI.query,
    onSuccess: (response) => {
      const data = response.data;
      
      // Add agent response message
      const agentMessage = {
        id: Date.now() + 1,
        content: data.answer,
        isUser: false,
        timestamp: new Date().toISOString(),
        executionTime: data.total_execution_time,
        toolCalls: data.tool_calls || [],
      };

      setMessages(prev => [...prev, agentMessage]);
      
      // Update conversation ID
      if (data.conversation_id) {
        setConversationId(data.conversation_id);
      }

      // Update reasoning steps
      if (data.reasoning_steps) {
        setCurrentReasoning(data.reasoning_steps);
      }
    },
    onError: (error) => {
      console.error('Agent query failed:', error);
      
      // Add error message
      const errorMessage = {
        id: Date.now() + 1,
        content: `Sorry, I encountered an error: ${error.response?.data?.detail || error.message}`,
        isUser: false,
        timestamp: new Date().toISOString(),
        isError: true,
      };

      setMessages(prev => [...prev, errorMessage]);
    },
  });

  const handleSendMessage = (message, includeReasoning) => {
    // Add user message immediately
    const userMessage = {
      id: Date.now(),
      content: message,
      isUser: true,
      timestamp: new Date().toISOString(),
    };

    setMessages(prev => [...prev, userMessage]);

    // Clear current reasoning
    setCurrentReasoning([]);

    // Send to agent
    agentMutation.mutate({
      query: message,
      conversation_id: conversationId,
      include_reasoning: includeReasoning,
    });
  };

  const handleClearConversation = () => {
    setMessages([]);
    setConversationId(null);
    setCurrentReasoning([]);
  };

  const toggleReasoningPanel = () => {
    setShowReasoningPanel(!showReasoningPanel);
  };

  return (
    <div className="flex-1 flex flex-col md:flex-row overflow-hidden">
      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col min-h-0">
        {/* Messages Area */}
        <div className="flex-1 relative">
          <ScrollArea className="h-full" ref={scrollAreaRef}>
            <div className="p-4 pb-0">
              {/* Empty State */}
              {messages.length === 0 && (
                <div className="text-center py-8 md:py-12">
                  <div className="text-4xl md:text-6xl mb-4">🤖</div>
                  <h2 className="text-lg md:text-xl font-semibold mb-2">
                    Welcome to AI Agent Toolbox
                  </h2>
                  <p className="text-muted-foreground mb-6 max-w-md mx-auto text-sm md:text-base">
                    I'm an AI agent with access to multiple tools. I can help you with calculations, 
                    weather information, web searches, notes, and time queries. Ask me anything!
                  </p>
                  <div className="flex flex-col sm:flex-row flex-wrap gap-2 justify-center">
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => handleSendMessage("What tools do you have access to?", true)}
                    >
                      What tools do you have?
                    </Button>
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => handleSendMessage("What's the weather like today?", true)}
                    >
                      Check weather
                    </Button>
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => handleSendMessage("Calculate 15% tip on $45", true)}
                    >
                      Do a calculation
                    </Button>
                  </div>
                </div>
              )}

              {/* Messages */}
              {messages.map((message) => (
                <MessageBubble
                  key={message.id}
                  message={message.content}
                  isUser={message.isUser}
                  timestamp={message.timestamp}
                  executionTime={message.executionTime}
                  toolCalls={message.toolCalls}
                />
              ))}

              {/* Loading Indicator */}
              {agentMutation.isPending && (
                <div className="flex justify-start mb-6">
                  <div className="max-w-[85%]">
                    <div className="flex items-center gap-2 mb-2">
                      <div className="text-xs text-muted-foreground">AI Agent is thinking...</div>
                    </div>
                    <div className="bg-muted rounded-lg p-4 border">
                      <div className="flex items-center gap-2">
                        <div className="w-2 h-2 bg-primary rounded-full animate-bounce" />
                        <div className="w-2 h-2 bg-primary rounded-full animate-bounce" style={{ animationDelay: '0.1s' }} />
                        <div className="w-2 h-2 bg-primary rounded-full animate-bounce" style={{ animationDelay: '0.2s' }} />
                        <span className="text-sm text-muted-foreground ml-2">Processing your request...</span>
                      </div>
                    </div>
                  </div>
                </div>
              )}

              {/* Error Alert */}
              {agentMutation.isError && (
                <Alert className="mb-4">
                  <AlertCircle className="h-4 w-4" />
                  <AlertDescription>
                    Failed to send message. Please check your connection and try again.
                  </AlertDescription>
                </Alert>
              )}

              <div ref={messagesEndRef} />
            </div>
          </ScrollArea>

          {/* Action Buttons */}
          <div className="absolute top-4 right-4 flex gap-2">
            {/* Mobile Reasoning Toggle */}
            {isMobile && currentReasoning.length > 0 && (
              <Button
                variant="outline"
                size="sm"
                onClick={toggleReasoningPanel}
                className="bg-background/80 backdrop-blur-sm"
              >
                <Brain className="w-4 h-4 mr-2" />
                Reasoning
              </Button>
            )}
            
            {/* Clear Conversation Button */}
            {messages.length > 0 && (
              <Button
                variant="outline"
                size="sm"
                onClick={handleClearConversation}
                className="bg-background/80 backdrop-blur-sm"
              >
                <Trash2 className="w-4 h-4 mr-2" />
                <span className="hidden sm:inline">Clear</span>
              </Button>
            )}
          </div>
        </div>

        {/* Input Area */}
        <InputArea
          onSend={handleSendMessage}
          isLoading={agentMutation.isPending}
        />
      </div>

      {/* Reasoning Panel - Desktop: Side panel, Mobile: Bottom sheet */}
      {isMobile ? (
        // Mobile: Bottom sheet
        showReasoningPanel && currentReasoning.length > 0 && (
          <div className="border-t bg-background max-h-[40vh] flex flex-col">
            <ReasoningPanel
              reasoningSteps={currentReasoning}
              isVisible={true}
              onToggleVisibility={toggleReasoningPanel}
              isMobile={true}
            />
          </div>
        )
      ) : (
        // Desktop: Side panel
        <ReasoningPanel
          reasoningSteps={currentReasoning}
          isVisible={showReasoningPanel}
          onToggleVisibility={toggleReasoningPanel}
          isMobile={false}
        />
      )}
    </div>
  );
};

export default ChatInterface;