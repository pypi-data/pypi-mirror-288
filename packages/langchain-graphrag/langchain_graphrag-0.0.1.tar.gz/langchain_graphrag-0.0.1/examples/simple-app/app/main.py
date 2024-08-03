import os
from enum import StrEnum
from pathlib import Path

from dotenv import load_dotenv

import typer
from typer import Typer

# going to do load_dotenv() here
# as OLLAMA_HOST needs to be in the environment
# before the imports below
load_dotenv()

from langchain_core.embeddings import Embeddings
from langchain_core.language_models import BaseLLM
from langchain_core.output_parsers.string import StrOutputParser

from langchain_text_splitters import TokenTextSplitter

from langchain_community.cache import SQLiteCache
from langchain_community.storage import SQLStore
from langchain_community.document_loaders.directory import DirectoryLoader

from langchain_ollama import OllamaLLM
from langchain_openai import ChatOpenAI, AzureChatOpenAI

from langchain.embeddings.cache import CacheBackedEmbeddings
from langchain_ollama import OllamaEmbeddings
from langchain_openai import OpenAIEmbeddings, AzureOpenAIEmbeddings


import langchain_graphrag.indexing.graph_generation.entity_relationship_extraction as er
import langchain_graphrag.indexing.graph_generation.entity_relationship_summarization as es

from langchain_graphrag.indexing.graph_generation.generator import GraphGenerator

from langchain_graphrag.indexing.indexer import Indexer
from langchain_graphrag.indexing.text_unit_extractor import TextUnitExtractor
from langchain_graphrag.indexing.graph_clustering.community_detector import (
    HierarchicalLeidenCommunityDetector,
)
from langchain_graphrag.indexing.embedding_generation.graph import (
    Node2VectorGraphEmbeddingGenerator,
)

from langchain_graphrag.indexing.embedding_generation import (
    EntityEmbeddingGenerator,
    RelationshipEmbeddingGenerator,
)


from langchain_graphrag.indexing.table_generation import EntitiesTableGenerator
from langchain_graphrag.indexing.table_generation import CommunitiesTableGenerator
from langchain_graphrag.indexing.table_generation import RelationshipsTableGenerator
from langchain_graphrag.indexing.table_generation import TextUnitsTableGenerator

app = Typer()


class LLMType(StrEnum):
    openai: str = "openai"
    azure_openai: str = "azure_openai"
    ollama: str = "ollama"


class LLMModel(StrEnum):
    gpt4o: str = "gpt-4o"
    gpt4omini: str = "gpt-4o-mini"
    gemma2_9b_instruct_q8_0: str = "gemma2:9b-instruct-q8_0"
    gemma2_27b_instruct_q6_K: str = "gemma2:27b-instruct-q6_K"


class EmbeddingModelType(StrEnum):
    openai: str = "openai"
    azure_openai: str = "azure_openai"
    ollama: str = "ollama"


class EmbeddingModel(StrEnum):
    text_embedding_3_small: str = "text-embedding-3-small"
    nomic_embed_text: str = "nomic_embed_text"


def make_llm_instance(
    llm_type: LLMType,
    llm_model: LLMModel,
    cache_dir: Path,
) -> BaseLLM:
    if llm_type == LLMType.openai:
        return ChatOpenAI(
            model=llm_model,
            api_key=os.getenv("LANGCHAIN_GRAPHRAG_OPENAI_CHAT_API_KEY"),
            cache=SQLiteCache(str(cache_dir / "openai_cache.db")),
        )
    elif llm_type == LLMType.azure_openai:
        return AzureChatOpenAI(
            model=llm_model,
            api_version="2024-05-01-preview",
            api_key=os.getenv("LANGCHAIN_GRAPHRAG_AZURE_OPENAI_CHAT_API_KEY"),
            azure_endpoint=os.getenv("LANGCHAIN_GRAPHRAG_AZURE_OPENAI_CHAT_ENDPOINT"),
            azure_deployment=os.getenv(
                "LANGCHAIN_GRAPHRAG_AZURE_OPENAI_CHAT_DEPLOYMENT"
            ),
            cache=SQLiteCache(str(cache_dir / "azure_openai_cache.db")),
        )
    elif llm_type == LLMType.ollama:
        return OllamaLLM(
            model=llm_model,
            cache=SQLiteCache(str(cache_dir / "ollama.db")),
        )


def make_embedding_instance(
    embedding_type: EmbeddingModelType,
    embedding_model: EmbeddingModel,
    cache_dir: Path,
) -> Embeddings:

    underlying_embedding: Embeddings

    if embedding_type == EmbeddingModelType.openai:
        underlying_embedding = OpenAIEmbeddings(
            model=embedding_model,
            api_key=os.getenv("LANGCHAIN_GRAPHRAG_OPENAI_EMBED_API_KEY"),
        )
    elif embedding_type == EmbeddingModelType.azure_openai:
        underlying_embedding = AzureOpenAIEmbeddings(
            model=embedding_model,
            api_version="2024-02-15-preview",
            api_key=os.getenv("LANGCHAIN_GRAPHRAG_AZURE_OPENAI_EMBED_API_KEY"),
            azure_endpoint=os.getenv("LANGCHAIN_GRAPHRAG_AZURE_OPENAI_EMBED_ENDPOINT"),
            azure_deployment=os.getenv(
                "LANGCHAIN_GRAPHRAG_AZURE_OPENAI_EMBED_DEPLOYMENT"
            ),
        )
    elif embedding_type == EmbeddingModelType.ollama:
        underlying_embedding = OllamaEmbeddings(model=embedding_model)

    embedding_db_path = "sqlite:///" + str(cache_dir.joinpath("embedding.db"))
    store = SQLStore(namespace=embedding_model, db_url=embedding_db_path)
    store.create_schema()

    cached_embedding_model = CacheBackedEmbeddings.from_bytes_store(
        underlying_embeddings=underlying_embedding,
        document_embedding_cache=store,
    )

    return cached_embedding_model


