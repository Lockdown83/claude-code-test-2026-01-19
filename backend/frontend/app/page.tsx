'use client';

import { useDashboard } from '@/hooks/useApi';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Briefcase, Rocket, TrendingUp, ArrowRight } from 'lucide-react';
import Link from 'next/link';

export default function Home() {
  const { data: stats, isLoading, error } = useDashboard();

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="text-lg text-muted-foreground">Loading dashboard...</div>
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
    <div className="space-y-6 p-8">
      {/* Header */}
      <div>
        <h1 className="text-4xl font-bold">Dashboard</h1>
        <p className="text-muted-foreground mt-1">Your VC journey at a glance</p>
      </div>

      {/* Quick Overview Cards */}
      <div className="grid gap-6 md:grid-cols-2">
        {/* Jobs Overview */}
        <Link href="/jobs">
          <Card className="bg-gradient-to-br from-blue-50 to-indigo-50 dark:from-blue-950/30 dark:to-indigo-950/30 border-blue-200 dark:border-blue-900 hover:shadow-lg transition-shadow cursor-pointer">
            <CardHeader>
              <CardTitle className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <Briefcase className="w-5 h-5" />
                  Job Applications
                </div>
                <ArrowRight className="w-5 h-5 text-muted-foreground" />
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex items-end justify-between">
                <div>
                  <div className="text-4xl font-bold">{stats.jobs.applications.total}</div>
                  <div className="text-sm text-muted-foreground">Total Applications</div>
                </div>
                <div className="text-right">
                  <div className="text-2xl font-semibold">{stats.jobs.activity_last_7_days}</div>
                  <div className="text-xs text-muted-foreground">This Week</div>
                </div>
              </div>
              <div className="grid grid-cols-3 gap-2 text-center pt-2 border-t">
                <div>
                  <div className="text-lg font-bold text-green-600 dark:text-green-400">
                    {(stats.jobs.applications.response_rate * 100).toFixed(0)}%
                  </div>
                  <div className="text-xs text-muted-foreground">Response</div>
                </div>
                <div>
                  <div className="text-lg font-bold text-blue-600 dark:text-blue-400">
                    {(stats.jobs.applications.interview_rate * 100).toFixed(0)}%
                  </div>
                  <div className="text-xs text-muted-foreground">Interview</div>
                </div>
                <div>
                  <div className="text-lg font-bold text-purple-600 dark:text-purple-400">
                    {(stats.jobs.applications.offer_rate * 100).toFixed(0)}%
                  </div>
                  <div className="text-xs text-muted-foreground">Offer</div>
                </div>
              </div>
            </CardContent>
          </Card>
        </Link>

        {/* Dealflow Overview */}
        <Link href="/dealflow">
          <Card className="bg-gradient-to-br from-purple-50 to-pink-50 dark:from-purple-950/30 dark:to-pink-950/30 border-purple-200 dark:border-purple-900 hover:shadow-lg transition-shadow cursor-pointer">
            <CardHeader>
              <CardTitle className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <Rocket className="w-5 h-5" />
                  Dealflow Pipeline
                </div>
                <ArrowRight className="w-5 h-5 text-muted-foreground" />
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex items-end justify-between">
                <div>
                  <div className="text-4xl font-bold">{stats.dealflow.total_startups}</div>
                  <div className="text-sm text-muted-foreground">Total Startups</div>
                </div>
                <div className="text-right">
                  <div className="text-2xl font-semibold">{stats.dealflow.activity_last_7_days.new_startups}</div>
                  <div className="text-xs text-muted-foreground">This Week</div>
                </div>
              </div>
              <div className="grid grid-cols-3 gap-2 text-center pt-2 border-t">
                <div>
                  <div className="text-lg font-bold text-blue-600 dark:text-blue-400">
                    {stats.dealflow.network_growth.total_emails_sent}
                  </div>
                  <div className="text-xs text-muted-foreground">Emails</div>
                </div>
                <div>
                  <div className="text-lg font-bold text-green-600 dark:text-green-400">
                    {stats.dealflow.network_growth.total_meetings_held}
                  </div>
                  <div className="text-xs text-muted-foreground">Meetings</div>
                </div>
                <div>
                  <div className="text-lg font-bold text-purple-600 dark:text-purple-400">
                    {stats.dealflow.network_growth.intros_made}
                  </div>
                  <div className="text-xs text-muted-foreground">Intros</div>
                </div>
              </div>
            </CardContent>
          </Card>
        </Link>
      </div>

      {/* Activity Summary */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <TrendingUp className="w-5 h-5" />
            Recent Activity
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            {stats.jobs.activity_last_7_days === 0 && stats.dealflow.activity_last_7_days.new_startups === 0 ? (
              <div className="text-center py-8 text-muted-foreground">
                <p>No activity yet this week</p>
                <p className="text-sm mt-2">Start by adding job applications or sourcing startups!</p>
              </div>
            ) : (
              <>
                <div className="flex items-center justify-between py-2 border-b">
                  <span className="text-sm text-muted-foreground">Total Activity (7 Days)</span>
                  <span className="font-bold">{stats.combined.total_activity_last_7_days}</span>
                </div>
                {stats.jobs.activity_last_7_days > 0 && (
                  <div className="flex items-center justify-between py-2">
                    <span className="text-sm">Job Applications</span>
                    <span className="font-semibold">{stats.jobs.activity_last_7_days}</span>
                  </div>
                )}
                {stats.dealflow.activity_last_7_days.new_startups > 0 && (
                  <div className="flex items-center justify-between py-2">
                    <span className="text-sm">New Startups Sourced</span>
                    <span className="font-semibold">{stats.dealflow.activity_last_7_days.new_startups}</span>
                  </div>
                )}
              </>
            )}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
