在使用RabbitMQ之前，我们要先明白它的工作机制

通过vhost将多租户分隔开来，同一rabbitMQ服务不同的vhost之间互不干扰

先创建exchange，确定其类别。然后创建queue，并与exchange进行绑定，就像是订阅了所有到该exchange的消息一样。但并不是所有到达该exchange的消息都会分发到该queue上，而是通过routing key来区分的。一个queue可以绑定多个exchange。

一个queue内的信息只会被消费一次，如果多个consumer都希望获取该消息，应该每个consumer各自都开设一个queue，去订阅消息，然后各自去消费属于自己的queue。

### Exchange的类型
1. Direct Exchange：匹配Routing_key的时候，直接进行比较，完全相等表示匹配上了。
2. Topic Exchange：匹配Routing_key的时候，支持正则匹配。（但注意，不同于普通的正则表达式，这里通配符是"#")
3. Fanout Exchange：不管Routing_key，只要是binding到这个Exchange的queue都会收到消息
4. header Exchange: 匹配header的内容

> \* 匹配一个单词; \# 匹配0个或多个字符; \*，\# 只能写在.号左右，且不能挨着字符; 单词和单词之间需要用.隔开。

### 推送消息

任何连接到MQ服务器的客户端，都可以向指定的Exchange推送消息。只需要连接上，然后创建一个channel（因为操作都需要在channel中完成），在该channel中，推送消息。参数包括：Exchange，string类型，指定要推送到哪个交换中心；routing_key，便于queue去订阅。

### 消费message

推送消息的客户端不用知道queue的存在，它们只需要知道Exhange和routing_key。因此，queue的名字之类的信息消费不用与推送端同步，自己管理即可。