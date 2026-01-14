import React, { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { RefreshCw, Info, Wrench } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { systemAPI, agentAPI } from '@/services/api';
import ToolsInfo from './ToolsInfo';

const Header = () => {
  const [showToolsInfo, setShowToolsInfo] = useState(false);

  // Health check query
  const { data: healthData, refetch: refetchHealth, isLoading: healthLoading } = useQuery({
    queryKey: ['system-health'],
    queryFn: systemAPI.getHealth,
    refetchInterval: 30000, // Refetch every 30 seconds
    retry: 1,
  });

  // Tools query
  const { data: toolsData } = useQuery({
    queryKey: ['agent-tools'],
    queryFn: agentAPI.getTools,
    retry: 1,
  });

  const getStatusColor = (status) => {
    switch (status?.toLowerCase()) {
      case 'healthy': return 'bg-green-500';
      case 'degraded': return 'bg-yellow-500';
      case 'unhealthy': return 'bg-red-500';
      default: return 'bg-gray-500';
    }
  };

  const getStatusText = (status) => {
    return status || 'Unknown';
  };

  const health = healthData?.data;
  const tools = toolsData?.data;

  return (
    <>
      <header className="border-b bg-background shadow-sm">
        <div className="container mx-auto px-4 py-3">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <h1 className="text-xl font-bold">🤖 AI Agent Toolbox</h1>
              
              {/* System Status */}
              <div className="flex items-center gap-2">
                <div className={`w-2 h-2 rounded-full ${getStatusColor(health?.status)}`} />
                <span className="text-sm text-muted-foreground">
                  {getStatusText(health?.status)}
                </span>
              </div>
            </div>

            <div className="flex items-center gap-3">
              {/* Model Info */}
              {health?.model_used && (
                <Badge variant="secondary" className="hidden sm:flex">
                  {health.model_used}
                </Badge>
              )}

              {/* Tools Count */}
              <Button
                variant="outline"
                size="sm"
                onClick={() => setShowToolsInfo(true)}
                className="flex items-center gap-2"
              >
                <Wrench className="w-4 h-4" />
                <span className="hidden sm:inline">
                  {tools?.length || 0} Tools
                </span>
                <span className="sm:hidden">{tools?.length || 0}</span>
              </Button>

              {/* Refresh Button */}
              <Button
                variant="outline"
                size="sm"
                onClick={() => refetchHealth()}
                disabled={healthLoading}
                className="flex items-center gap-2"
              >
                <RefreshCw className={`w-4 h-4 ${healthLoading ? 'animate-spin' : ''}`} />
                <span className="hidden sm:inline">Refresh</span>
              </Button>

              {/* System Info */}
              <Button
                variant="ghost"
                size="sm"
                className="hidden md:flex"
                onClick={() => {
                  if (health) {
                    console.log('System Health:', health);
                  }
                }}
              >
                <Info className="w-4 h-4" />
              </Button>
            </div>
          </div>

          {/* Additional Status Info */}
          {health && (
            <div className="mt-2 flex flex-wrap gap-2 text-xs text-muted-foreground">
              {health.version && (
                <span>v{health.version}</span>
              )}
              {health.groq_api_status && (
                <span>• Groq API: {health.groq_api_status}</span>
              )}
              {health.database_status && (
                <span>• DB: {health.database_status}</span>
              )}
            </div>
          )}
        </div>
      </header>

      <ToolsInfo 
        open={showToolsInfo} 
        onOpenChange={setShowToolsInfo}
        tools={tools}
      />
    </>
  );
};

export default Header;