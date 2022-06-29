from db import SessionLocal, Base, engine
from db_models import GoogleApp, DevelopHref
from google_play_scraper import app
from modules.google_play import DeveloperFindApp
from slack_package.slack_methods import send_slack_message
from slack_package.model_message import Message
from loguru import logger
import time

@logger.catch
def run():
    db = SessionLocal()
    developer_find_app = DeveloperFindApp()
    all_develop = db.query(DevelopHref).filter_by().all()
    for develop in all_develop:
        try:
            list_app = developer_find_app.find_app(dev_href=develop.develop_href)
            for one_app in list_app:
                if db.query(GoogleApp).filter_by(app_id=one_app).first() == None:
                    try:
                        if develop.count_parse != 0:
                            result = app(one_app, lang='en', country='us')

                            block = Message(
                                name=result['title'],
                                href=result['url'],
                                developer=result["developer"],
                                screenshots=result['screenshots'],
                                video=result['video'],
                                already_send=False
                            ).block
                            send_slack_message(block=block)
                        new_app = GoogleApp(app_id=one_app, develop_href=develop.develop_href)
                        db.add(new_app)
                        db.commit()
                    except:
                        logger.exception(f"ErrorApp: {one_app}")
            develop.count_parse += 1
            db.commit()
        except:
            logger.exception(f"ErrorDevelop: {develop.develop_href}")
    developer_find_app._end()

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    logger.add("debug.log", format="{time} {level} {message}", level="DEBUG", rotation="10 MB")

    run()
