
import { FileQuestion } from 'lucide-react';
import { Button } from '../components/ui/Button';
import { useNavigate } from 'react-router-dom';

export default function NotFoundPage() {
  const navigate = useNavigate();
  
  return (
    <div className="flex h-screen flex-col items-center justify-center text-center bg-muted/20">
      <div className="rounded-full bg-primary/10 p-6 mb-4">
        <FileQuestion className="h-12 w-12 text-primary" />
      </div>
      <h1 className="text-4xl font-bold tracking-tight mb-2">404</h1>
      <h2 className="text-2xl font-semibold mb-2">Page Not Found</h2>
      <p className="text-muted-foreground mb-6 max-w-[400px]">
        The page you are looking for doesn't exist or has been moved.
      </p>
      <Button onClick={() => navigate('/')}>
        Go Home
      </Button>
    </div>
  );
}
