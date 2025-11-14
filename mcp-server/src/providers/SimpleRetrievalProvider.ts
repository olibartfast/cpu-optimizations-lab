import { IRetrievalProvider, SearchResult } from "./IRetrievalProvider.js";
import { LEARNING_RESOURCES } from "../data/knowledgeBase.js";

/**
 * Simple keyword-based retrieval provider (Option C - current implementation)
 * No embeddings, no LLM - just fast keyword matching
 */
export class SimpleRetrievalProvider implements IRetrievalProvider {
  async initialize(): Promise<void> {
    // No initialization needed for simple retrieval
    console.error("SimpleRetrievalProvider: Using keyword-based search");
  }

  async searchTopics(query: string, limit: number = 10): Promise<SearchResult[]> {
    const lowerQuery = query.toLowerCase();
    const results: SearchResult[] = [];

    // Search books
    LEARNING_RESOURCES.books.forEach(book => {
      const score = this.calculateRelevance(book, lowerQuery);
      if (score > 0) {
        results.push({ type: "book", ...book, relevanceScore: score });
      }
    });

    // Search online resources
    LEARNING_RESOURCES.onlineResources.forEach(resource => {
      const score = this.calculateRelevance(resource, lowerQuery);
      if (score > 0) {
        results.push({ type: "online-resource", ...resource, relevanceScore: score });
      }
    });

    // Search projects
    LEARNING_RESOURCES.projects.forEach(project => {
      const score = this.calculateRelevance(project, lowerQuery);
      if (score > 0) {
        results.push({ type: "project", ...project, relevanceScore: score });
      }
    });

    // Search labs
    LEARNING_RESOURCES.labs.forEach(lab => {
      const score = this.calculateRelevance(lab, lowerQuery);
      if (score > 0) {
        results.push({ type: "lab", ...lab, relevanceScore: score });
      }
    });

    return results.sort((a, b) => b.relevanceScore - a.relevanceScore).slice(0, limit);
  }

  private calculateRelevance(item: any, query: string): number {
    let score = 0;

    // Check title
    if (item.title?.toLowerCase().includes(query)) score += 10;

    // Check description
    if (item.description?.toLowerCase().includes(query)) score += 5;

    // Check topics
    if (item.topics) {
      const topicMatch = item.topics.some((topic: string) =>
        topic.toLowerCase().includes(query) || query.includes(topic.toLowerCase())
      );
      if (topicMatch) score += 8;
    }

    return score;
  }

  async getLearningPath(level: string): Promise<any> {
    const levelMap: { [key: string]: string[] } = {
      beginner: ["lab-01", "lab-02", "lab-03"],
      intermediate: ["lab-04", "lab-05", "lab-06"],
      advanced: ["lab-07", "lab-08"]
    };

    const labIds = levelMap[level.toLowerCase()] || [];
    return LEARNING_RESOURCES.labs.filter(lab => labIds.includes(lab.id));
  }

  async getLabInfo(labNumber: number): Promise<any> {
    const labId = `lab-${labNumber.toString().padStart(2, '0')}`;
    return LEARNING_RESOURCES.labs.find(lab => lab.id === labId);
  }

  async getProfilingTools(platform: string): Promise<any> {
    const platformLower = platform.toLowerCase();
    if (platformLower.includes('linux')) return LEARNING_RESOURCES.tools.linux;
    if (platformLower.includes('windows')) return LEARNING_RESOURCES.tools.windows;
    if (platformLower.includes('mac')) return LEARNING_RESOURCES.tools.macos;
    return null;
  }

  async getAllResources(): Promise<any> {
    return LEARNING_RESOURCES;
  }

  async dispose(): Promise<void> {
    // Nothing to clean up
  }
}
