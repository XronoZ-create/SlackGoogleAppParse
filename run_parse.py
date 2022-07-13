from db import SessionLocal, Base, engine
from db_models import GoogleApp, AndroidDevelopHref, IosApp, IosDevelopHref
from google_play_scraper import app
from modules.google_play import DeveloperFindApp
from slack_package.slack_methods import send_slack_message
from slack_package.model_message import Message
from loguru import logger
import time
from itunes_app_scraper.scraper import AppStoreScraper

@logger.catch
def run_google_play():
    db = SessionLocal()
    developer_find_app = DeveloperFindApp()
    all_develop = db.query(AndroidDevelopHref).filter_by().all()
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
                                already_send=False,
                                platform='Android'
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

@logger.catch
def run_app_store():
    db = SessionLocal()
    scraper = AppStoreScraper()
    all_develop = db.query(IosDevelopHref).filter_by().all()
    for develop in all_develop:
        try:
            list_app = scraper.get_app_ids_for_developer(developer_id=int(develop.develop_id))
            for one_app in list_app:
                if db.query(IosApp).filter_by(app_id=one_app).first() == None:
                    try:
                        if develop.count_parse != 0:
                            result = scraper.get_app_details(one_app, country='us')

                            block = Message(
                                name=result['trackName'],
                                href=result['trackViewUrl'],
                                developer=result["artistName"],
                                screenshots=result['screenshotUrls'].split(','),
                                video=None,
                                already_send=False,
                                platform='IOS'
                            ).block
                            send_slack_message(block=block)
                        new_app = IosApp(app_id=one_app, develop_id=develop.develop_id)
                        db.add(new_app)
                        db.commit()
                    except:
                        logger.exception(f"ErrorApp: {one_app}")
            develop.count_parse += 1
            db.commit()
        except:
            logger.exception(f"ErrorDevelop: {develop.develop_id}")


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    logger.add("debug.log", format="{time} {level} {message}", level="DEBUG", rotation="10 MB")

    run_google_play()
    run_app_store()
