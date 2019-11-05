import pika

username = "my_username"
password = "special_pw"
host = "192.168.0.1"
port = "5672"
vhost = "my_vhost"

credentials = pika.PlainCredentials(username, password)
conn_params = pika.ConnectionParameters(host, port, vhost, credentials)
conn = pika.BlockingConnection(conn_params)


def create():
    # 任何操作都是在channel中进行，所以需要先创建一个channel
    channel = conn.channel()

    # 创建一个exchange
    # durable: rabbitmq服务重启之后该exchange是否还存在
    # auto_delete: 当没有queue绑定该exchange的时候，自动删除该exchange
    channel.exchange_declare("exchange_name", exchange_type="topic", durable=True, auto_delete=False)

    # 创建一个队列
    # passive: 被动，只检查是否已经存在，如果不存在该queue，报错
    # durable: rabbitmq服务重启之后是否还在
    # exclusive: 创建的队列只能为当前的channel使用
    # auto_delete: 没有consumer的时候，自动删除
    channel.queue_declare("queue_name", passive=False, durable=False, exclusive=False, auto_delete=False)

    # 将指定的队列绑定到指定的exchange，并定义routing_key
    channel.queue_bind("queue_name", "exchange_name", routing_key="#.chat_end")

    # 向指定的exchange推送消息
    channel.basic_publish("exchange_name", routing_key="#.chat_end", body="string_type_can_be_json")

    # 消费指定的queue
    def callback_fn(channel, method, properties, body):
        # 收到的消息都是binary，需要先decode
        msg = body.decode()

    # 消费指定队列的queue，第二个参数为回调函数
    channel.basic_consume("queue_name", callback_fn, auto_ack=True)

    # 删除不用的queue或者exchange
    channel.queue_delete("queue_name")
    channel.exchange_delete("exchange_name")

    channel.close()
