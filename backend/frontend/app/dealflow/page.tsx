'use client';

import { useDealflow } from '@/hooks/useApi';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Plus, Filter, Search, Mail, Calendar } from 'lucide-react';
import { Input } from '@/components/ui/input';
import { useState } from 'react';

const STATUS_CONFIG = {
  sourced: { label: 'Sourced', color: 'bg-gray-500' },
  researching: { label: 'Researching', color: 'bg-blue-500' },
  contacted: { label: 'Contacted', color: 'bg-yellow-500' },
  meeting: { label: 'Meeting', color: 'bg-orange-500' },
  shared: { label: 'Shared', color: 'bg-purple-500' },
  progressing: { label: 'Progressing', color: 'bg-green-500' },
  closed: { label: 'Closed', color: 'bg-red-500' },
};

export default function DealflowPage() {
  const [search, setSearch] = useState('');
  const [statusFilter, setStatusFilter] = useState<string | null>(null);

  const { data, isLoading, error } = useDealflow();

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="text-lg text-muted-foreground">Loading pipeline...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="text-lg text-red-500">Error loading dealflow</div>
      </div>
    );
  }

  const dealflow = data?.applications || [];

  // Filter dealflow
  const filteredDealflow = dealflow.filter((deal) => {
    const matchesSearch = search === '' ||
      deal.startup?.name?.toLowerCase().includes(search.toLowerCase()) ||
      deal.startup?.industry?.toLowerCase().includes(search.toLowerCase());
    const matchesStatus = !statusFilter || deal.status === statusFilter;
    return matchesSearch && matchesStatus;
  });

  // Group by status for kanban view
  const groupedByStatus = filteredDealflow.reduce((acc, deal) => {
    if (!acc[deal.status]) {
      acc[deal.status] = [];
    }
    acc[deal.status].push(deal);
    return acc;
  }, {} as Record<string, typeof dealflow>);

  return (
    <div className="h-full flex flex-col">
      {/* Header */}
      <div className="border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
        <div className="p-6 space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold">Dealflow Pipeline</h1>
              <p className="text-muted-foreground mt-1">
                Source and track promising startups
              </p>
            </div>
            <Button className="gap-2">
              <Plus className="w-4 h-4" />
              Add Startup
            </Button>
          </div>

          {/* Search and Filters */}
          <div className="flex gap-3">
            <div className="relative flex-1 max-w-md">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
              <Input
                placeholder="Search startups..."
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
              All ({dealflow.length})
            </button>
            {Object.entries(STATUS_CONFIG).map(([status, config]) => {
              const count = dealflow.filter((deal) => deal.status === status).length;
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

      {/* Pipeline Kanban Board */}
      <div className="flex-1 overflow-x-auto overflow-y-hidden">
        <div className="h-full flex gap-4 p-6 min-w-max">
          {Object.entries(STATUS_CONFIG).map(([status, config]) => {
            const statusDeals = groupedByStatus[status] || [];

            return (
              <div key={status} className="flex flex-col w-80 flex-shrink-0">
                {/* Column Header */}
                <div className="flex items-center justify-between mb-3">
                  <div className="flex items-center gap-2">
                    <div className={`w-2 h-2 rounded-full ${config.color}`} />
                    <h3 className="font-semibold">{config.label}</h3>
                    <Badge variant="secondary">{statusDeals.length}</Badge>
                  </div>
                </div>

                {/* Column Cards */}
                <div className="flex-1 space-y-3 overflow-y-auto">
                  {statusDeals.length === 0 ? (
                    <div className="text-center py-8 text-sm text-muted-foreground border-2 border-dashed rounded-lg">
                      No startups
                    </div>
                  ) : (
                    statusDeals.map((deal) => (
                      <Card key={deal.id} className="hover:shadow-md transition-shadow cursor-pointer">
                        <CardHeader className="pb-3">
                          <CardTitle className="text-base line-clamp-2">
                            {deal.startup?.name || 'Untitled Startup'}
                          </CardTitle>
                          <div className="flex items-center gap-2">
                            {deal.startup?.industry && (
                              <Badge variant="outline" className="text-xs">
                                {deal.startup.industry}
                              </Badge>
                            )}
                            {deal.startup?.funding_stage && (
                              <Badge variant="secondary" className="text-xs">
                                {deal.startup.funding_stage}
                              </Badge>
                            )}
                          </div>
                        </CardHeader>
                        <CardContent className="space-y-3">
                          {deal.startup?.description && (
                            <p className="text-xs text-muted-foreground line-clamp-2">
                              {deal.startup.description}
                            </p>
                          )}

                          {/* Contact Activity */}
                          <div className="flex items-center gap-4 text-xs text-muted-foreground">
                            {deal.emails_sent > 0 && (
                              <div className="flex items-center gap-1">
                                <Mail className="w-3 h-3" />
                                <span>{deal.emails_sent}</span>
                              </div>
                            )}
                            {deal.meetings_held > 0 && (
                              <div className="flex items-center gap-1">
                                <Calendar className="w-3 h-3" />
                                <span>{deal.meetings_held}</span>
                              </div>
                            )}
                          </div>

                          {/* Last Contact Date */}
                          {deal.last_contact_date && (
                            <div className="text-xs text-muted-foreground">
                              Last contact: {new Date(deal.last_contact_date).toLocaleDateString()}
                            </div>
                          )}

                          {/* Notes Preview */}
                          {deal.notes && (
                            <p className="text-xs text-muted-foreground italic line-clamp-2">
                              {deal.notes}
                            </p>
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
