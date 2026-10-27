import { Loader2 } from 'lucide-react';

interface LoadingProps {
  fullScreen?: boolean;
  text?: string;
}

export function Loading({ fullScreen = false, text = "Loading..." }: LoadingProps) {
  const content = (
    <div className="flex flex-col items-center justify-center space-y-2 text-muted-foreground">
      <Loader2 className="h-8 w-8 animate-spin text-primary" />
      {text && <p className="text-sm font-medium animate-pulse">{text}</p>}
    </div>
  );

  if (fullScreen) {
    return (
      <div className="fixed inset-0 z-50 flex items-center justify-center bg-background/80 backdrop-blur-sm">
        {content}
      </div>
    );
  }

  return (
    <div className="flex h-full w-full items-center justify-center p-8">
      {content}
    </div>
  );
}
