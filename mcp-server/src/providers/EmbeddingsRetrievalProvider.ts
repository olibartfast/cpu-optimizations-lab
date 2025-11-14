import { IRetrievalProvider, SearchResult } from "./IRetrievalProvider.js";
import { LEARNING_RESOURCES } from "../data/knowledgeBase.js";

/**
 * Embeddings-based retrieval provider (Option A)
 * Uses llama.cpp for embeddings and vector similarity search
 * 
 * NOTE: Requires llama.cpp model for embeddings
 * Example models: nomic-embed-text, all-MiniLM-L6-v2
 */
export class EmbeddingsRetrievalProvider implements IRetrievalProvider {
  private embeddings: Map<string, number[]> = new Map();
  private documents: Map<string, any> = new Map();
  private llama: any; // Would be LlamaCpp instance
  private initialized = false;

  async initialize(): Promise<void> {
    console.error("EmbeddingsRetrievalProvider: Initializing...");
    
    // TODO: Initialize llama.cpp with embedding model
    // const { LlamaCpp } = await import('node-llama-cpp');
    // this.llama = new LlamaCpp({
    //   modelPath: process.env.EMBEDDING_MODEL_PATH || './models/nomic-embed-text.gguf',
    //   embedding: true
    // });
    
    // TODO: Generate embeddings for all documents
    await this.indexDocuments();
    
    this.initialized = true;
    console.error("EmbeddingsRetrievalProvider: Ready (STUB - not yet implemented)");
  }

  private async indexDocuments(): Promise<void> {
    // TODO: Convert all resources to embeddings
    const allDocs = [
      ...LEARNING_RESOURCES.books.map(b => ({ ...b, type: 'book' })),
      ...LEARNING_RESOURCES.onlineResources.map(r => ({ ...r, type: 'online-resource' })),
      ...LEARNING_RESOURCES.projects.map(p => ({ ...p, type: 'project' })),
      ...LEARNING_RESOURCES.labs.map(l => ({ ...l, type: 'lab' }))
    ];

    for (const doc of allDocs) {
      const docId = `${doc.type}-${doc.id}`;
      this.documents.set(docId, doc);
      
      // TODO: Generate embedding for document
      // const text = this.documentToText(doc);
      // const embedding = await this.llama.embed(text);
      // this.embeddings.set(docId, embedding);
      
      // For now, store dummy embedding
      this.embeddings.set(docId, new Array(384).fill(0));
    }

    console.error(`EmbeddingsRetrievalProvider: Indexed ${allDocs.length} documents`);
  }

  private documentToText(doc: any): string {
    const parts = [
      doc.title,
      doc.description,
      doc.topics?.join(' '),
      doc.author
    ].filter(Boolean);
    return parts.join('. ');
  }

  private cosineSimilarity(a: number[], b: number[]): number {
    let dotProduct = 0;
    let normA = 0;
    let normB = 0;
    
    for (let i = 0; i < a.length; i++) {
      dotProduct += a[i] * b[i];
      normA += a[i] * a[i];
      normB += b[i] * b[i];
    }
    
    return dotProduct / (Math.sqrt(normA) * Math.sqrt(normB));
  }

  async searchTopics(query: string, limit: number = 10): Promise<SearchResult[]> {
    if (!this.initialized) {
      throw new Error("Provider not initialized. Call initialize() first.");
    }

    // TODO: Generate query embedding
    // const queryEmbedding = await this.llama.embed(query);
    
    // For now, fall back to simple search
    console.error("EmbeddingsRetrievalProvider: Falling back to keyword search (embedding not implemented)");
    return this.fallbackSearch(query, limit);
    
    // TODO: Find similar documents using cosine similarity
    // const results: SearchResult[] = [];
    // for (const [docId, docEmbedding] of this.embeddings.entries()) {
    //   const similarity = this.cosineSimilarity(queryEmbedding, docEmbedding);
    //   if (similarity > 0.5) { // threshold
    //     const doc = this.documents.get(docId)!;
    //     results.push({ ...doc, relevanceScore: similarity * 100 });
    //   }
    // }
    // return results.sort((a, b) => b.relevanceScore - a.relevanceScore).slice(0, limit);
  }

  private fallbackSearch(query: string, limit: number): SearchResult[] {
    const lowerQuery = query.toLowerCase();
    const results: SearchResult[] = [];

    for (const [_, doc] of this.documents.entries()) {
      let score = 0;
      if (doc.title?.toLowerCase().includes(lowerQuery)) score += 10;
      if (doc.description?.toLowerCase().includes(lowerQuery)) score += 5;
      if (doc.topics?.some((t: string) => t.toLowerCase().includes(lowerQuery))) score += 8;
      
      if (score > 0) {
        results.push({ ...doc, relevanceScore: score });
      }
    }

    return results.sort((a, b) => b.relevanceScore - a.relevanceScore).slice(0, limit);
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
    // TODO: Clean up llama.cpp resources
    // if (this.llama) {
    //   await this.llama.dispose();
    // }
    this.embeddings.clear();
    this.documents.clear();
  }
}
