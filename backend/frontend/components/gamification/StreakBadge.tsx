import { Flame } from 'lucide-react';
import { Badge } from '@/components/ui/badge';
import { cn } from '@/lib/utils';

interface StreakBadgeProps {
  days: number;
  type?: 'jobs' | 'dealflow';
  className?: string;
}

export function StreakBadge({ days, type = 'jobs', className }: StreakBadgeProps) {
  const getStreakColor = () => {
    if (days === 0) return 'bg-gray-200 dark:bg-gray-700 text-gray-600 dark:text-gray-400';
    if (days < 7) return 'bg-orange-100 dark:bg-orange-900/30 text-orange-700 dark:text-orange-400';
    if (days < 30) return 'bg-yellow-100 dark:bg-yellow-900/30 text-yellow-700 dark:text-yellow-400';
    return 'bg-red-100 dark:bg-red-900/30 text-red-700 dark:text-red-400';
  };

  const getFlameColor = () => {
    if (days === 0) return 'text-gray-400';
    if (days < 7) return 'text-orange-500';
    if (days < 30) return 'text-yellow-500';
    return 'text-red-500';
  };

  return (
    <Badge
      variant="outline"
      className={cn(
        "flex items-center gap-2 px-3 py-1.5 text-sm font-semibold border-0",
        getStreakColor(),
        days > 0 && "animate-pulse",
        className
      )}
    >
      <Flame className={cn("w-4 h-4", getFlameColor())} />
      <span>{days} day streak</span>
    </Badge>
  );
}
