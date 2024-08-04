import json
import logging
import uuid
from typing import Any, AsyncGenerator, Generator, Optional

from r2r.base import (
    AsyncState,
    CompletionProvider,
    LLMChatCompletionChunk,
    PipeType,
    PromptProvider,
)
from r2r.base.abstractions.llm import GenerationConfig

from ..abstractions.generator_pipe import GeneratorPipe
from .search_rag_pipe import SearchRAGPipe

logger = logging.getLogger(__name__)


class StreamingSearchRAGPipe(SearchRAGPipe):
    SEARCH_STREAM_MARKER = "search"
    COMPLETION_STREAM_MARKER = "completion"

    def __init__(
        self,
        llm_provider: CompletionProvider,
        prompt_provider: PromptProvider,
        type: PipeType = PipeType.GENERATOR,
        config: Optional[GeneratorPipe] = None,
        *args,
        **kwargs,
    ):
        super().__init__(
            llm_provider=llm_provider,
            prompt_provider=prompt_provider,
            type=type,
            config=config
            or GeneratorPipe.Config(
                name="default_streaming_rag_pipe", task_prompt="default_rag"
            ),
            *args,
            **kwargs,
        )

    async def _run_logic(
        self,
        input: SearchRAGPipe.Input,
        state: AsyncState,
        run_id: uuid.UUID,
        rag_generation_config: GenerationConfig,
        *args: Any,
        **kwargs: Any,
    ) -> AsyncGenerator[str, None]:
        iteration = 0
        context = ""
        # dump the search results and construct the context
        async for query, search_results in input.message:
            yield f"<{self.SEARCH_STREAM_MARKER}>"
            if search_results.vector_search_results:
                context += "Vector Search Results:\n"
                for result in search_results.vector_search_results:
                    if iteration >= 1:
                        yield ","
                    yield json.dumps(result.json())
                    context += (
                        f"{iteration + 1}:\n{result.metadata['text']}\n\n"
                    )
                    iteration += 1

            # FIXME: Add KG search results into RAG workflow
            # if search_results.kg_search_results:
            #     for result in search_results.kg_search_results:
            #         if iteration >= 1:
            #             yield ","
            #         yield json.dumps(result.json())
            #         context += f"Result {iteration+1}:\n{result.metadata['text']}\n\n"
            #         iteration += 1

            yield f"</{self.SEARCH_STREAM_MARKER}>"

            messages = self.prompt_provider._get_message_payload(
                system_prompt_name=self.config.system_prompt,
                task_prompt_name=self.config.task_prompt,
                task_inputs={"query": query, "context": context},
            )
            yield f"<{self.COMPLETION_STREAM_MARKER}>"
            response = ""
            for chunk in self.llm_provider.get_completion_stream(
                messages=messages, generation_config=rag_generation_config
            ):
                chunk = StreamingSearchRAGPipe._process_chunk(chunk)
                response += chunk
                yield chunk

            yield f"</{self.COMPLETION_STREAM_MARKER}>"

            await self.enqueue_log(
                run_id=run_id,
                key="llm_response",
                value=response,
            )

    async def _yield_chunks(
        self,
        start_marker: str,
        chunks: Generator[str, None, None],
        end_marker: str,
    ) -> str:
        yield start_marker
        for chunk in chunks:
            yield chunk
        yield end_marker

    @staticmethod
    def _process_chunk(chunk: LLMChatCompletionChunk) -> str:
        return chunk.choices[0].delta.content or ""
