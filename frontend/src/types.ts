export type Message = {
  id: string;
  content: string;
  role: 'user' | 'bot';
  timestamp: Date;
  ageBand?: string;
  moderationExplain?: {
    reason: string;
    categories?: Record<string, number>;
  };
  literacyInjected?: boolean;
  riskLevel?: string;
  adjusted?: boolean; // anthropomorphism or safety adjustment applied
};