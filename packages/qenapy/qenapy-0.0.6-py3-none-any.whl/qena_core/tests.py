from libs.logstash import Logstash

Logstash().start()
Logstash().info(message="test", tags=["test"], extra="test")
