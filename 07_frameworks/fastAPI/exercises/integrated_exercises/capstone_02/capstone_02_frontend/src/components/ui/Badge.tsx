import React, { forwardRef } from 'react';
import { cn } from './Button';

export interface BadgeProps extends React.HTMLAttributes<HTMLDivElement> {
  variant?: 'default' | 'secondary' | 'destructive' | 'outline' | 'success' | 'warning';
}

export const Badge = forwardRef<HTMLDivElement, BadgeProps>(
  ({ className, variant = 'default', ...props }, ref) => {
    return (
      <div
        ref={ref}
        className={cn(
          "inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2",
          {
            "border-transparent bg-primary text-primary-foreground shadow hover:bg-primary/80": variant === 'default',
            "border-transparent bg-secondary text-secondary-foreground hover:bg-secondary/80": variant === 'secondary',
            "border-transparent bg-destructive text-destructive-foreground shadow hover:bg-destructive/80": variant === 'destructive',
            "text-foreground": variant === 'outline',
            "border-transparent bg-green-500/15 text-green-700 dark:text-green-400": variant === 'success',
            "border-transparent bg-yellow-500/15 text-yellow-700 dark:text-yellow-400": variant === 'warning',
          },
          className
        )}
        {...props}
      />
    );
  }
);
Badge.displayName = "Badge";
