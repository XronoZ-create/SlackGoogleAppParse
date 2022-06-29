import requests
from PIL import Image
from imgur_python import Imgur
from config import Config


def get_concat_h_multi_resize(im_list, resample=Image.BICUBIC):
    min_height = min(im.height for im in im_list)
    im_list_resize = [im.resize((int(im.width * min_height / im.height), min_height),resample=resample)
                      for im in im_list]
    total_width = sum(im.width for im in im_list_resize)
    dst = Image.new('RGB', (total_width, min_height))
    pos_x = 0
    for im in im_list_resize:
        dst.paste(im, (pos_x, 0))
        pos_x += im.width
    return dst

def get_concat_v_multi_resize(im_list, resample=Image.BICUBIC):
    min_width = min(im.width for im in im_list)
    im_list_resize = [im.resize((min_width, int(im.height * min_width / im.width)),resample=resample)
                      for im in im_list]
    total_height = sum(im.height for im in im_list_resize)
    dst = Image.new('RGB', (min_width, total_height))
    pos_y = 0
    for im in im_list_resize:
        dst.paste(im, (0, pos_y))
        pos_y += im.height
    return dst

def get_concat(im_list):
    w, h = im_list[0].size
    if h > w:
        dst = get_concat_h_multi_resize(im_list)
    else:
        dst = get_concat_v_multi_resize(im_list)
    return dst

class Message:
    def __init__(self, name: str, href: str, developer: str, screenshots: list, video: str, already_send: bool, text=None, screenshots_href=None):
        self.name = name
        self.href = href
        self.developer = developer
        self.screenshots = screenshots
        self.video = video
        self.already_send = already_send
        self.text = text
        self.imgur_client = Imgur({'client_id': Config.IMGUR_CLIENT_ID, 'access_token': Config.IMGUR_ACCESS_TOKEN})
        self.screenshots_href = screenshots_href

    @property
    def block(self):
        if not self.text:
            self.text = f"🎮 <https://play.google.com/store/apps/details?id=net.DuckyGames.PetIdle| {self.name}> \n " \
                        f"👤 *Разработчик*: {self.developer} "
            if self.video:
                self.text += f"<{self.video}| >"

        self.block_message = [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": self.text
                }
            }
        ]
        self.jpg_screenshots = []
        if self.screenshots and not self.video and not self.screenshots_href:
            #  если есть скриншоты и нет видео. Действие не от кнопки(screenshots_href - нет ссылки на общий скриншот)
            self.num_screen = 0
            for self.one_screen in self.screenshots:
                self.r = requests.get(self.one_screen, allow_redirects=True)
                with open(f'test_{self.num_screen}.jpg', 'wb') as self.jpg_file:
                    self.jpg_file.write(self.r.content)
                self.jpg_screenshots.append(Image.open(f'test_{self.num_screen}.jpg'))
                self.num_screen += 1
            get_concat(self.jpg_screenshots).save('combine.jpg')
            self.url_image = self.imgur_client.image_upload('combine.jpg', self.name, self.developer)['response']['data']['link']
            self.block_message.append(
                {
                    "type": "divider"
                }
            )
            self.block_message.append(
                {
                    "type": "image",
                    "image_url": self.url_image,
                    "alt_text": "inspiration"
                }
            )
            self.block_message.append(
                {
                    "type": "divider"
                }
            )
        elif self.screenshots_href:
            # действие от кнопки. Есть ссылка на общий скриншот
            self.block_message.append(
                {
                    "type": "divider"
                }
            )
            self.block_message.append(
                {
                    "type": "image",
                    "image_url": self.screenshots_href,
                    "alt_text": "inspiration"
                }
            )
            self.block_message.append(
                {
                    "type": "divider"
                }
            )
        if not self.already_send:
            self.block_message.append(
                {
                    "type": "actions",
                    "elements": [
                        {
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "text": "📫 Send to Google Sheets",
                                "emoji": True
                            },
                            "value": "to_sheets",
                            "action_id": "actionId-0"
                        }
                    ]
                }
            )
        return self.block_message
