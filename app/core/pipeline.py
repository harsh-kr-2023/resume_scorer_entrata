"""
Template Method pattern implementation for the resume matching pipeline.

Defines the skeleton of the matching algorithm with five steps:
1. Parse document
2. Load rules
3. Build prompt
4. Score with LLM
5. Persist result

Each step can fail independently, and errors are caught and reported.
"""

import logging
from app.core.interfaces.base_parser import BaseParser
from app.core.interfaces.base_scorer import BaseScorer
from app.core.interfaces.base_repository import BaseRepository
from app.core.models import PipelineResult
from app.core.exceptions import (
    ParsingError,
    RuleLoadingError,
    PromptBuildError,
    ScoringError,
    PersistenceError,
    MatcherError
)
from app.services.rule_loader import RuleLoader
from app.services.prompt_builder import PromptBuilder

logger = logging.getLogger(__name__)


class MatchingPipeline:
    """
    Template Method pattern for resume matching pipeline.
    
    Orchestrates the five-step process of matching a resume to a job description:
    1. Parse the resume document
    2. Load evaluation rules for the role
    3. Build the evaluation prompt
    4. Score using the configured scorer
    5. Persist the result
    
    Each step is isolated and can fail independently with specific error handling.
    """
    
    def __init__(
        self,
        parser: BaseParser,
        scorer: BaseScorer,
        repository: BaseRepository,
        rule_loader: RuleLoader,
        prompt_builder: PromptBuilder
    ):
        """
        Initialize the pipeline with all required strategies.
        
        Args:
            parser: Strategy for parsing documents.
            scorer: Strategy for scoring resumes.
            repository: Strategy for persisting results.
            rule_loader: Service for loading evaluation rules.
            prompt_builder: Service for building prompts.
        """
        self.parser = parser
        self.scorer = scorer
        self.repository = repository
        self.rule_loader = rule_loader
        self.prompt_builder = prompt_builder
    
    def execute(
        self,
        file_path: str,
        jd_text: str,
        role: str,
        resume_name: str
    ) -> PipelineResult:
        """
        Execute the complete matching pipeline.
        
        Args:
            file_path: Path to the resume file.
            jd_text: Job description text.
            role: Role identifier for loading rules.
            resume_name: Name/identifier for the resume.
            
        Returns:
            PipelineResult indicating success or failure with detailed error info.
        """
        try:
            # Step 1: Parse document
            logger.info(f"Step 1/5: Parsing document: {file_path}")
            try:
                parsed = self.parser.parse(file_path)
                logger.info(f"Parsed document: {parsed.metadata.get('page_count', 'unknown')} pages")
            except ParsingError as e:
                logger.error(f"Parsing failed: {str(e)}")
                return PipelineResult(
                    success=False,
                    data=None,
                    error=str(e),
                    failed_step="parse"
                )
            
            # Step 2: Load rules
            logger.info(f"Step 2/5: Loading rules for role: {role}")
            try:
                rules = self.rule_loader.load(role)
                logger.info(f"Loaded rules: {len(rules.get('must_have', []))} must-have, "
                          f"{len(rules.get('nice_to_have', []))} nice-to-have")
            except RuleLoadingError as e:
                logger.error(f"Rule loading failed: {str(e)}")
                return PipelineResult(
                    success=False,
                    data=None,
                    error=str(e),
                    failed_step="load_rules"
                )
            
            # Step 3: Build prompt
            logger.info("Step 3/5: Building evaluation prompt")
            try:
                prompt = self.prompt_builder.build(parsed.text, jd_text, rules)
                logger.info(f"Built prompt: {len(prompt)} characters")
            except PromptBuildError as e:
                logger.error(f"Prompt building failed: {str(e)}")
                return PipelineResult(
                    success=False,
                    data=None,
                    error=str(e),
                    failed_step="build_prompt"
                )
            
            # Step 4: Score
            logger.info("Step 4/5: Scoring with LLM")
            try:
                result = self.scorer.score(prompt)
                logger.info(f"Scoring complete: score={result.score}")
            except ScoringError as e:
                logger.error(f"Scoring failed: {str(e)}")
                return PipelineResult(
                    success=False,
                    data=None,
                    error=str(e),
                    failed_step="score"
                )
            
            # Step 5: Persist
            logger.info("Step 5/5: Persisting result")
            try:
                self.repository.save(result, role, resume_name)
                logger.info("Result persisted successfully")
            except PersistenceError as e:
                logger.error(f"Persistence failed: {str(e)}")
                return PipelineResult(
                    success=False,
                    data=None,
                    error=str(e),
                    failed_step="persist"
                )
            
            # Success!
            logger.info("Pipeline completed successfully")
            return PipelineResult(
                success=True,
                data=result,
                error=None,
                failed_step=None
            )
            
        except MatcherError as e:
            # Catch any MatcherError that wasn't caught above
            logger.error(f"Pipeline failed with MatcherError: {str(e)}")
            return PipelineResult(
                success=False,
                data=None,
                error=str(e),
                failed_step="unknown"
            )
        except Exception as e:
            # Catch unexpected errors
            logger.error(f"Pipeline failed with unexpected error: {str(e)}", exc_info=True)
            return PipelineResult(
                success=False,
                data=None,
                error=f"Unexpected error: {str(e)}",
                failed_step="unknown"
            )
