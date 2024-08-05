"""
Proompter

Wrapper for llm calls, meant for experimentation with different prompt and history 
handling strategies.
"""

import logging
import asyncio 
import time
from transformers import AutoTokenizer #==4.43.2
from huggingface_hub import login #==0.24.2
from typing import Any, AnyStr, Union, Optional, Sequence, Mapping, Literal, overload, Callable, Dict
import attrs #==23.2.0
import attrs #==23.2.0
from typing import Any, AnyStr, Union, Optional, Sequence, Mapping, Literal, overload, Callable, Dict
import pandas as pd #==2.1.1
from mocker_db import MockerDB #==0.2.0
from ollama import AsyncClient, Client #==0.2.1
from typing import Any, AnyStr, Union, Optional, Sequence, Mapping, Literal, overload, Callable, Dict

__design_choices__ = {}

@attrs.define
class PromptHandler():

    """
    PromptHandler prepares inputs for the llm requests.
    """

    template : Optional[dict] = attrs.field(default=None)

    # Logger settings
    logger = attrs.field(default=None)
    logger_name = attrs.field(default='Prompt Handler Async')
    loggerLvl = attrs.field(default=logging.INFO)
    logger_format = attrs.field(default=None)

    def __attrs_post_init__(self):
        self._initialize_logger()

    def _initialize_logger(self):

        """
        Initialize a logger for the class instance based on the specified logging level and logger name.
        """

        if self.logger is None:
            logging.basicConfig(level=self.loggerLvl, format=self.logger_format)
            logger = logging.getLogger(self.logger_name)
            logger.setLevel(self.loggerLvl)

            self.logger = logger

    def apply_template(self, 
                       messages : list, 
                       template : dict = None):

        """
        Transforms messages according to prompt templates.
        """

        if template is None:
            template = self.template

        if template is None:
            return messages

        messages = messages.copy()

        return [{'role': message['role'],
                'content': template.get(message['role'], 
                "{content}").format(content=message['content'])}
            for message in messages
        ]

