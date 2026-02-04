import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Progress } from '@/components/ui/progress';
import { Trophy, TrendingUp } from 'lucide-react';

interface GoalCardProps {
  title: string;
  current: number;
  target: number;
  progress: number; // 0-1
  icon?: React.ReactNode;
}

export function GoalCard({ title, current, target, progress, icon }: GoalCardProps) {
  const percentage = Math.round(progress * 100);

  return (
    <Card>
      <CardHeader className="pb-3">
        <CardTitle className="flex items-center gap-2 text-base">
          {icon || <Trophy className="w-4 h-4" />}
          {title}
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-2">
          <div className="flex items-center justify-between text-sm">
            <span className="text-muted-foreground">Progress</span>
            <span className="font-bold">{current} / {target}</span>
          </div>
          <Progress value={percentage} className="h-2" />
          <div className="flex items-center gap-1 text-xs text-muted-foreground">
            <TrendingUp className="w-3 h-3" />
            <span>{percentage}% complete</span>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
