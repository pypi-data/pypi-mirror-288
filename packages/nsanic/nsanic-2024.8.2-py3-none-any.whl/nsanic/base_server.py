import asyncio

from sanic import Sanic
from tortoise.contrib.sanic import register_tortoise

from nsanic.base_conf import BaseConf
from nsanic.libs import consts


class InitServer:

    def __init__(
            self,
            conf,
            mws: (list, tuple) = None,
            bps: (list, tuple) = None,
            excps: (list, tuple) = None,
            start_evt: list = None,
            stop_evt: list = None):
        self.__conf: BaseConf = conf
        self.__conf.set_conf()
        consts.GLOBAL_TZ = conf.TIME_ZONE
        self.__evt_before_api = start_evt or []
        self.__evt_after_api = []
        self.__stop_evt = stop_evt or []
        self.__srv = Sanic(self.__conf.SERVER_NAME, log_config=self.__conf.log_conf())
        self.__srv.update_config(self.__conf)
        self.__bp_list = []
        if self.__conf.db_conf:
            register_tortoise(self.__srv, config=self.__conf.db_conf())
        for mdw_fun in mws or []:
            mdw_fun.set_conf(self.__conf)
            self.__srv.middleware(mdw_fun.main)
        for bp_cls in bps:
            bp_cls.set_conf(self.__conf)
            bp_cls.load_default_api()
            hasattr(bp_cls, 'init_loop_task') and self.__bp_list.append(bp_cls)
            self.__srv.blueprint(bp_cls.bpo)
        for expt_fun in excps or []:
            expt_fun.set_conf(self.__conf)
            self.__srv.error_handler.add(Exception, expt_fun.catch_req)
        self.__srv.register_listener(self.__after_server_start, 'after_server_start')
        self.__srv.register_listener(self.__before_server_stop, 'before_server_stop')

    async def __after_server_start(self, app, loop):
        if self.__conf.rds:
            self.__conf.rds.set_looping()
            await asyncio.sleep(0.5)
        for fun in self.__evt_before_api:
            (await fun(app, loop)) if asyncio.iscoroutinefunction(fun) else fun(app, loop)
        for bp_cls in self.__bp_list:
            bp_cls.init_loop_task()
        consts.GLOBAL_SRV_STATUS = True
        for fun in self.__evt_after_api:
            (await fun(app, loop)) if asyncio.iscoroutinefunction(fun) else fun(app, loop)

    async def __before_server_stop(self, app, loop):
        consts.GLOBAL_SRV_STATUS = False
        for fun in self.__stop_evt:
            await fun(app, loop)

    @property
    def main(self):
        return self.__srv

    def add_signal(self, signal_map: dict):
        """信号注册"""
        if not signal_map:
            return
        for k, v in signal_map.items():
            callable(v) and self.__srv.add_signal(v, k)

    def add_start_event(self, events, before=True):
        if callable(events):
            self.__evt_before_api.append(events) if before else self.__evt_after_api.append(events)
        if isinstance(events, (list, tuple)):
            self.__evt_before_api.extend(events) if before else self.__evt_after_api.extend(events)

    def add_stop_event(self, events):
        if callable(events):
            self.__stop_evt.append(events)
        if isinstance(events, (list, tuple)):
            self.__stop_evt.extend(events)

    def run(self, protocol=None):

        self.__srv.run(
            host=self.__conf.HOST,
            port=self.__conf.RUN_PORT,
            workers=self.__conf.RUN_WORKER if not self.__conf.RUN_FAST else 1,
            fast=self.__conf.RUN_FAST,
            debug=self.__conf.DEBUG_MODE,
            access_log=self.__conf.ACCESS_LOG,
            protocol=protocol
        )
