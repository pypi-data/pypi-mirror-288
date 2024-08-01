[<img alt="LOGO" src="https://github.com/favicon.ico" height="21" width="21"/>]()
[![Release](https://img.shields.io/github/release/2018-11-27/LogCollectionFormatter2.svg?style=flat-square")](https://github.com/2018-11-27/LogCollectionFormatter2/releases/latest)
[![Python Versions](https://img.shields.io/pypi/pyversions/LogCollectionFormatter2)](https://pypi.org/project/LogCollectionFormatter2)
[![License](https://img.shields.io/pypi/l/LogCollectionFormatter2)](https://github.com/2018-11-27/LogCollectionFormatter2/blob/main/LICENSE)
[![Downloads](https://static.pepy.tech/badge/LogCollectionFormatter2)](https://pepy.tech/project/LogCollectionFormatter2)

# LogCollectionFormatter2

## 介绍

LogCollectionFormatter2 是一个灵活的日志记录和消息队列工具库，专为 Python 应用程序设计。它提供了强大的日志记录和消息队列功能，帮助开发者轻松追踪应用程序的运行状态和发送日志消息到消息队列中。

## 安装

可以通过 pip 安装 LogCollectionFormatter2：

```bash
pip install LogCollectionFormatter2
```

## 主要组件

### BaseLog 类

`BaseLog` 是所有日志功能的基类，提供基本的日志配置和日志记录方法。主要功能包括：

- 配置日志级别、日志文件名、日志文件路径等。
- 支持日志文件的自动轮转。
- 提供多种日志级别的方法，如 `debug`, `info`, `warn`, `error` 等。
- 支持自定义日志格式和扩展日志记录功能。

### MainLog 类

`MainLog` 继承自 `BaseLog`，增加了对消息队列的支持。主要功能包括：

- 配置消息队列（如 RabbitMQ）的连接参数。
- 提供将日志消息发送到消息队列的功能。
- 支持装饰器模式，方便在 Flask 或其他 Web 框架中自动记录接口访问日志。

### InsertQueue 类

`InsertQueue` 类负责管理消息队列的连接和消息发送。主要功能包括：

- 管理和维护消息队列的连接池。
- 提供同步和异步发送消息到消息队列的方法。
- 支持连接的重试和异常处理。

## 使用示例

### 基本日志记录

```python
from LogCollectionFormatter2 import MainLog

# 初始化 MainLog 实例
log = MainLog(app_name='MyApp', prefix_path='/var/log/myapp', t_code='10001')

# 记录不同级别的日志
log.debug('This is a debug message')
log.info('This is an info message')
log.warn('This is a warning message')
log.error('This is an error message')
```

### 集成 Flask 和消息队列

```python
from flask import Flask, request, jsonify
from LogCollectionFormatter2 import MainLog

app = Flask(__name__)

# 初始化日志记录器和消息队列支持
log = MainLog(
    app_name='FlaskApp', prefix_path='/var/log/flaskapp', t_code='10002',
    journal_mq_enable=True, host='rabbitmq_host', port=5672
)

@app.route('/api/data', methods=['POST'])
@log.with_internal_journallog(method_code='GET_DATA')
def get_data():
    data = request.json
    # 处理数据...
    return jsonify({'status': 'success', 'data': data})

if __name__ == '__main__':
    app.run(debug=True)
```

## 配置参数

`MainLog` 初始化时支持多种配置参数，以便灵活适应不同的应用场景。主要参数包括：

- `app_name`: 应用名称，用于日志文件的命名。
- `prefix_path`: 日志文件存储的前缀路径。
- `t_code`: 交易代码，用于日志记录中的特定标识。
- `journal_log_enable`: 是否启用日志记录功能。
- `journal_mq_enable`: 是否启用消息队列功能。
- `host`, `port`, `virtual_host`, `name`, `password`: RabbitMQ 连接参数。

更多配置参数请参考源代码中的 `MainLog` 类定义。

## 注意事项

- 确保 RabbitMQ 或其他消息队列服务正常运行。
- 在生产环境中，建议关闭 Flask 的 `debug` 模式以提高性能和安全性。
- 根据实际应用场景调整日志级别和文件轮转策略。

## 联系我们

如果您在使用过程中遇到任何问题或有任何建议，请通过 GitHub Issues 反馈给我们。

## 许可证

LogCollectionFormatter2 遵循 BSD 3-Clause 许可证。详细信息请参考 LICENSE 文件。
