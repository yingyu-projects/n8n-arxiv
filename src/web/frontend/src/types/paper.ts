export interface Paper {
  id: string;
  title: string;
  pdf_link: string;
  category: string;
  arxiv_id?: string;
  summary?: Record<string, any>;
  parsed_at?: string;
  created_at: string;
}

export interface PaperList {
  id: string;
  title: string;
  pdf_link: string;
  category: string;
  parsed_at?: string;
  created_at: string;
}

