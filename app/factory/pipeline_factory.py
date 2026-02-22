"""
Factory pattern for creating configured pipeline instances.

Assembles the pipeline with the appropriate strategies based on configuration.
Provides a single point for creating fully configured pipeline instances.
"""

from app.core.pipeline import MatchingPipeline
from app.config import Config
from app.services.rule_loader import RuleLoader
from app.services.prompt_builder import PromptBuilder

# Import all parser strategies
from app.strategies.parsers.text_extract_parser import TextExtractParser
from app.strategies.parsers.ocr_parser import OCRParser
from app.strategies.parsers.llm_parser import LLMParser

# Import all scorer strategies
from app.strategies.scorers.llm_scorer import LLMScorer
from app.strategies.scorers.regex_scorer import RegexScorer

# Import all repository strategies
from app.strategies.repositories.sqlite_repository import SQLiteRepository
from app.strategies.repositories.filesystem_repository import FilesystemRepository
from app.strategies.repositories.in_memory_repository import InMemoryRepository


class PipelineFactory:
    """
    Factory for creating configured pipeline instances.
    
    Uses the Factory pattern to assemble pipelines with the appropriate
    strategies based on configuration or runtime parameters.
    """
    
    # Strategy registries
    PARSER_REGISTRY = {
        "text": TextExtractParser,
        "ocr": OCRParser,
        "llm": LLMParser
    }
    
    SCORER_REGISTRY = {
        "llm": LLMScorer,
        "regex": RegexScorer
    }
    
    REPOSITORY_REGISTRY = {
        "sqlite": SQLiteRepository,
        "filesystem": FilesystemRepository,
        "memory": InMemoryRepository
    }
    
    @classmethod
    def build(
        cls,
        config: Config,
        parser: str = None,
        scorer: str = None,
        repository: str = None
    ) -> MatchingPipeline:
        """
        Build a configured pipeline instance.
        
        Args:
            config: Configuration object.
            parser: Parser strategy key (defaults to config.DEFAULT_PARSER).
            scorer: Scorer strategy key (defaults to config.DEFAULT_SCORER).
            repository: Repository strategy key (defaults to config.DEFAULT_REPOSITORY).
            
        Returns:
            Fully configured MatchingPipeline instance.
            
        Raises:
            ValueError: If an unknown strategy key is provided.
        """
        # Use defaults from config if not specified
        parser_key = parser or config.DEFAULT_PARSER
        scorer_key = scorer or config.DEFAULT_SCORER
        repository_key = repository or config.DEFAULT_REPOSITORY
        
        # Instantiate parser
        if parser_key not in cls.PARSER_REGISTRY:
            raise ValueError(f"Unknown parser strategy: {parser_key}")
        parser_class = cls.PARSER_REGISTRY[parser_key]
        parser_instance = parser_class()
        
        # Instantiate scorer
        if scorer_key not in cls.SCORER_REGISTRY:
            raise ValueError(f"Unknown scorer strategy: {scorer_key}")
        scorer_class = cls.SCORER_REGISTRY[scorer_key]
        
        # LLMScorer needs config, others don't
        if scorer_key == "llm":
            scorer_instance = scorer_class(config=config)
        else:
            scorer_instance = scorer_class()
        
        # Instantiate repository
        if repository_key not in cls.REPOSITORY_REGISTRY:
            raise ValueError(f"Unknown repository strategy: {repository_key}")
        repository_class = cls.REPOSITORY_REGISTRY[repository_key]
        
        # FilesystemRepository needs output_dir, others might need different params
        if repository_key == "filesystem":
            repository_instance = repository_class(output_dir=config.RESULTS_DIR)
        elif repository_key == "sqlite":
            repository_instance = repository_class()  # Would need db_path in full implementation
        else:
            repository_instance = repository_class()
        
        # Instantiate services
        rule_loader = RuleLoader(rules_dir=config.RULES_DIR)
        prompt_builder = PromptBuilder(templates_dir=config.TEMPLATES_DIR)
        
        # Assemble and return pipeline
        return MatchingPipeline(
            parser=parser_instance,
            scorer=scorer_instance,
            repository=repository_instance,
            rule_loader=rule_loader,
            prompt_builder=prompt_builder
        )
