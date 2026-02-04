'use client';

import { useDashboard } from '@/hooks/useApi';
import { StreakBadge } from '@/components/gamification/StreakBadge';
import { ProgressRing } from '@/components/gamification/ProgressRing';
import { GoalCard } from '@/components/gamification/GoalCard';
import { ConversionMetrics } from '@/components/gamification/ConversionMetrics';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Briefcase, Rocket, Activity, Target } from 'lucide-react';

export default function Home() {
  const { data: stats, isLoading, error } = useDashboard();

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="text-lg text-muted-foreground">Loading your dashboard...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="text-lg text-red-500">Error loading dashboard. Is the backend running?</div>
      </div>
    );
  }

  if (!stats) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="text-lg text-muted-foreground">No data available</div>
      </div>
    );
  }

  return (
    <div className="space-y-6 p-6">
      {/* Header with Overall Streak */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold">VC Dashboard</h1>
          <p className="text-muted-foreground">Your journey to breaking into VC</p>
        </div>
        <StreakBadge
          days={stats.combined.overall_streak}
          type="jobs"
          className="text-lg"
        />
      </div>

      {/* Weekly Goals Progress */}
      <div className="grid gap-6 md:grid-cols-2">
        <Card className="bg-gradient-to-br from-blue-50 to-indigo-50 dark:from-blue-950/30 dark:to-indigo-950/30">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Briefcase className="w-5 h-5" />
              Job Applications
            </CardTitle>
          </CardHeader>
          <CardContent className="flex items-center justify-between">
            <ProgressRing
              current={stats.jobs.weekly_goal.current}
              target={stats.jobs.weekly_goal.target}
              label="This Week"
              size="md"
            />
            <div className="text-right space-y-2">
              <div className="text-sm text-muted-foreground">Current Streak</div>
              <StreakBadge days={stats.jobs.current_streak} type="jobs" />
              <div className="text-2xl font-bold">{stats.jobs.applications.total}</div>
              <div className="text-sm text-muted-foreground">Total Applications</div>
            </div>
          </CardContent>
        </Card>

        <Card className="bg-gradient-to-br from-purple-50 to-pink-50 dark:from-purple-950/30 dark:to-pink-950/30">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Rocket className="w-5 h-5" />
              Dealflow Sourcing
            </CardTitle>
          </CardHeader>
          <CardContent className="flex items-center justify-between">
            <ProgressRing
              current={stats.dealflow.weekly_goal.current}
              target={stats.dealflow.weekly_goal.target}
              label="This Week"
              size="md"
            />
            <div className="text-right space-y-2">
              <div className="text-sm text-muted-foreground">Current Streak</div>
              <StreakBadge days={stats.dealflow.current_streak} type="dealflow" />
              <div className="text-2xl font-bold">{stats.dealflow.total_startups}</div>
              <div className="text-sm text-muted-foreground">Total Startups</div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Tabs for Jobs vs Dealflow Details */}
      <Tabs defaultValue="jobs" className="space-y-4">
        <TabsList className="grid w-full grid-cols-2">
          <TabsTrigger value="jobs">Job Applications</TabsTrigger>
          <TabsTrigger value="dealflow">Dealflow</TabsTrigger>
        </TabsList>

        {/* Jobs Tab */}
        <TabsContent value="jobs" className="space-y-4">
          <div className="grid gap-4 md:grid-cols-3">
            <ConversionMetrics metrics={stats.jobs.applications} />

            <Card>
              <CardHeader>
                <CardTitle>Activity (7 Days)</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-4xl font-bold">{stats.jobs.activity_last_7_days}</div>
                <p className="text-sm text-muted-foreground">Applications submitted</p>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Status Breakdown</CardTitle>
              </CardHeader>
              <CardContent className="space-y-2">
                {Object.entries(stats.jobs.applications.by_status).map(([status, count]) => (
                  <div key={status} className="flex justify-between items-center">
                    <span className="text-sm capitalize">{status}</span>
                    <span className="font-semibold">{count}</span>
                  </div>
                ))}
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        {/* Dealflow Tab */}
        <TabsContent value="dealflow" className="space-y-4">
          <div className="grid gap-4 md:grid-cols-3">
            <Card>
              <CardHeader>
                <CardTitle>Pipeline Stages</CardTitle>
              </CardHeader>
              <CardContent className="space-y-2">
                {Object.entries(stats.dealflow.pipeline).map(([stage, count]) => (
                  <div key={stage} className="flex justify-between items-center">
                    <span className="text-sm capitalize">{stage}</span>
                    <span className="font-semibold">{count}</span>
                  </div>
                ))}
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Network Growth</CardTitle>
              </CardHeader>
              <CardContent className="space-y-2">
                <div className="flex justify-between">
                  <span className="text-sm">Emails Sent</span>
                  <span className="font-semibold">{stats.dealflow.network_growth.total_emails_sent}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm">Meetings Held</span>
                  <span className="font-semibold">{stats.dealflow.network_growth.total_meetings_held}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm">Intros Made</span>
                  <span className="font-semibold">{stats.dealflow.network_growth.intros_made}</span>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>This Week</CardTitle>
              </CardHeader>
              <CardContent className="space-y-2">
                <div className="flex justify-between">
                  <span className="text-sm">New Startups</span>
                  <span className="font-semibold">{stats.dealflow.activity_last_7_days.new_startups}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm">Emails</span>
                  <span className="font-semibold">{stats.dealflow.activity_last_7_days.emails_sent}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm">Meetings</span>
                  <span className="font-semibold">{stats.dealflow.activity_last_7_days.meetings_held}</span>
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>
      </Tabs>
    </div>
  );
}
