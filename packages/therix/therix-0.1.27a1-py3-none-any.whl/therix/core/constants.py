from enum import Enum
class DataSourceMaster:
    TEXT = "TEXT"
    PDF = "PDF"
    WEBSITE = "WEBSITE"
    DOCX = "DOCX"
    CSV = "CSV"
    DATABASE = "DATABASE"
    YOUTUBE="YOUTUBE"

class EmbeddingModelMaster:
    OPENAI_TEXT_ADA = 'text-embedding-ada-002'
    OPENAI_TEXT_EMBEDDING_3_LARGE = 'text-embedding-3-large'
    OPENAI_TEXT_EMBEDDING_3_SMALL = 'text-embedding-3-small'
    AZURE_TEXT_ADA='text-embedding-ada-002'
    AZURE_TEXT_EMBEDDING_3_LARGE = 'text-embedding-3-large'
    AZURE_TEXT_EMBEDDING_3_SMALL = 'text-embedding-3-small'
    BEDROCK_TITAN_EMBEDDING='amazon.titan-embed-text-v1'
    BEDROCK_TITAN_MULTIMODAL_EMBEDDING='amazon.titan-embed-image-v1'
    GEMINI_EMBEDDING='models/embedding-001'

class InferenceModelMaster:
    OPENAI_GPT_4_TURBO_PREVIEW = 'gpt-4-turbo-preview'
    OPENAI_GPT_4 = 'gpt-4'
    OPENAI_GPT_4_O = 'gpt-4o'
    OPENAI_GPT_4_O_MINI = 'gpt-4o-mini'
    OPENAI_GPT_3_5_TURBO = 'gpt-3.5-turbo'
    OPENAI_GPT_3_5_TURBO_INSTRUCT = 'gpt-3.5-turbo-instruct'
    AZURE_GPT_4_TURBO_PREVIEW = 'gpt-4-turbo-preview'
    AZURE_GPT_4 = 'gpt-4'
    AZURE_GPT_4_O = 'gpt-4o'
    AZURE_GPT_3_5_TURBO = 'gpt-3.5-turbo'
    AZURE_GPT_3_5_TURBO_INSTRUCT = 'gpt-3.5-turbo-instruct'
    GROQ_LLM_MIXTRAL_8_7_B='mixtral-8x7b-32768'
    GROQ_LLM_LLAMA3_70B= 'llama3-70b-8192'
    GROQ_LLM_GEMMA7B= 'gemma-7b-it'
    GROQ_LLM_LLAMA3_8B= 'llama3-8b-8192'
    GROQ_LLM_LLAMA3_1_8B= 'llama-3.1-8b-instant'
    GROQ_LLM_LLAMA3_1_70B= 'llama-3.1-70b-versatile'
    GROQ_LLM_LLAMA3_1_405B= 'llama-3.1-405b-reasoning'
    BEDROCK_TEXT_EXPRES_V1='amazon.titan-text-express-v1'
    BEDROCK_TEXT_LITE_G1='amazon.titan-text-lite-v1'
    GOOGLE_GEMINI_PRO='gemini-pro'
    GOOGLE_GEMINI_1_5_PRO='gemini-1.5-pro'
    ANTHROPIC_CLAUDE_3_OPUS='claude-3-opus-20240229'
    ANTHROPIC_CLAUDE_2_1='claude-2.1'

class OutputSourceMaster:
    S3 = "S3"
    LOCAL = "LOCAL"
    DATABASE = "DATABASE"


class ChatMessage(Enum):
    CHAT_SAVED = "Message saved successfully!"
    CHAT_FAILED = "Error saving message"
    FAILED_TO_RETRIEVE = "Error retrieving message history"

class PipelineTypeMaster(Enum):
    RAG = 'RAG'
    SUMMARIZER = 'SUMMARIZER'
    DEFAULT = 'DEFAULT'
    
class API_Endpoint:
    EMBEDDING_ENDPOINT = "https://cloud-api.therix.ai/api/sdk/embedding" 
    CHAT_HISTORY_ENDPOINT = "https://cloud-api.therix.ai/api/sdk/chat-history/"
    BASE_URL = "https://cloud-api.therix.ai/api/sdk/"