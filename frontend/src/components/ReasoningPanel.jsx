import React, { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Separator } from '@/components/ui/separator';
import { ChevronDown, ChevronUp, Brain, Eye, Lightbulb, Zap, ChevronLeft, ChevronRight, X } from 'lucide-react';

const ReasoningPanel = ({ reasoningSteps = [], isVisible = true, onToggleVisibility, isMobile = false }) => {
  const [expandedSteps, setExpandedSteps] = useState(new Set());

  const toggleStep = (stepIndex) => {
    const newExpanded = new Set(expandedSteps);
    if (newExpanded.has(stepIndex)) {
      newExpanded.delete(stepIndex);
    } else {
      newExpanded.add(stepIndex);
    }
    setExpandedSteps(newExpanded);
  };

  const getStepIcon = (step) => {
    const content = step?.thought?.toLowerCase() || step?.action?.toLowerCase() || '';
    if (content.includes('think') || content.includes('consider')) return Brain;
    if (content.includes('observe') || content.includes('see') || content.includes('result')) return Eye;
    if (content.includes('decide') || content.includes('plan')) return Lightbulb;
    return Zap;
  };

  const formatStepContent = (content) => {
    if (!content) return 'No content';
    const maxLength = isMobile ? 150 : 200;
    return content.length > maxLength ? content.substring(0, maxLength) + '...' : content;
  };

  if (!isVisible) {
    return (
      <div className="w-8 border-l bg-background flex flex-col">
        <Button
          variant="ghost"
          size="sm"
          onClick={onToggleVisibility}
          className="h-12 w-full rounded-none border-b"
          title="Show reasoning panel"
        >
          <ChevronLeft className="w-4 h-4" />
        </Button>
      </div>
    );
  }

  const panelClasses = isMobile 
    ? "flex-1 bg-background flex flex-col" 
    : "w-1/3 min-w-[300px] border-l bg-background flex flex-col";

  return (
    <div className={panelClasses}>
      {/* Header */}
      <div className="p-4 border-b">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Brain className="w-4 h-4 text-primary" />
            <h3 className="font-semibold">Reasoning Steps</h3>
            {reasoningSteps.length > 0 && (
              <Badge variant="secondary" className="text-xs">
                {reasoningSteps.length}
              </Badge>
            )}
          </div>
          <Button
            variant="ghost"
            size="sm"
            onClick={onToggleVisibility}
            className="h-8 w-8 p-0"
            title={isMobile ? "Close reasoning" : "Hide reasoning panel"}
          >
            {isMobile ? (
              <X className="w-4 h-4" />
            ) : (
              <ChevronRight className="w-4 h-4" />
            )}
          </Button>
        </div>
      </div>

      {/* Content */}
      <ScrollArea className="flex-1">
        <div className="p-4">
          {reasoningSteps.length === 0 ? (
            <div className="text-center py-8">
              <Brain className="w-12 h-12 text-muted-foreground mx-auto mb-4" />
              <p className="text-sm text-muted-foreground mb-2">
                No reasoning steps yet
              </p>
              <p className="text-xs text-muted-foreground">
                Enable "Show reasoning steps" and ask a question to see how the agent thinks
              </p>
            </div>
          ) : (
            <div className="space-y-3">
              {reasoningSteps.map((step, index) => {
                const isExpanded = expandedSteps.has(index);
                const StepIcon = getStepIcon(step);
                
                return (
                  <Card key={index} className="border-l-4 border-l-primary/30">
                    <CardHeader className="pb-2">
                      <CardTitle className="flex items-center justify-between text-sm">
                        <div className="flex items-center gap-2">
                          <StepIcon className="w-4 h-4 text-primary" />
                          <span>Step {index + 1}</span>
                          <Badge variant="outline" className="text-xs">
                            {step.type || 'thought'}
                          </Badge>
                        </div>
                        {(step.thought?.length > (isMobile ? 150 : 200) || 
                          step.action?.length > (isMobile ? 150 : 200) || 
                          step.observation?.length > (isMobile ? 150 : 200)) && (
                          <Button
                            variant="ghost"
                            size="sm"
                            onClick={() => toggleStep(index)}
                            className="h-6 w-6 p-0"
                          >
                            {isExpanded ? (
                              <ChevronUp className="w-3 h-3" />
                            ) : (
                              <ChevronDown className="w-3 h-3" />
                            )}
                          </Button>
                        )}
                      </CardTitle>
                    </CardHeader>
                    <CardContent className="pt-0 space-y-3">
                      {/* Thought */}
                      {step.thought && (
                        <div>
                          <div className="text-xs font-medium text-muted-foreground mb-1">
                            💭 Thought:
                          </div>
                          <div className="text-sm bg-muted/50 rounded p-2">
                            {isExpanded ? step.thought : formatStepContent(step.thought)}
                          </div>
                        </div>
                      )}

                      {/* Action */}
                      {step.action && (
                        <div>
                          <div className="text-xs font-medium text-muted-foreground mb-1">
                            ⚡ Action:
                          </div>
                          <div className="text-sm bg-primary/10 rounded p-2">
                            {isExpanded ? step.action : formatStepContent(step.action)}
                          </div>
                        </div>
                      )}

                      {/* Observation */}
                      {step.observation && (
                        <div>
                          <div className="text-xs font-medium text-muted-foreground mb-1">
                            👁️ Observation:
                          </div>
                          <div className="text-sm bg-green-50 dark:bg-green-950/20 rounded p-2">
                            {isExpanded ? step.observation : formatStepContent(step.observation)}
                          </div>
                        </div>
                      )}

                      {/* Tool Call Info */}
                      {step.tool_name && (
                        <div className="flex items-center gap-2 text-xs text-muted-foreground">
                          <Zap className="w-3 h-3" />
                          <span>Used tool: {step.tool_name}</span>
                        </div>
                      )}
                    </CardContent>
                  </Card>
                );
              })}
            </div>
          )}
        </div>
      </ScrollArea>
    </div>
  );
};

export default ReasoningPanel;