@attrs.define
class PromptStrategyHandler():

    """
    PromptStrategyHandler defines how to deal with single prompt call.
    """

    strategy_name : Optional[str] = attrs.field(default=None)
    strategy_params : Optional[dict] = attrs.field(default={})

    # Outputs
    responses : Optional[list] = attrs.field(default=[])
    last_responses : Optional[list] = attrs.field(default=[])

    # Logger settings
    logger = attrs.field(default=None)
    logger_name = attrs.field(default="Prompt Strategy Handler")
    loggerLvl = attrs.field(default=logging.INFO)
    logger_format = attrs.field(default=None)

    def __attrs_post_init__(self):
        self._initialize_logger()

    def _initialize_logger(self):

        """
        Initialize a logger for the class instance based on the specified logging level and logger name.
        """

        if self.logger is None:
            logging.basicConfig(level=self.loggerLvl, format=self.logger_format)
            logger = logging.getLogger(self.logger_name)
            logger.setLevel(self.loggerLvl)

            self.logger = logger

    async def _call_n_times(self, 
                            function: Callable, 
                            n_calls : int, 
                            *args, **kwargs):

        """
        Calls provided function n times.
        """

        response_calls = [function(*args, **kwargs) for _ in range(n_calls)]

        responses = await asyncio.gather(*response_calls)

        self.responses += responses
        self.last_responses = responses

        return responses

    
    async def most_common_output_of_3(self, 
                          function: Callable, 
                          strategy_params : dict, 
                          *args, **kwargs) -> Dict[str, Any]:

        """
        Calls function a given number of times and selects output
        of minimal length.
        """

        n_calls = 3

        responses = await self._call_n_times(
            function = function, 
            n_calls = n_calls, 
            *args, **kwargs)

        contents = [response['message']['content'] \
            for response in responses]

        
        # use mocker to find pair that is the closes according to cosine dist

        hh = MockerDB(
            embedder_params = {
                'model_name_or_path' : 'intfloat/multilingual-e5-base',
                'processing_type' : 'batch',
                'tbatch_size' : 500})

        hh.establish_connection()

        insert = [{
            'collection' : 'responses',
            'text' : text,
            'id' : rid} for text, rid in zip(contents, range(n_calls))]

        hh.insert_values(values_dict_list=insert,
                        var_for_embedding_name='text',
                        embed=True)

        records = []
        for text in contents:
            text2 = hh.search_database(query = text,
                                    filter_criteria={
                                        "collection" : "responses",
                                    },
                            return_keys_list=['text', 'id'],
                            search_results_n=2)

            #texts = [t['text'] for t in text2]

            records.append({
                'distance' : hh.results_dictances[1],
                'query' : text2[0]['text'],
                'id' : text2[0]['id']
            })

        # sorting ascending by distance (to pop later)
        rddf = pd.DataFrame(records).sort_values(
            by='distance',ascending=True)

        # extracting most_commonm_response_id
        most_commonm_response_id = rddf['id'].to_list().pop()

        return responses[most_commonm_response_id]


    async def min_output_length(self, 
                          function: Callable, 
                          strategy_params : dict, 
                          *args, **kwargs) -> Dict[str, Any]:

        """
        Calls function a given number of times and selects output
        of minimal length.
        """

        n_calls = max(strategy_params.get('n_calls', 2), 2)

        responses = await self._call_n_times(
            function = function, 
            n_calls = n_calls, 
            *args, **kwargs)

        contents = [response['message']['content'] \
            for response in responses]

        min_content = min(contents, key=len)

        # Find the response with the min content
        min_response = next(response for response in responses \
            if response['message']['content'] == min_content)
        return min_response

    async def max_output_length(self, 
                                function: Callable, 
                                strategy_params: dict, 
                                *args, **kwargs) -> Dict[str, Any]:
        """
        Calls function a given number of times and selects output of maximal length.
        """
        n_calls = max(strategy_params.get('n_calls', 2), 2)

        responses = await self._call_n_times(
            function=function, 
            n_calls=n_calls, 
            *args, **kwargs
        )

        contents = [response['message']['content'] for response in responses]
        max_content = max(contents, key=len)

        # Find the response with the max content
        max_response = next(response for response in responses if response['message']['content'] == max_content)
        return max_response

    async def last_call(self, 
                        function: Callable,
                        strategy_params: dict, 
                        *args, **kwargs) -> Dict[str, Any]:
        """
        Calls function a given number of times and selects output of maximal length.
        """
        n_calls = max(strategy_params.get('n_calls', 1), 1)

        responses = await self._call_n_times(
            function=function, 
            n_calls=n_calls, 
            *args, **kwargs
        )

        return responses[-1]

        
    async def call_async(self, 
             function: Callable, 
             strategy_name: Optional[str]= None, 
             strategy_params: Optional[dict] = None,
             *args, **kwargs) -> Any:

        """
        Calls a given function with selected strategy.
        """

        if strategy_name is None:
            strategy_name = self.strategy_name

        if strategy_params is None:
            strategy_params = self.strategy_params

        if strategy_name:

            strategy_name = getattr(self, strategy_name, None)
            if callable(strategy_name):
                return await strategy_name(
                    function = function, 
                    strategy_params=strategy_params,
                    *args, **kwargs)
            else:
                raise AttributeError(f"Strategy '{strategy_name}' not found")            
        else:
            return await function(*args, **kwargs)

