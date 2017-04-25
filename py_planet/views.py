# -*- coding: utf8 -*-

import json
import logging

import requests
import telepot

from django.template.loader import render_to_string
from django.http import HttpResponseForbidden, HttpResponseBadRequest, JsonResponse
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.conf import settings

from .utils import parse_planetpy_rss

TelegramBot = telepot.Bot(settings.TELEGRAM_BOT_TOKEN)

logger = logging.getLogger('telegram.bot')


def _display_help():
    return render_to_string('help.md')


def _display_planetpy_feed():
    return render_to_string('feed.md', {'items': parse_planetpy_rss()})


def _display_kurs():
    url = "https://api.privatbank.ua/p24api/"
    url += "pubinfo?json&exchange&coursid=11"
    return render_to_string('kurs.md', {'kurs': requests.get(url).json()})


def _display_my_shows():
    return render_to_string('myshows.md')


def _display_weather(city='Lviv'):
    api_key = settings.WEATHER_API_KEY
    api_url = "http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&mode=json&appid={}".format(
        city, api_key)

    return render_to_string('weather.md', {'weather': requests.get(api_url).json()})


class CommandReceiveView(View):
    def post(self, request, bot_token):
        if bot_token != settings.TELEGRAM_BOT_TOKEN:
            return HttpResponseForbidden('Invalid token')

        commands = {
            '/start': _display_help,
            '/help': _display_help,
            '/feed': _display_planetpy_feed,
            '/kurs': _display_kurs,
            '/myshows': _display_my_shows,
            '/weather': _display_weather,
        }

        raw = request.body.decode('utf-8')
        logger.info(raw)

        try:
            payload = json.loads(raw)
        except ValueError:
            return HttpResponseBadRequest('Invalid request body')
        else:
            chat_id = payload['message']['chat']['id']
            cmd = payload['message'].get('text')  # command

            func = commands.get(cmd.split()[0].lower())
            if func:
                TelegramBot.sendMessage(chat_id, func(), parse_mode='Markdown')
            else:
                TelegramBot.sendMessage(chat_id, 'I do not understand you, walk on home, boy!')

        return JsonResponse({}, status=200)

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(CommandReceiveView, self).dispatch(request, *args, **kwargs)