@app.command()
def indexer(
    input_dir: Path = typer.Option(..., dir_okay=True, file_okay=False),
    output_dir: Path = typer.Option(..., dir_okay=True, file_okay=False),
    prompts_dir: Path = typer.Option(..., dir_okay=True, file_okay=False),
    cache_dir: Path = typer.Option(..., dir_okay=True, file_okay=False),
    llm_type: LLMType = typer.Option(LLMType.azure_openai, case_sensitive=False),
    llm_model: LLMModel = typer.Option(LLMModel.gpt4o, case_sensitive=False),
    embedding_type: EmbeddingModelType = typer.Option(
        EmbeddingModelType.azure_openai, case_sensitive=False
    ),
    embedding_model: EmbeddingModel = typer.Option(
        EmbeddingModel.text_embedding_3_small, case_sensitive=False
    ),
    chunk_size: int = typer.Option(1200),
    chunk_overlap: int = typer.Option(100),
):

    ######### Start of creation of various objects/dependencies #############

    # Dataloader that loads all the text files from
    # the supplied directory
    data_loader = DirectoryLoader(str(input_dir), glob="*.txt")

    # TextSplitter required by TextUnitExtractor
    text_splitter = TokenTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )

    # TextUnitExtractor that extracts text units from the text files
    text_unit_extractor = TextUnitExtractor(text_splitter=text_splitter)

    # Prompt Builder for Entity Extraction
    er_extraction_prompt = prompts_dir / "entity_extraction.txt"
    er_prompt_builder = er.DefaultEntityExtractionPromptBuilder(er_extraction_prompt)

    # LLM
    er_llm = make_llm_instance(llm_type, llm_model, cache_dir)
    # Output Parser
    er_op = er.EntityExtractionOutputParser()
    # Graph Merger
    er_gm = er.GraphsMerger()

    # Entity Extractor
    entity_extractor = er.EntityRelationshipExtractor(
        prompt_builder=er_prompt_builder,
        llm=er_llm,
        output_parser=er_op,
        graphs_merger=er_gm,
    )

    # Prompt Builder for Entity Extraction
    es_extraction_prompt = prompts_dir / "summarize_descriptions.txt"
    es_prompt_builder = es.DefaultSummarizeDescriptionPromptBuilder(
        es_extraction_prompt
    )

    # LLM
    es_llm = make_llm_instance(llm_type, llm_model, cache_dir)

    # Entity Summarizer
    entity_summarizer = es.EntityRelationshipDescriptionSummarizer(
        prompt_builder=es_prompt_builder, llm=es_llm, output_parser=StrOutputParser()
    )

    # Graph Generator
    graph_generator = GraphGenerator(
        er_extractor=entity_extractor,
        er_description_summarizer=entity_summarizer,
    )

    # Community Detector
    community_detector = HierarchicalLeidenCommunityDetector()

    # Graph Embedding Generator
    graph_embedding_generator = Node2VectorGraphEmbeddingGenerator()

    # Entity Embedding Generator
    entity_embedding_generator = EntityEmbeddingGenerator(
        embedding_model=make_embedding_instance(
            embedding_type=embedding_type,
            embedding_model=embedding_model,
            cache_dir=cache_dir,
        )
    )

    # Relationship Embedding Generator
    relationship_embedding_generator = RelationshipEmbeddingGenerator(
        embedding_model=make_embedding_instance(
            embedding_type=embedding_type,
            embedding_model=embedding_model,
            cache_dir=cache_dir,
        )
    )

    # Final Entities Generator
    entities_table_generator = EntitiesTableGenerator(
        entity_embedding_generator=entity_embedding_generator,
        graph_embedding_generator=graph_embedding_generator,
    )

    # Final Relationships Generator
    relationships_table_generator = RelationshipsTableGenerator(
        relationship_embedding_generator=relationship_embedding_generator
    )

    # Final Communities Generator
    communities_table_generator = CommunitiesTableGenerator()

    text_units_table_generator = TextUnitsTableGenerator(
        embedding_model=make_embedding_instance(
            embedding_type=embedding_type,
            embedding_model=embedding_model,
            cache_dir=cache_dir,
        )
    )

    ######### End of creation of various objects/dependencies #############

    indexer = Indexer(
        output_dir=output_dir,
        data_loader=data_loader,
        text_unit_extractor=text_unit_extractor,
        graph_generator=graph_generator,
        community_detector=community_detector,
        entities_table_generator=entities_table_generator,
        relationships_table_generator=relationships_table_generator,
        communities_table_generator=communities_table_generator,
        text_units_table_generator=text_units_table_generator,
    )

    indexer.run()


@app.command()
def query():
    pass


if __name__ == "__main__":
    app()
