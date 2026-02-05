'use client';

import { useDashboard } from '@/hooks/useApi';
import { StreakBadge } from '@/components/gamification/StreakBadge';
import { ProgressRing } from '@/components/gamification/ProgressRing';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Flame, Target, TrendingUp, Activity } from 'lucide-react';
import { cn } from '@/lib/utils';

interface GamificationSidebarProps {
  context?: 'jobs' | 'dealflow' | 'dashboard';
}

export function GamificationSidebar({ context = 'dashboard' }: GamificationSidebarProps) {
  const { data: stats, isLoading } = useDashboard();

  if (isLoading || !stats) {
    return (
      <div className="w-80 border-l bg-card p-6">
        <div className="text-sm text-muted-foreground">Loading...</div>
      </div>
    );
  }

  return (
    <div className="w-80 border-l bg-card flex flex-col overflow-y-auto">
      <div className="p-6 space-y-6">
        {/* Streaks Section */}
        <Card className="bg-gradient-to-br from-orange-50 to-red-50 dark:from-orange-950/20 dark:to-red-950/20 border-orange-200 dark:border-orange-900">
          <CardHeader className="pb-3">
            <CardTitle className="text-base flex items-center gap-2">
              <Flame className="w-4 h-4" />
              Active Streaks
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            <div className="flex justify-between items-center">
              <span className="text-sm text-muted-foreground">Overall</span>
              <StreakBadge days={stats.combined.overall_streak} type="jobs" />
            </div>
            <div className="flex justify-between items-center">
              <span className="text-sm text-muted-foreground">Jobs</span>
              <StreakBadge days={stats.jobs.current_streak} type="jobs" />
            </div>
            <div className="flex justify-between items-center">
              <span className="text-sm text-muted-foreground">Dealflow</span>
              <StreakBadge days={stats.dealflow.current_streak} type="dealflow" />
            </div>
          </CardContent>
        </Card>

        {/* Weekly Goals */}
        <Card>
          <CardHeader className="pb-3">
            <CardTitle className="text-base flex items-center gap-2">
              <Target className="w-4 h-4" />
              This Week
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex flex-col items-center">
              <ProgressRing
                current={stats.jobs.weekly_goal.current}
                target={stats.jobs.weekly_goal.target}
                label="Job Apps"
                size="sm"
              />
            </div>
            <div className="flex flex-col items-center">
              <ProgressRing
                current={stats.dealflow.weekly_goal.current}
                target={stats.dealflow.weekly_goal.target}
                label="Dealflow"
                size="sm"
              />
            </div>
          </CardContent>
        </Card>

        {/* Context-Aware Metrics */}
        {context === 'jobs' && (
          <Card className="bg-gradient-to-br from-blue-50 to-indigo-50 dark:from-blue-950/20 dark:to-indigo-950/20 border-blue-200 dark:border-blue-900">
            <CardHeader className="pb-3">
              <CardTitle className="text-base flex items-center gap-2">
                <TrendingUp className="w-4 h-4" />
                Performance
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              <MetricRow
                label="Response Rate"
                value={`${(stats.jobs.applications.response_rate * 100).toFixed(1)}%`}
                threshold={stats.jobs.applications.response_rate}
              />
              <MetricRow
                label="Interview Rate"
                value={`${(stats.jobs.applications.interview_rate * 100).toFixed(1)}%`}
                threshold={stats.jobs.applications.interview_rate}
              />
              <MetricRow
                label="Offer Rate"
                value={`${(stats.jobs.applications.offer_rate * 100).toFixed(1)}%`}
                threshold={stats.jobs.applications.offer_rate}
              />
              <div className="pt-2 border-t">
                <div className="flex justify-between text-sm">
                  <span className="text-muted-foreground">This Week</span>
                  <span className="font-bold">{stats.jobs.activity_last_7_days}</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-muted-foreground">Total Apps</span>
                  <span className="font-bold">{stats.jobs.applications.total}</span>
                </div>
              </div>
            </CardContent>
          </Card>
        )}

        {context === 'dealflow' && (
          <Card className="bg-gradient-to-br from-purple-50 to-pink-50 dark:from-purple-950/20 dark:to-pink-950/20 border-purple-200 dark:border-purple-900">
            <CardHeader className="pb-3">
              <CardTitle className="text-base flex items-center gap-2">
                <Activity className="w-4 h-4" />
                Pipeline
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-2">
              {Object.entries(stats.dealflow.pipeline).map(([stage, count]) => (
                <div key={stage} className="flex justify-between items-center text-sm">
                  <span className="text-muted-foreground capitalize">{stage}</span>
                  <span className="font-semibold">{count}</span>
                </div>
              ))}
              <div className="pt-2 border-t space-y-1">
                <div className="flex justify-between text-sm">
                  <span className="text-muted-foreground">Emails</span>
                  <span className="font-bold">{stats.dealflow.network_growth.total_emails_sent}</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-muted-foreground">Meetings</span>
                  <span className="font-bold">{stats.dealflow.network_growth.total_meetings_held}</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-muted-foreground">Intros</span>
                  <span className="font-bold">{stats.dealflow.network_growth.intros_made}</span>
                </div>
              </div>
            </CardContent>
          </Card>
        )}

        {context === 'dashboard' && (
          <Card>
            <CardHeader className="pb-3">
              <CardTitle className="text-base flex items-center gap-2">
                <Activity className="w-4 h-4" />
                Quick Stats
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              <div className="space-y-1">
                <div className="text-xs text-muted-foreground">Jobs</div>
                <div className="flex justify-between text-sm">
                  <span>Total Apps</span>
                  <span className="font-bold">{stats.jobs.applications.total}</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span>This Week</span>
                  <span className="font-bold">{stats.jobs.activity_last_7_days}</span>
                </div>
              </div>
              <div className="space-y-1 pt-2 border-t">
                <div className="text-xs text-muted-foreground">Dealflow</div>
                <div className="flex justify-between text-sm">
                  <span>Total Startups</span>
                  <span className="font-bold">{stats.dealflow.total_startups}</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span>This Week</span>
                  <span className="font-bold">{stats.dealflow.activity_last_7_days.new_startups}</span>
                </div>
              </div>
            </CardContent>
          </Card>
        )}

        {/* Quick Actions */}
        <Card>
          <CardHeader className="pb-3">
            <CardTitle className="text-base">Quick Actions</CardTitle>
          </CardHeader>
          <CardContent className="space-y-2">
            <button className="w-full px-4 py-2 text-sm font-medium text-left rounded-md bg-blue-500 text-white hover:bg-blue-600 transition-colors">
              + New Application
            </button>
            <button className="w-full px-4 py-2 text-sm font-medium text-left rounded-md bg-purple-500 text-white hover:bg-purple-600 transition-colors">
              + New Dealflow
            </button>
            <button className="w-full px-4 py-2 text-sm font-medium text-left rounded-md bg-gray-200 dark:bg-gray-700 hover:bg-gray-300 dark:hover:bg-gray-600 transition-colors">
              🔍 Scrape Jobs
            </button>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}

function MetricRow({ label, value, threshold }: { label: string; value: string; threshold: number }) {
  const getColor = () => {
    if (threshold >= 0.3) return 'text-green-600 dark:text-green-400';
    if (threshold >= 0.15) return 'text-yellow-600 dark:text-yellow-400';
    return 'text-red-600 dark:text-red-400';
  };

  return (
    <div className="flex justify-between items-center">
      <span className="text-sm text-muted-foreground">{label}</span>
      <span className={cn('text-base font-bold', getColor())}>{value}</span>
    </div>
  );
}
