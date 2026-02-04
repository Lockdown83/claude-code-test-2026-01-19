import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { ArrowRight } from 'lucide-react';

interface ConversionMetricsProps {
  metrics: {
    response_rate: number;
    interview_rate: number;
    offer_rate: number;
  };
}

export function ConversionMetrics({ metrics }: ConversionMetricsProps) {
  const formatRate = (rate: number) => `${(rate * 100).toFixed(1)}%`;

  const getRateColor = (rate: number) => {
    if (rate >= 0.3) return 'text-green-600 dark:text-green-400';
    if (rate >= 0.15) return 'text-yellow-600 dark:text-yellow-400';
    return 'text-red-600 dark:text-red-400';
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle>Conversion Funnel</CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        {/* Response Rate */}
        <div className="flex items-center justify-between">
          <span className="text-sm text-muted-foreground">Response Rate</span>
          <span className={`text-2xl font-bold ${getRateColor(metrics.response_rate)}`}>
            {formatRate(metrics.response_rate)}
          </span>
        </div>

        <ArrowRight className="w-4 h-4 mx-auto text-muted-foreground" />

        {/* Interview Rate */}
        <div className="flex items-center justify-between">
          <span className="text-sm text-muted-foreground">Interview Rate</span>
          <span className={`text-2xl font-bold ${getRateColor(metrics.interview_rate)}`}>
            {formatRate(metrics.interview_rate)}
          </span>
        </div>

        <ArrowRight className="w-4 h-4 mx-auto text-muted-foreground" />

        {/* Offer Rate */}
        <div className="flex items-center justify-between">
          <span className="text-sm text-muted-foreground">Offer Rate</span>
          <span className={`text-2xl font-bold ${getRateColor(metrics.offer_rate)}`}>
            {formatRate(metrics.offer_rate)}
          </span>
        </div>
      </CardContent>
    </Card>
  );
}