@attrs.define
class OllamaHandlerAsync(AsyncClient):

    """
    OllamaHandlerAsync is a simple connector to ollama.AsyncClient
    meant to with LlmHandlerAsync in the role of llm_handler.
    """

    connection_string: Optional[str] = attrs.field(default=None)

    model_name : Optional[str] = attrs.field(default=None)

    # Logger settings
    logger = attrs.field(default=None)
    logger_name = attrs.field(default="Ollama Handler Async")
    loggerLvl = attrs.field(default=logging.INFO)
    logger_format = attrs.field(default=None)

    # Passthrough options
    kwargs: dict = attrs.field(factory=dict)
    
    def __attrs_post_init__(self):
        super().__init__(host=self.connection_string, **self.kwargs)
        self._initialize_logger()

    def _initialize_logger(self):

        """
        Initialize a logger for the class instance based on the specified logging level and logger name.
        """

        if self.logger is None:
            logging.basicConfig(level=self.loggerLvl, format=self.logger_format)
            logger = logging.getLogger(self.logger_name)
            logger.setLevel(self.loggerLvl)

            self.logger = logger


    async def chat(self,
                    messages : list, 
                model_name : str = None):

        """
        Async chat method from ollama.AsyncClient extended with message history and optional token usage counter.
        """
        
        # request chat
        response = await super().chat(
            model=model_name or self.model_name, 
            messages=messages)


        return response

    async def chat_stream(self,
                    messages : list, 
                model_name : str = None):

        """
        Async stream chat method from ollama.AsyncClient extended with message history and optional token usage counter,
        returns generator.
        """
        
        # request chat
        response = await super().chat(
            model=model_name or self.model_name, 
            messages=messages,
            stream = True)


        async for chunk in response:
            yield chunk['message']['content']


    async def generate(self,
                    prompt : str, 
                model_name : str = None):

        """
        Async chat method from ollama.AsyncClient extended with message history and optional token usage counter.
        """
        
        # request chat
        response = await super().generate(
            model=model_name or self.model_name, 
            prompt=prompt)


        return response

# Metadata for package creation
__package_metadata__ = {
    "author": "Kyrylo Mordan",
    "author_email": "parachute.repo@gmail.com",
    "description": "Simple wrapper around some Llm handlers.",
}



@attrs.define
class HfTokenizerHandler():

    """
    HfTokenizerHandler is a wrapper to use Tokenizers from Huggingface.
    """

    access_token : Optional[str] = attrs.field(default=None)
    use_auth_token : Optional[bool] = attrs.field(default=None)
    tokenizer_name : Optional[str] = attrs.field(default=None)

    tokenizer = attrs.field(default=None)

    # Logger settings
    logger = attrs.field(default=None)
    logger_name = attrs.field(default='HF Tokenizer')
    loggerLvl = attrs.field(default=logging.INFO)
    logger_format = attrs.field(default=None)

    def __attrs_post_init__(self):
        self._initialize_logger()

        # authenticate to access hugginface
        if self.access_token:
            login(self.access_token)
            self.use_auth_token = True
        else:
            self.use_auth_token = False

    def _initialize_logger(self):

        """
        Initialize a logger for the class instance based on the specified logging level and logger name.
        """

        if self.logger is None:
            logging.basicConfig(level=self.loggerLvl, format=self.logger_format)
            logger = logging.getLogger(self.logger_name)
            logger.setLevel(self.loggerLvl)

            self.logger = logger

    def tokenize(self, text : str):

        """
        Tokenize text.
        """

        if self.tokenizer is None:
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.tokenizer_name, 
                use_auth_token = self.use_auth_token)
        

        return self.tokenizer.tokenize(str(text))


