'use client';

import { useApplications } from '@/hooks/useApi';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Plus, Filter, Search } from 'lucide-react';
import { Input } from '@/components/ui/input';
import { useState } from 'react';

const STATUS_CONFIG = {
  saved: { label: 'Saved', color: 'bg-gray-500' },
  applied: { label: 'Applied', color: 'bg-blue-500' },
  interviewing: { label: 'Interviewing', color: 'bg-yellow-500' },
  rejected: { label: 'Rejected', color: 'bg-red-500' },
  offer: { label: 'Offer', color: 'bg-green-500' },
  accepted: { label: 'Accepted', color: 'bg-purple-500' },
};

export default function JobsPage() {
  const [search, setSearch] = useState('');
  const [statusFilter, setStatusFilter] = useState<string | null>(null);

  const { data, isLoading, error } = useApplications();

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="text-lg text-muted-foreground">Loading applications...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="text-lg text-red-500">Error loading applications</div>
      </div>
    );
  }

  const applications = data?.applications || [];

  // Filter applications
  const filteredApplications = applications.filter((app) => {
    const matchesSearch = search === '' ||
      app.job?.title?.toLowerCase().includes(search.toLowerCase()) ||
      app.job?.company?.toLowerCase().includes(search.toLowerCase());
    const matchesStatus = !statusFilter || app.status === statusFilter;
    return matchesSearch && matchesStatus;
  });

  // Group by status for kanban view
  const groupedByStatus = filteredApplications.reduce((acc, app) => {
    if (!acc[app.status]) {
      acc[app.status] = [];
    }
    acc[app.status].push(app);
    return acc;
  }, {} as Record<string, typeof applications>);

  return (
    <div className="h-full flex flex-col">
      {/* Header */}
      <div className="border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
        <div className="p-6 space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold">Job Applications</h1>
              <p className="text-muted-foreground mt-1">
                Track your VC job search journey
              </p>
            </div>
            <Button className="gap-2">
              <Plus className="w-4 h-4" />
              New Application
            </Button>
          </div>

          {/* Search and Filters */}
          <div className="flex gap-3">
            <div className="relative flex-1 max-w-md">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
              <Input
                placeholder="Search applications..."
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                className="pl-10"
              />
            </div>
            <Button variant="outline" className="gap-2">
              <Filter className="w-4 h-4" />
              Filters
            </Button>
          </div>

          {/* Status Filter Chips */}
          <div className="flex gap-2 flex-wrap">
            <button
              onClick={() => setStatusFilter(null)}
              className={`px-3 py-1 text-sm rounded-full transition-colors ${
                statusFilter === null
                  ? 'bg-primary text-primary-foreground'
                  : 'bg-secondary text-secondary-foreground hover:bg-secondary/80'
              }`}
            >
              All ({applications.length})
            </button>
            {Object.entries(STATUS_CONFIG).map(([status, config]) => {
              const count = applications.filter((app) => app.status === status).length;
              if (count === 0) return null;
              return (
                <button
                  key={status}
                  onClick={() => setStatusFilter(status)}
                  className={`px-3 py-1 text-sm rounded-full transition-colors ${
                    statusFilter === status
                      ? 'bg-primary text-primary-foreground'
                      : 'bg-secondary text-secondary-foreground hover:bg-secondary/80'
                  }`}
                >
                  {config.label} ({count})
                </button>
              );
            })}
          </div>
        </div>
      </div>

      {/* Kanban Board */}
      <div className="flex-1 overflow-x-auto overflow-y-hidden">
        <div className="h-full flex gap-4 p-6 min-w-max">
          {Object.entries(STATUS_CONFIG).map(([status, config]) => {
            const statusApps = groupedByStatus[status] || [];

            return (
              <div key={status} className="flex flex-col w-80 flex-shrink-0">
                {/* Column Header */}
                <div className="flex items-center justify-between mb-3">
                  <div className="flex items-center gap-2">
                    <div className={`w-2 h-2 rounded-full ${config.color}`} />
                    <h3 className="font-semibold">{config.label}</h3>
                    <Badge variant="secondary">{statusApps.length}</Badge>
                  </div>
                </div>

                {/* Column Cards */}
                <div className="flex-1 space-y-3 overflow-y-auto">
                  {statusApps.length === 0 ? (
                    <div className="text-center py-8 text-sm text-muted-foreground border-2 border-dashed rounded-lg">
                      No applications
                    </div>
                  ) : (
                    statusApps.map((app) => (
                      <Card key={app.id} className="hover:shadow-md transition-shadow cursor-pointer">
                        <CardHeader className="pb-3">
                          <CardTitle className="text-base line-clamp-2">
                            {app.job?.title || 'Untitled Position'}
                          </CardTitle>
                          <p className="text-sm text-muted-foreground">
                            {app.job?.company || 'Unknown Company'}
                          </p>
                        </CardHeader>
                        <CardContent className="space-y-2">
                          <div className="flex items-center justify-between text-xs text-muted-foreground">
                            <span>{app.job?.location || 'Remote'}</span>
                            <span>{new Date(app.applied_date).toLocaleDateString()}</span>
                          </div>
                          {app.notes && (
                            <p className="text-xs text-muted-foreground line-clamp-2">
                              {app.notes}
                            </p>
                          )}
                          {app.interview_count > 0 && (
                            <Badge variant="outline" className="text-xs">
                              {app.interview_count} interview{app.interview_count > 1 ? 's' : ''}
                            </Badge>
                          )}
                        </CardContent>
                      </Card>
                    ))
                  )}
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
