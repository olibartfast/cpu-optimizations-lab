/**
 * Interface for different retrieval strategies
 */
export interface SearchResult {
  type: string;
  id: string;
  title: string;
  description: string;
  topics?: string[];
  relevanceScore: number;
  [key: string]: any;
}

export interface IRetrievalProvider {
  /**
   * Initialize the provider (load models, create indexes, etc.)
   */
  initialize(): Promise<void>;

  /**
   * Search for resources by query
   */
  searchTopics(query: string, limit?: number): Promise<SearchResult[]>;

  /**
   * Get learning path for a skill level
   */
  getLearningPath(level: string): Promise<any>;

  /**
   * Get information about a specific lab
   */
  getLabInfo(labNumber: number): Promise<any>;

  /**
   * Get profiling tools for a platform
   */
  getProfilingTools(platform: string): Promise<any>;

  /**
   * Get all available resources
   */
  getAllResources(): Promise<any>;

  /**
   * Clean up resources
   */
  dispose(): Promise<void>;
}
