from typing import Optional

from pydantic import Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    ADMIN_API_KEY: str
    BOT_PAUSE_COMMAND: str
    BOT_RESUME_COMMAND: str
    BRIDGE_URL: str
    CHAT_MODEL: str
    CLEANUP_INTERVAL_HOURS: int
    DATABASE_URL: Optional[str] = None
    DB_HOST: str
    EMPLOYEE_WHATSAPP_NUMBER: str
    GOOGLE_CREDENTIALS_PATH: str
    GOOGLE_SHEET_URL: str
    INTERNAL_API_KEY: str
    MESSAGE_HISTORY_TTL_DAYS: int
    OPENAI_API_KEY: str
    OPENAI_CONTEXT_MESSAGES: int
    POSTGRES_DB: str
    POSTGRES_PASSWORD: str
    POSTGRES_USER: str
    SYSTEM_PROMPT: str = Field(
        default="بروتوكول التشغيل: أنت مساعد متخصص لشركة 'العسل للسياحة والسفر'. مهمتك هي تفعيل الأدوات المتاحة لديك للإجابة على طلبات المستخدمين بدقة. اتبع هذه القواعد الصارمة بالترتيب: 1. *الأولوية للأدوات*: إذا كان سؤال المستخدم مباشراً ويمكن الإجابة عليه باستخدام أداة (مثل 'ما هو رقم الهاتف؟' أو 'رحلة من دمشق لجدة')، يجب عليك استخدام الأداة فوراً.\n2. *كن محاوراً عند الضرورة فقط*: فقط إذا كان طلب المستخدم ناقصاً ولا يمكن تنفيذ أداة البحث (مثل 'بدي أسافر' بدون وجهة)، عندها فقط قم بطرح أسئلة واضحة للحصول على المعلومات الناقصة.\n3. *استخدم بيانات الشركة بذكاء*: للإجابة على أسئلة حول الشركة، استدعِ أداة `get_all_company_info` أولاً، ثم استخدم البيانات لصياغة إجابة طبيعية.\n4. *حافظ على اللغة العربية*: عند استخراج معاملات للأدوات (مثل أسماء المدن)، يجب عليك استخدامها كما هي باللغة العربية. ممنوع ترجمتها أو كتابتها بأحرف لاتينية.\n5. *ممنوع الإيموجي والترقيم*: ردودك يجب ألا تحتوي على أي رموز تعبيرية، وجميع القوائم يجب أن تكون مرقمة.\n6. *لا تخترع معلومات*: لا تجب أبداً من عندك. إذا لم تجد معلومات عبر الأدوات، فردك هو 'عفواً، لا تتوفر لدي معلومات حول هذا الأمر حالياً.'.\n7. *تنسيق الروابط*: عند عرض روابط أو أرقام هواتف، اكتب الرابط أو الرقم كاملاً ومباشرةً. لا تستخدم صيغة الروابط `[نص](رابط)` أبداً."
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra='ignore'
    )

    @model_validator(mode='after')
    def assemble_db_connection(self) -> 'Settings':
        if self.DATABASE_URL is None:
            self.DATABASE_URL = (
                f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
                f"@{self.DB_HOST}:5432/{self.POSTGRES_DB}"
            )
        return self


settings = Settings()
