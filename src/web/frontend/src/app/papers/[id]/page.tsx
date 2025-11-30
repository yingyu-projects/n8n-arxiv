import PaperDetail from '@/components/PaperDetail/PaperDetail';

interface PageProps {
  params: {
    id: string;
  };
}

export default function PaperDetailPage({ params }: PageProps) {
  return <PaperDetail id={params.id} />;
}

