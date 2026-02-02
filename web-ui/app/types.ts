export interface PiiEntity {
  label: string;
  text: string;
  start: number;
  end: number;
}

export interface PiiResponse {
  original_text: string;
  entities: PiiEntity[];
  model_used: string;
  processing_time: number;
}

export interface DocumentLog {
  id: number;
  full_text: string;
  pii_entities: PiiEntity[];
  model_used: string;
  processing_time: number;
  created_at: string;
}