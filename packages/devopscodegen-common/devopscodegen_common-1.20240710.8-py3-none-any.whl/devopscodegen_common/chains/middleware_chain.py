"""
This module contains the create_find_middleware_chain function which
returns the find_middleware_chain corresponding to the language and dependency management tool
"""

from importlib.resources import files
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable
from devopscodegen_common.repositories.source_code_repository import (
    SourceCodeRepository,
)
from devopscodegen_common.output_parsers.devopscodegen_output_parser import (
    DevopscodegenOutputParser,
)


class MiddlewareChain:
    """
    Middleware Chain class
    """

    # pylint: disable=R0913
    def __init__(
        self,
        llm: Runnable = None,
        source_code_repository: SourceCodeRepository = None,
        chain=None,
        templates_package: str = "devopscodegen_common.templates.middlewares",
    ):
        self.set_llm(llm)
        self.set_source_code_repository(source_code_repository)
        self.set_chain(chain)
        self.set_templates_package(templates_package)

    def get_llm(self) -> Runnable:
        """Get llm"""
        return self.llm

    def set_llm(self, llm: Runnable = None):
        """Set llm"""
        self.llm = llm

    def get_source_code_repository(self) -> SourceCodeRepository:
        """Get source code repository"""
        return self.source_code_repository

    def set_source_code_repository(
        self, source_code_repository: SourceCodeRepository = None
    ):
        """Set source code repository"""
        self.source_code_repository = source_code_repository

    def get_chain(self) -> Runnable:
        """Get chain"""
        return self.chain

    def set_chain(self, chain: Runnable = None):
        """Set chain"""
        self.chain = chain

    def get_templates_package(self) -> str:
        """Get templates_package"""
        return self.templates_package

    def set_templates_package(self, templates_package: str = None):
        """Set chain"""
        self.templates_package = templates_package

    def create_chain(self) -> Runnable:
        """Create middleware chain"""
        llm = self.get_llm()
        language = self.get_source_code_repository().get_language()
        dependency_management_tool = (
            self.get_source_code_repository().get_dependency_management_tool()
        )
        templates_package = self.get_templates_package()

        middlewares = (
            files(templates_package)
            .joinpath(language, dependency_management_tool, "middlewares.txt")
            .read_text(encoding="utf-8")
        )

        chain = (
            ChatPromptTemplate.from_messages(
                [
                    (
                        "system",
                        """You will be provided with below information
    - contents of dependency manifest {dependency_manifest} enclosed within ```{dependency_manifest}_begin and ```{dependency_manifest}_end delimiters.
    - {language} middlewares enclosed within ```middlewares_begin and ```middlewares_end delimiters.
    Your task is to select the correct middleware using only the provided information.
    Middleware should be enclosed within ```middleware_begin and ```middleware_end delimiters.
    If more than one {language} middleware are possible, then select the most specific instead of the most generic.
    Before selecting the middleware, explain your reasoning.
    Your reasoning should be enclosed within ```reasoning_begin and ```reasoning_end delimiters.
    """,
                    ),
                    (
                        "human",
                        """```{dependency_manifest}_begin
    {dependency_manifest_content}
    ```{dependency_manifest}_end

    ```{language}_middlewares_begin
    {middlewares}
    ```{language}_middlewares_end
    """,
                    ),
                ]
            ).partial(middlewares=middlewares)
            | llm
            | DevopscodegenOutputParser()
        ).with_config(run_name="find_middleware_chain")
        self.set_chain(chain)
        return chain
