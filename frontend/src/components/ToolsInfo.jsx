import React from 'react';
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Calculator, Cloud, Search, FileText, Clock, Wrench } from 'lucide-react';

const getToolIcon = (toolName) => {
  const name = toolName?.toLowerCase() || '';
  if (name.includes('calculator')) return Calculator;
  if (name.includes('weather')) return Cloud;
  if (name.includes('search') || name.includes('web')) return Search;
  if (name.includes('note')) return FileText;
  if (name.includes('datetime') || name.includes('time')) return Clock;
  return Wrench;
};

const getToolDescription = (toolName) => {
  const name = toolName?.toLowerCase() || '';
  if (name.includes('calculator')) return 'Perform mathematical calculations and conversions';
  if (name.includes('weather')) return 'Get current weather information for any location';
  if (name.includes('search') || name.includes('web')) return 'Search the web for current information';
  if (name.includes('note')) return 'Save and retrieve notes and reminders';
  if (name.includes('datetime') || name.includes('time')) return 'Get current time and date information';
  return 'Utility tool for various tasks';
};

const getExampleUsage = (toolName) => {
  const name = toolName?.toLowerCase() || '';
  if (name.includes('calculator')) return '"Calculate 25% of 80"';
  if (name.includes('weather')) return '"What\'s the weather in Lagos?"';
  if (name.includes('search') || name.includes('web')) return '"Search for latest AI news"';
  if (name.includes('note')) return '"Save a note: Meeting at 3pm"';
  if (name.includes('datetime') || name.includes('time')) return '"What time is it in New York?"';
  return '"Use this tool for specific tasks"';
};

const ToolsInfo = ({ open, onOpenChange, tools = [] }) => {
  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-4xl max-h-[80vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-2">
            <Wrench className="w-5 h-5" />
            Available Tools ({tools.length})
          </DialogTitle>
        </DialogHeader>
        
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {tools.length > 0 ? (
            tools.map((tool, index) => {
              const IconComponent = getToolIcon(tool.name);
              return (
                <Card key={index} className="hover:shadow-md transition-shadow">
                  <CardHeader className="pb-3">
                    <CardTitle className="flex items-center gap-2 text-base">
                      <IconComponent className="w-4 h-4 text-primary" />
                      {tool.name || `Tool ${index + 1}`}
                    </CardTitle>
                    <CardDescription className="text-sm">
                      {tool.description || getToolDescription(tool.name)}
                    </CardDescription>
                  </CardHeader>
                  <CardContent className="pt-0">
                    <div className="space-y-2">
                      <div>
                        <Badge variant="outline" className="text-xs">
                          Example
                        </Badge>
                        <p className="text-xs text-muted-foreground mt-1">
                          {getExampleUsage(tool.name)}
                        </p>
                      </div>
                      {tool.parameters && (
                        <div>
                          <Badge variant="secondary" className="text-xs">
                            Parameters
                          </Badge>
                          <p className="text-xs text-muted-foreground mt-1">
                            {Object.keys(tool.parameters).join(', ') || 'Dynamic'}
                          </p>
                        </div>
                      )}
                    </div>
                  </CardContent>
                </Card>
              );
            })
          ) : (
            <div className="col-span-full text-center py-8">
              <Wrench className="w-12 h-12 text-muted-foreground mx-auto mb-4" />
              <p className="text-muted-foreground">
                No tools available or still loading...
              </p>
            </div>
          )}
        </div>

        {tools.length > 0 && (
          <div className="mt-6 p-4 bg-muted/50 rounded-lg">
            <h4 className="font-medium mb-2">How to use tools:</h4>
            <ul className="text-sm text-muted-foreground space-y-1">
              <li>• Simply ask questions that require these tools</li>
              <li>• The agent will automatically choose the right tools</li>
              <li>• Enable "Show reasoning steps" to see tool selection process</li>
              <li>• Tool calls and results will be displayed in the chat</li>
            </ul>
          </div>
        )}
      </DialogContent>
    </Dialog>
  );
};

export default ToolsInfo;