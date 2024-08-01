import asyncio
import logging
import time
import traceback
from typing import List, Optional, Union
from urllib.parse import urlparse

import aio_pika
import aiormq
from httpx import AsyncClient
from pydantic import BaseModel

from ..logger import logger
from ..stoppable import Stoppable
from .types import QueueRole, QueueRoutedMessage, QueueMessage


class RestAPI:
    def __init__(self, connection_url):
        p = urlparse(connection_url)
        # TODO: port should be configurable
        self.url = f"http://{p.username}:{p.password}@{p.hostname}:15672/api/"

        logging.getLogger("httpx").setLevel(logging.WARNING)  # disable verbose logging when global level is INFO

    async def get_queue(self, queue_name):
        async with AsyncClient() as client:
            r = await client.get(f"{self.url}queues/%2f/{queue_name}")
            q = r.json()
            # print(q)
            return q


class RabbitmqParams(BaseModel):
    exchange_type: Optional[aio_pika.ExchangeType] = aio_pika.ExchangeType.DIRECT
    exchange_name: Optional[str] = None
    routing_key: Optional[Union[str, List[str]]] = None
    prefetch_count: Optional[int] = 1
    exclusive: Optional[bool] = False
    x_max_priority: Optional[int] = None


class RabbitmqQueue(Stoppable):
    connection: aio_pika.robust_connection.AbstractRobustConnection
    internal_queue: asyncio.Queue
    # channel_invalid_state_flag: asyncio.Event
    # channel: aio_pika.abc.AbstractChannel
    receiver_queue: aio_pika.abc.AbstractQueue
    queue_name: Optional[str]
    exchange_name: Optional[str]

    def __init__(
        self,
        role: QueueRole,
        connection_url: str,
        queue_name: Optional[str] = None,
        params: Optional[RabbitmqParams] = RabbitmqParams(),
    ):
        super().__init__()
        self.role = role
        self.url = connection_url
        self.params = params
        self.queue_name = queue_name
        self.internal_queue = asyncio.Queue()
        self.ready_state = {self.role: asyncio.Event()}  # dict is for future: may support both server+client
        self.rest_api = RestAPI(self.url)
        # self.channel_invalid_state_flag = asyncio.Event()

    async def run(self):
        # logger.info( f'{id(self.role)=} {id(QueueRole.Receiver)=} {id(QueueRole.Publisher)=}' )
        if self.role == QueueRole.Publisher:
            self.tasks.append(asyncio.create_task(self.publisher_loop()))
        elif self.role == QueueRole.Receiver:
            self.tasks.append(asyncio.create_task(self.receiver_loop()))
        else:
            raise Exception(f"BUG: unimplemented role {self.role}")
        await super().run()

    async def stop(self):
        # logger.info( f'rabbitmq {self.internal_queue.qsize()=}')
        # if self.internal_queue.qsize() > 0:
        #     logger.info("rabbitmq joining internal queue")
        #     await self.internal_queue.join()
        #     logger.info("rabbitmq joined internal queue")
        # logger.info("rabbitmq stopping super")
        await super().stop()
        # logger.info("rabbitmq super stopped")

    async def push(self, data):
        # logger.info(f'rabbitmq {self.queue_name} push')
        await self.internal_queue.put(data)
        # logger.info(f'rabbitmq {self.queue_name} pushed')

    async def pop(self, timeout=None) -> QueueMessage | None:
        if timeout is None:
            # logger.info(f'rabbitmq pop {self.queue_name} no timeout')
            res = await self.internal_queue.get()
            # logger.info(f'rabbitmq {self.queue_name} poped {res}')
            return res
        try:
            res = await asyncio.wait_for(self.internal_queue.get(), timeout)
            return res
        except asyncio.TimeoutError:
            return None

    async def until_empty(self):
        last_log = 0
        while True:
            # is internal queue empty?
            if self.internal_queue.empty():
                # if receiver then is receiver queue empty?
                if self.role == QueueRole.Receiver:
                    queue = await self.rest_api.get_queue(self.queue_name)
                    if "message_stats" in queue:
                        if time.time() - last_log > 5:
                            last_log = time.time()
                            logger.info(
                                f'=================== receiver queue size {self.queue_name} {self.params} {queue["messages"]=} {queue["messages_unacknowledged"]=} {queue["message_stats"]["publish"]=} {queue["message_stats"]["deliver_get"]=}'
                            )
                        if (
                            queue["messages"] == 0
                            and queue["messages_unacknowledged"] == 0
                            # ensures that at least anything was put into and got out of the queue.
                            and queue["message_stats"]["publish"] > 0
                            and queue["message_stats"]["deliver_get"] >= queue["message_stats"]["publish"]
                        ):
                            break
                    elif queue["messages"] == 0 and "message_stats" not in queue:
                        # non touched queue => nothing to wait
                        break
                elif self.role == QueueRole.Publisher:
                    break
                else:
                    raise Exception("not implemented")
            await asyncio.sleep(1)

    async def mark_done(self, message: aio_pika.IncomingMessage):
        try:
            await message.ack()
        except aio_pika.exceptions.ChannelInvalidStateError:
            logger.error(f"ack for {message.message_id=} failed with ChannelInvalidStateError")
            # logger.error(f"{self.channel.is_closed=}")
            # self.channel_invalid_state_flag.set()

    async def reject(self, message: aio_pika.IncomingMessage, requeue: bool):
        try:
            await message.reject(requeue)
        except aio_pika.exceptions.ChannelInvalidStateError:
            logger.error(f"reject for {message.message_id=} failed with ChannelInvalidStateError")
            # logger.error(f"{self.channel.is_closed=}")
            # self.channel_invalid_state_flag.set()

    async def is_ready(self):
        await self.ready_state[self.role].wait()

    async def publisher_loop(self):
        try:
            while not await self.is_stopped():
                if not await self.connect():
                    logger.info("Failed connect to rabbitmq, waiting..")
                    await asyncio.sleep(5)
                    continue

                logger.info(f"rabbitmq {self.connection=} --------------------")

                async with self.connection:
                    channel = await self.connection.channel()
                    logger.info(f"rabbitmq {channel=} ----------------------")

                    self.exchange_name = (
                        self.params.exchange_name
                        if self.params.exchange_name is not None
                        else self._gen_queue_exchange_name()
                    )
                    if self.params.exchange_type == aio_pika.ExchangeType.TOPIC:
                        exchange = await channel.declare_exchange(
                            name=self.exchange_name, type=aio_pika.ExchangeType.TOPIC, durable=True
                        )
                    elif self.params.exchange_type == aio_pika.ExchangeType.DIRECT:
                        exchange = await channel.declare_exchange(
                            name=self.exchange_name, type=aio_pika.ExchangeType.DIRECT, durable=False
                        )
                    else:
                        raise Exception(f"not supported {self.params.exchange_type=}")

                    # Declaring and binding queue, so if consumer does not exist yet, messages will not be lost
                    if self.queue_name:
                        arguments = {}
                        if self.params.x_max_priority is not None:
                            arguments["x-max-priority"] = self.params.x_max_priority

                        logger.info(f"publisher creating receiver queue {self.queue_name} {arguments=}")
                        receiver_queue = await channel.declare_queue(
                            self.queue_name,
                            durable=True,
                            arguments=arguments,
                            exclusive=self.params.exclusive,
                        )
                        await receiver_queue.bind(exchange, routing_key=self.queue_name)

                    self.ready_state[QueueRole.Publisher].set()

                    try:
                        while not await self.is_stopped():
                            # logger.info( f'puslisher {self.queue_name} loop iteration')
                            message = await self.pop(1)
                            # logger.info( f'publisher loop {self.queue_name} poped {message=}')
                            if message is not None:
                                # logger.info(f"-------------------publishing msg {message.encode()}")

                                if isinstance(message, QueueRoutedMessage):
                                    routing_key = message.routing_key
                                else:
                                    routing_key = self.queue_name

                                # logger.info(f"publishing into {routing_key=} {message.data=} {message.priority=}")
                                await exchange.publish(
                                    aio_pika.Message(
                                        body=message.encode(),
                                        delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
                                        priority=message.priority,
                                    ),
                                    routing_key=routing_key,
                                )
                                # logger.info( f'published into {routing_key=}')

                                self.internal_queue.task_done()

                    except Exception as e:
                        logger.error("exception in RabbitmqQueue::publisher_loop (internal)")
                        logger.error(traceback.format_exc())

                self.ready_state[QueueRole.Publisher].clear()

        except Exception as e:
            logger.error("exception in RabbitmqQueue::publisher_loop")
            logger.error(traceback.format_exc())

    def _gen_queue_exchange_name(self):
        return f"{self.queue_name}_exchange"

    async def create_channel(self):
        channel = await self.connection.channel()
        logger.info(f"rabbitmq {self.queue_name} {channel=} ----------------------")

        # Maximum message count which will be processing at the same time.
        await channel.set_qos(prefetch_count=self.params.prefetch_count)

        # Declaring queue
        arguments = {}
        if self.params.x_max_priority is not None:
            arguments["x-max-priority"] = self.params.x_max_priority
        logger.info(f"receiver creating queue {self.queue_name} {arguments=}")
        self.receiver_queue = await channel.declare_queue(
            name=self.queue_name,
            durable=True,
            arguments=arguments,
            exclusive=self.params.exclusive,
        )

        self.exchange_name = (
            self.params.exchange_name if self.params.exchange_name is not None else self._gen_queue_exchange_name()
        )
        if self.params.exchange_type == aio_pika.ExchangeType.TOPIC:
            exchange = await channel.declare_exchange(
                name=self.exchange_name, type=aio_pika.ExchangeType.TOPIC, durable=True
            )
        elif self.params.exchange_type == aio_pika.ExchangeType.DIRECT:
            exchange = await channel.declare_exchange(
                name=self.exchange_name, type=aio_pika.ExchangeType.DIRECT, durable=False
            )
        else:
            raise Exception(f"not supported {self.params.exchange_type=}")
        rks = self.params.routing_key if isinstance(self.params.routing_key, list) else [self.params.routing_key]
        for rk in rks:
            if rk == "":
                rk = self.queue_name
            logger.info(f"binding queue to {self.exchange_name=} {rk=}")
            await self.receiver_queue.bind(exchange, routing_key=rk)
        return channel

    async def connect(self):
        try:
            self.connection = await aio_pika.connect_robust(self.url)
            return True
        except (aiormq.exceptions.AMQPConnectionError, StopAsyncIteration):
            return False

    async def receiver_loop(self):
        try:
            while not await self.is_stopped():
                if not await self.connect():
                    logger.info("Failed connect to rabbitmq, waiting..")
                    await asyncio.sleep(5)
                    continue

                logger.info(f"rabbitmq {self.queue_name} {self.connection=} -----------------------")

                try:
                    # Creating channel
                    channel = await self.create_channel()
                    # self.channel_invalid_state_flag.clear()

                    self.ready_state[QueueRole.Receiver].set()

                    logger.info(f"rabbitmq {self.queue_name} consume start----------------------------")

                    # await self.receiver_queue.consume(self.receive_message)
                    async with self.receiver_queue.iterator(timeout=3) as queue_iter:
                        while not await self.is_stopped():  # and not self.channel_invalid_state_flag.is_set():
                            if channel.is_closed:
                                # logger.info(f"channel for queue {self.queue_name} is closed, reopening")
                                # await self.channel.reopen()
                                break
                            try:
                                message = await anext(queue_iter)
                                # logger.info(
                                #     f"receiver loop {self.queue_name=} {message.message_id=} {message.redelivered=} {message.delivery_tag=}"
                                # )
                                await self.push(message)
                                # logger.info(f"receiver pushed {message.message_id}")
                            except asyncio.TimeoutError:
                                pass

                    logger.info(f"rabbitmq {self.queue_name} consume done----------------------------")

                except Exception as e:
                    logger.error(f"!!!!!!!!!!!!!!!!!! exception in rabbitmq receiver_loop {e}")
                    logger.error(traceback.format_exc())

                self.ready_state[QueueRole.Receiver].clear()
        except Exception as e:
            logger.error(f"!!!!!!!!!!!!!!!!!! exception in rabbitmq {e}")
            logger.error(traceback.format_exc())

    async def delete(self):
        channel = await self.connection.channel()
        await channel.queue_delete(self.queue_name)
        await channel.exchange_delete(self.exchange_name)
