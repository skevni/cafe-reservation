from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    api_title: str = 'Бронирование мест в кафе'
    api_description: str = (
        'Сервис для управления бронированием мест в кафе, просмотром и '
        'предварительным заказом меню, просмотром действующих акций'
    )
    database_url: str = 'sqlite+aiosqlite:///./cafe_reserv.db'
    secret_key: str = 'rhcqHcKjoMsksffAa2-Uh3E3sNepKBp#OOsbtIzogNA'

    model_config = SettingsConfigDict(env_file='.env')


settings = Settings()
