import React, { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { Copy, Check, Clock, User, Bot } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import ToolCallCard from './ToolCallCard';

const MessageBubble = ({ message, isUser, timestamp, executionTime, toolCalls = [] }) => {
  const [copied, setCopied] = useState(false);

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(message);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      console.error('Failed to copy text:', err);
    }
  };

  const formatTime = (time) => {
    if (!time) return '';
    return new Date(time).toLocaleTimeString([], { 
      hour: '2-digit', 
      minute: '2-digit' 
    });
  };

  return (
    <div className={`mb-6 ${isUser ? 'flex justify-end' : 'flex justify-start'}`}>
      <div className={`max-w-[85%] ${isUser ? 'order-2' : 'order-1'}`}>
        {/* Message Header */}
        <div className={`flex items-center gap-2 mb-2 ${isUser ? 'justify-end' : 'justify-start'}`}>
          <div className="flex items-center gap-1 text-xs text-muted-foreground">
            {isUser ? (
              <>
                <User className="w-3 h-3" />
                <span>You</span>
              </>
            ) : (
              <>
                <Bot className="w-3 h-3" />
                <span>AI Agent</span>
              </>
            )}
            {timestamp && (
              <>
                <span>•</span>
                <span>{formatTime(timestamp)}</span>
              </>
            )}
            {executionTime && !isUser && (
              <>
                <span>•</span>
                <Clock className="w-3 h-3" />
                <span>{executionTime}ms</span>
              </>
            )}
          </div>
        </div>

        {/* Message Bubble */}
        <div className={`relative group rounded-lg p-4 ${
          isUser 
            ? 'bg-gradient-to-r from-primary to-primary/90 text-primary-foreground' 
            : 'bg-muted text-muted-foreground border'
        }`}>
          {/* Message Content */}
          <div className="prose prose-sm max-w-none">
            {isUser ? (
              <p className="whitespace-pre-wrap m-0">{message}</p>
            ) : (
              <ReactMarkdown 
                remarkPlugins={[remarkGfm]}
                components={{
                  // Custom components for better styling
                  p: ({ children }) => <p className="mb-2 last:mb-0">{children}</p>,
                  code: ({ inline, children }) => 
                    inline ? (
                      <code className="bg-background/20 px-1 py-0.5 rounded text-sm">
                        {children}
                      </code>
                    ) : (
                      <pre className="bg-background/20 p-2 rounded text-sm overflow-x-auto">
                        <code>{children}</code>
                      </pre>
                    ),
                  ul: ({ children }) => <ul className="list-disc list-inside mb-2">{children}</ul>,
                  ol: ({ children }) => <ol className="list-decimal list-inside mb-2">{children}</ol>,
                  li: ({ children }) => <li className="mb-1">{children}</li>,
                  a: ({ href, children }) => (
                    <a 
                      href={href} 
                      target="_blank" 
                      rel="noopener noreferrer"
                      className="underline hover:no-underline"
                    >
                      {children}
                    </a>
                  ),
                }}
              >
                {message}
              </ReactMarkdown>
            )}
          </div>

          {/* Copy Button */}
          {!isUser && (
            <Button
              variant="ghost"
              size="sm"
              onClick={handleCopy}
              className="absolute top-2 right-2 opacity-0 group-hover:opacity-100 transition-opacity h-6 w-6 p-0"
            >
              {copied ? (
                <Check className="w-3 h-3" />
              ) : (
                <Copy className="w-3 h-3" />
              )}
            </Button>
          )}
        </div>

        {/* Tool Calls */}
        {toolCalls && toolCalls.length > 0 && (
          <div className="mt-3 space-y-2">
            <div className="flex items-center gap-2">
              <Badge variant="outline" className="text-xs">
                Tools Used ({toolCalls.length})
              </Badge>
            </div>
            <div className="space-y-2">
              {toolCalls.map((toolCall, index) => (
                <ToolCallCard key={index} toolCall={toolCall} />
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default MessageBubble;