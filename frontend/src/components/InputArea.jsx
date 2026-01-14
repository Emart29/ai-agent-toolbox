import React, { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { Checkbox } from '@/components/ui/checkbox';
import { Card, CardContent } from '@/components/ui/card';
import { Send, Lightbulb, X } from 'lucide-react';

const exampleQueries = [
  {
    text: "What's the weather in Lagos?",
    description: "Get current weather information"
  },
  {
    text: "Calculate 25% of 80 and convert the result to euros",
    description: "Multi-tool calculation"
  },
  {
    text: "Search for latest AI developments and summarize",
    description: "Web search and analysis"
  },
  {
    text: "What time is it in New York and Tokyo?",
    description: "DateTime utilities"
  },
  {
    text: "Save a note: Meeting with team tomorrow at 3pm",
    description: "Notes management"
  }
];

const InputArea = ({ onSend, isLoading }) => {
  const [input, setInput] = useState('');
  const [showReasoning, setShowReasoning] = useState(true);
  const [showExamples, setShowExamples] = useState(false);

  const handleSend = () => {
    if (input.trim() && !isLoading) {
      onSend(input.trim(), showReasoning);
      setInput('');
      setShowExamples(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleExampleClick = (exampleText) => {
    setInput(exampleText);
    setShowExamples(false);
  };

  const adjustTextareaHeight = (e) => {
    const textarea = e.target;
    textarea.style.height = 'auto';
    const newHeight = Math.min(textarea.scrollHeight, 120); // Max 5 lines
    textarea.style.height = newHeight + 'px';
  };

  return (
    <div className="border-t bg-background">
      {/* Example Queries */}
      {showExamples && (
        <div className="border-b p-4">
          <div className="flex items-center justify-between mb-3">
            <div className="flex items-center gap-2">
              <Lightbulb className="w-4 h-4 text-primary" />
              <span className="font-medium text-sm">Example Queries</span>
            </div>
            <Button
              variant="ghost"
              size="sm"
              onClick={() => setShowExamples(false)}
              className="h-6 w-6 p-0"
            >
              <X className="w-4 h-4" />
            </Button>
          </div>
          <div className="grid gap-2 sm:grid-cols-2 lg:grid-cols-3">
            {exampleQueries.map((example, index) => (
              <Card 
                key={index} 
                className="cursor-pointer hover:shadow-md transition-shadow"
                onClick={() => handleExampleClick(example.text)}
              >
                <CardContent className="p-3">
                  <p className="text-sm font-medium mb-1">{example.text}</p>
                  <p className="text-xs text-muted-foreground">{example.description}</p>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      )}

      {/* Input Area */}
      <div className="p-4">
        <div className="flex items-end gap-3">
          <div className="flex-1">
            <Textarea
              value={input}
              onChange={(e) => {
                setInput(e.target.value);
                adjustTextareaHeight(e);
              }}
              onKeyDown={handleKeyDown}
              placeholder="Ask me anything... (Shift+Enter for new line)"
              className="min-h-[60px] resize-none"
              maxLength={1000}
              disabled={isLoading}
              style={{ height: '60px' }}
            />
          </div>
          <Button 
            onClick={handleSend} 
            disabled={!input.trim() || isLoading}
            className="h-[60px] px-6"
          >
            {isLoading ? (
              <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
            ) : (
              <Send className="w-4 h-4" />
            )}
          </Button>
        </div>

        {/* Controls */}
        <div className="flex items-center justify-between mt-3">
          <div className="flex items-center gap-4">
            <div className="flex items-center gap-2">
              <Checkbox
                id="reasoning"
                checked={showReasoning}
                onCheckedChange={setShowReasoning}
                disabled={isLoading}
              />
              <label htmlFor="reasoning" className="text-sm cursor-pointer">
                Show reasoning steps
              </label>
            </div>

            <Button
              variant="ghost"
              size="sm"
              onClick={() => setShowExamples(!showExamples)}
              disabled={isLoading}
              className="text-xs"
            >
              <Lightbulb className="w-3 h-3 mr-1" />
              Examples
            </Button>
          </div>

          <div className="flex items-center gap-2 text-xs text-muted-foreground">
            <span>{input.length}/1000</span>
            {input.length > 900 && (
              <span className="text-yellow-600">
                ({1000 - input.length} remaining)
              </span>
            )}
          </div>
        </div>

        {/* Keyboard Hint */}
        <div className="mt-2 text-xs text-muted-foreground">
          Press Enter to send • Shift+Enter for new line
        </div>
      </div>
    </div>
  );
};

export default InputArea;