@attrs.define
class Proompter():

    """
    Proompter is meant as a wrapper around some Llm handlers.
    Its purpose is to serve as extension component that abstract their usage.

    Proompter consists of multiple dependecies, which could be initialized and passed to the class externally or parameters could be passed for class to initialize them.

    These include:

        - LLM handler: makes calls to llm
        - Prompt handler: prepares input based on templates
        - Prompt strategy handler: contains ways to call llm handler with selected strategy
        - Tokenizer handler: tokenizes text
    """

    # Dependencies
    llm_handler_class = attrs.field(default=OllamaHandlerAsync)
    prompt_handler_class = attrs.field(default=PromptHandler)
    tokenizer_handler_class = attrs.field(default=HfTokenizerHandler)
    call_strategy_handler_class = attrs.field(default=PromptStrategyHandler)

    # Instances
    llm_handler_h = attrs.field(default=None)
    tokenizer_h = attrs.field(default=None)
    prompt_h = attrs.field(default=None)
    call_strategy_h = attrs.field(default=None)

    # Dependecies params
    llm_h_params = attrs.field(default={})
    prompt_h_params = attrs.field(default={})
    call_strategy_h_params = attrs.field(default={})
    tokenizer_h_params = attrs.field(default={})

    # Chat history
    messages : Optional[list] = attrs.field(default=None)
    responses : Optional[list] = attrs.field(default=[])

    # Logger settings
    logger = attrs.field(default=None)
    logger_name = attrs.field(default='Llm Handler Async')
    loggerLvl = attrs.field(default=logging.INFO)
    logger_format = attrs.field(default=None)
    
    def __attrs_post_init__(self):

        self._initialize_logger()
        self._initialize_llm_handler()
        self._initialize_prompt_handler()
        self._initialize_call_strategy_handler()
        self._initialize_tokenizer_handler()


    def _initialize_logger(self):

        """
        Initialize a logger for the class instance based on the specified logging level and logger name.
        """

        if self.logger is None:
            logging.basicConfig(level=self.loggerLvl, format=self.logger_format)
            logger = logging.getLogger(self.logger_name)
            logger.setLevel(self.loggerLvl)

            self.logger = logger

    def _initialize_llm_handler(self):

        """
        Initialize llm handler instance with provided parameters
        """

        if self.llm_handler_h is None:

            self.llm_handler_h = self.llm_handler_class(
                **self.llm_h_params,
                logger = self.logger
            )

    def _initialize_prompt_handler(self):

        """
        Initialize prompt handler instance with provided parameters
        """

        if self.prompt_h is None:
            self.prompt_h = self.prompt_handler_class(
                **self.prompt_h_params,
                logger = self.logger
            )

    def _initialize_call_strategy_handler(self):

        """
        Initialize call stetegy handler instance with provided parameters
        """

        self.call_strategy_h = self.call_strategy_handler_class(
            **self.call_strategy_h_params,
            logger = self.logger
        )

    def _initialize_tokenizer_handler(self):

        """
        Initialize llm handler instance with provided parameters
        """

        if self.tokenizer_h_params != {}:

            self.tokenizer_h = self.tokenizer_handler_class(
                **self.tokenizer_h_params,
                logger = self.logger)
        
    def estimate_tokens(self, text : str):

        """
        Estimate number of tokens for provided text with defined tokenizer
        """

        if self.tokenizer_h:
            return len(self.tokenizer_h.tokenize(text = text))
        else:
            self.logger.warning("Tokenizer was not defined, estimation will be skipped!")
            return None

    async def prompt_chat(self,
                    messages : list, 
                    model_name : str = None,
                    prompt_templates : dict = None,
                    call_strategy_name : str = None,
                    call_strategy_params : dict = None):

        """
        Async prompt method extended with message history and optional token usage counter.
        """

        if prompt_templates is None:
            prompt_templates = self.prompt_h_params.get(
                'template', None)

        if model_name is None: 
            model_name = self.llm_h_params.get(
                'model_name', None) 

        if call_strategy_name is None:
            call_strategy_name = self.call_strategy_h_params.get(
                'strategy_name', None)

        if call_strategy_params is None:
            call_strategy_params = self.call_strategy_h_params.get(
                'strategy_params', None)

        messages = messages.copy()

        # apply prompt template
        processed_messages = self.prompt_h.apply_template(
            messages=messages,
            template=prompt_templates)


        # prompting chat
        start_time = time.time()
        response = await self.call_strategy_h.call_async(
            function = self.llm_handler_h.chat,
            strategy_name = call_strategy_name,
            strategy_params = call_strategy_params,
            messages = processed_messages, 
            model_name = model_name
        ) 
        end_time = time.time()

        # save response time
        response['response_time'] = end_time - start_time

        # save message history
        messages.append(response['message'])
        response['messages'] = self.prompt_h.apply_template(
            messages=messages,
            template=prompt_templates)


        # calculating token usage
        input_tokens = self.estimate_tokens(text=messages)
        output_tokens = self.estimate_tokens(text=response['message']['content'])
        
        if input_tokens and output_tokens:
            total_tokens = input_tokens + output_tokens
        else:
            total_tokens = None

        response['input_tokens'] = input_tokens
        response['output_tokens'] = output_tokens
        response['total_tokens'] = total_tokens

        # saving responses
        self.messages = messages
        self.responses.append(response)

        return response

    async def prompt_instruct(self,
                    prompt : list, 
                    model_name : str = None,
                    call_strategy_name : str = None,
                    call_strategy_params : dict = None):

        """
        Async prompt method to run instruct models.
        """

        if model_name is None: 
            model_name = self.llm_h_params.get(
                'model_name', None) 

        if call_strategy_name is None:
            call_strategy_name = self.call_strategy_h_params.get(
                'strategy_name', None)

        if call_strategy_params is None:
            call_strategy_params = self.call_strategy_h_params.get(
                'strategy_params', None)

        # prompting chat
        start_time = time.time()
        response = await self.call_strategy_h.call_async(
            function = self.llm_handler_h.generate,
            strategy_name = call_strategy_name,
            strategy_params = call_strategy_params,
            prompt = prompt, 
            model_name = model_name
        ) 
        end_time = time.time()

        # save response time
        response['response_time'] = end_time - start_time

        # calculating token usage
        input_tokens = self.estimate_tokens(text=prompt)
        output_tokens = self.estimate_tokens(text=response['response'])
        
        if input_tokens and output_tokens:
            total_tokens = input_tokens + output_tokens
        else:
            total_tokens = None

        response['input_tokens'] = input_tokens
        response['output_tokens'] = output_tokens
        response['total_tokens'] = total_tokens

        # saving responses
        self.responses.append(response)

        return response

    async def prompt_chat_parallel(self,
                                    messages : list, 
                                    model_name : str = None,
                                    prompt_templates : dict = None,
                                    call_strategy_name : str = None,
                                    call_strategy_params : dict = None):

        """
        Async prompt method that processes each message independently in parallel
        """

        messages = messages.copy()
        
        response_calls = [self.prompt_chat(messages = messages_list, 
                                    model_name = model_name,
                                    prompt_templates = prompt_templates,
                                    call_strategy_name = call_strategy_name,
                                    call_strategy_params = call_strategy_params) \
                                        for messages_list in messages]

        responses = await asyncio.gather(*response_calls)                            

        return responses

    async def prompt_instruct_parallel(self,
                                    prompts : list, 
                                    model_name : str = None,
                                    call_strategy_name : str = None,
                                    call_strategy_params : dict = None):

        """
        Async prompt method that processes each prompt independently in parallel
        """
        
        response_calls = [self.prompt_instruct(prompt = prompt, 
                                    model_name = model_name,
                                    call_strategy_name = call_strategy_name,
                                    call_strategy_params = call_strategy_params) \
                                        for prompt in prompts]

        responses = await asyncio.gather(*response_calls)                            

        return responses

    async def chat(self, 
                   prompt : str, 
                   new_dialog : bool = False):

        """
        Async chat method to pass new prompts and manage history.
        """


        if self.messages is None:
            messages = []
        else:
            messages = self.messages.copy()

        if new_dialog:
            messages = []

        messages.append({'role': 'user', 'content': prompt})

        response = await self.prompt_chat(
            messages = messages)

        return response['message']['content']

    async def chat_stream(self, prompt: str, 
                          new_dialog: bool = False):
        """
        Async chat method to pass new prompts and manage history.
        """
        if new_dialog or self.messages is None:
            messages = []
            self.messages = []
        else:
            messages = self.messages.copy()

        messages.append({'role': 'user', 'content': prompt})

        full_message = ''
        async for message in self.llm_handler_h.chat_stream(messages=messages):
            full_message += message
            # Yield the message for streaming
            yield message

        # Append the response from the assistant to the messages list
        messages.append({'role': 'assistant', 'content': full_message})
        # Update the class-level message history
        self.messages = messages