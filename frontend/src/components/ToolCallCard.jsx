import React, { useState } from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Calculator, Cloud, Search, FileText, Clock, Wrench, ChevronDown, ChevronUp } from 'lucide-react';

const getToolIcon = (toolName) => {
  const name = toolName?.toLowerCase() || '';
  if (name.includes('calculator')) return Calculator;
  if (name.includes('weather')) return Cloud;
  if (name.includes('search') || name.includes('web')) return Search;
  if (name.includes('note')) return FileText;
  if (name.includes('datetime') || name.includes('time')) return Clock;
  return Wrench;
};

const ToolCallCard = ({ toolCall }) => {
  const [expanded, setExpanded] = useState(false);
  
  const IconComponent = getToolIcon(toolCall?.tool_name || toolCall?.name);
  const toolName = toolCall?.tool_name || toolCall?.name || 'Unknown Tool';
  const input = toolCall?.input || toolCall?.arguments || {};
  const output = toolCall?.output || toolCall?.result || 'No output';
  const executionTime = toolCall?.execution_time;
  const status = toolCall?.status || 'success';

  const truncateText = (text, maxLength = 100) => {
    const textStr = typeof text === 'string' ? text : JSON.stringify(text, null, 2);
    if (textStr.length <= maxLength) return textStr;
    return textStr.substring(0, maxLength) + '...';
  };

  const formatJson = (data) => {
    if (typeof data === 'string') return data;
    return JSON.stringify(data, null, 2);
  };

  return (
    <Card className="border-l-4 border-l-primary/50 hover:shadow-sm transition-shadow">
      <CardContent className="p-3">
        <div className="space-y-2">
          {/* Tool Header */}
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <IconComponent className="w-4 h-4 text-primary" />
              <span className="font-medium text-sm">{toolName}</span>
              <Badge 
                variant={status === 'success' ? 'default' : 'destructive'}
                className="text-xs"
              >
                {status}
              </Badge>
            </div>
            {executionTime && (
              <div className="flex items-center gap-1 text-xs text-muted-foreground">
                <Clock className="w-3 h-3" />
                <span>{executionTime}ms</span>
              </div>
            )}
          </div>

          {/* Input Parameters */}
          {Object.keys(input).length > 0 && (
            <div>
              <div className="text-xs font-medium text-muted-foreground mb-1">Input:</div>
              <div className="bg-muted/50 rounded p-2 text-xs font-mono">
                {expanded ? (
                  <pre className="whitespace-pre-wrap">{formatJson(input)}</pre>
                ) : (
                  <span>{truncateText(formatJson(input))}</span>
                )}
              </div>
            </div>
          )}

          {/* Output */}
          <div>
            <div className="text-xs font-medium text-muted-foreground mb-1">Output:</div>
            <div className="bg-muted/50 rounded p-2 text-xs">
              {expanded ? (
                <pre className="whitespace-pre-wrap font-mono">{formatJson(output)}</pre>
              ) : (
                <span>{truncateText(output)}</span>
              )}
            </div>
          </div>

          {/* Expand/Collapse Button */}
          {(formatJson(input).length > 100 || formatJson(output).length > 100) && (
            <Button
              variant="ghost"
              size="sm"
              onClick={() => setExpanded(!expanded)}
              className="w-full h-7 text-xs"
            >
              {expanded ? (
                <>
                  <ChevronUp className="w-3 h-3 mr-1" />
                  Show Less
                </>
              ) : (
                <>
                  <ChevronDown className="w-3 h-3 mr-1" />
                  Show More
                </>
              )}
            </Button>
          )}
        </div>
      </CardContent>
    </Card>
  );
};

export default ToolCallCard;