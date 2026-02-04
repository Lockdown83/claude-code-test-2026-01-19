import { cn } from '@/lib/utils';

interface ProgressRingProps {
  current: number;
  target: number;
  label: string;
  size?: 'sm' | 'md' | 'lg';
}

export function ProgressRing({ current, target, label, size = 'md' }: ProgressRingProps) {
  const percentage = Math.min((current / target) * 100, 100);

  const getProgressColor = () => {
    if (percentage < 25) return 'stroke-[#EF4444]'; // red
    if (percentage < 50) return 'stroke-[#F59E0B]'; // orange
    if (percentage < 100) return 'stroke-[#10B981]'; // green
    return 'stroke-[#6366F1]'; // indigo
  };

  const sizeClasses = {
    sm: 'w-20 h-20 text-xs',
    md: 'w-32 h-32 text-base',
    lg: 'w-48 h-48 text-lg',
  };

  const strokeWidth = {
    sm: 6,
    md: 8,
    lg: 10,
  };

  const radius = 40;
  const circumference = 2 * Math.PI * radius;
  const strokeDashoffset = circumference - (percentage / 100) * circumference;

  return (
    <div className="flex flex-col items-center gap-2">
      <div className={cn("relative flex items-center justify-center", sizeClasses[size])}>
        {/* Background circle */}
        <svg className="absolute inset-0 transform -rotate-90" viewBox="0 0 100 100">
          <circle
            cx="50"
            cy="50"
            r={radius}
            fill="none"
            stroke="currentColor"
            strokeWidth={strokeWidth[size]}
            className="text-gray-200 dark:text-gray-700"
          />
          {/* Progress circle */}
          <circle
            cx="50"
            cy="50"
            r={radius}
            fill="none"
            strokeWidth={strokeWidth[size]}
            strokeDasharray={circumference}
            strokeDashoffset={strokeDashoffset}
            className={cn("transition-all duration-1000 ease-out", getProgressColor())}
            strokeLinecap="round"
          />
        </svg>

        {/* Center text */}
        <div className="text-center z-10">
          <div className="font-bold">{current}</div>
          <div className="text-xs text-muted-foreground">/ {target}</div>
        </div>
      </div>

      <p className="text-sm font-medium text-center">{label}</p>
    </div>
  );
}
