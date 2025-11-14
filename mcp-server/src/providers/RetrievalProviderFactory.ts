import { IRetrievalProvider } from "./IRetrievalProvider.js";
import { SimpleRetrievalProvider } from "./SimpleRetrievalProvider.js";
import { EmbeddingsRetrievalProvider } from "./EmbeddingsRetrievalProvider.js";
import { FullRAGProvider } from "./FullRAGProvider.js";

export type ProviderType = 'simple' | 'embeddings' | 'full-rag';

/**
 * Factory for creating retrieval providers based on configuration
 */
export class RetrievalProviderFactory {
  /**
   * Create a retrieval provider based on type
   * @param type Provider type: 'simple', 'embeddings', or 'full-rag'
   * @returns Configured retrieval provider
   */
  static async createProvider(type: ProviderType): Promise<IRetrievalProvider> {
    let provider: IRetrievalProvider;

    switch (type) {
      case 'simple':
        console.error('Using SimpleRetrievalProvider (keyword-based search)');
        provider = new SimpleRetrievalProvider();
        break;

      case 'embeddings':
        console.error('Using EmbeddingsRetrievalProvider (vector similarity search)');
        console.error('Note: llama.cpp integration is stubbed - needs implementation');
        provider = new EmbeddingsRetrievalProvider();
        break;

      case 'full-rag':
        console.error('Using FullRAGProvider (embeddings + LLM generation)');
        console.error('Note: llama.cpp integration is stubbed - needs implementation');
        provider = new FullRAGProvider();
        break;

      default:
        throw new Error(`Unknown provider type: ${type}`);
    }

    await provider.initialize();
    return provider;
  }

  /**
   * Create provider from environment variable
   * Set RETRIEVAL_PROVIDER=simple|embeddings|full-rag
   */
  static async createFromEnv(): Promise<IRetrievalProvider> {
    const providerType = (process.env.RETRIEVAL_PROVIDER || 'simple') as ProviderType;
    
    if (!['simple', 'embeddings', 'full-rag'].includes(providerType)) {
      console.error(`Invalid RETRIEVAL_PROVIDER: ${providerType}, falling back to 'simple'`);
      return this.createProvider('simple');
    }

    return this.createProvider(providerType);
  }
}
