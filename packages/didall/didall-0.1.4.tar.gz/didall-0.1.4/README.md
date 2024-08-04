# 基于DID的跨平台身份认证和端到端加密通信技术

**作者**: 常高伟  
**邮箱**: chgaowei@gmail.com  
**官网**: [pi-unlimited.com](http://pi-unlimited.com)  

## 摘要

本文提出了一种基于去中心化标识符（DID）和端到端加密通信技术，旨在解决当前智能体跨平台身份认证和安全通信的难题。通过结合W3C DID规范、区块链技术和TLS协议，本文设计了一种低成本、高效且安全的跨平台身份认证和加密通信方案。

## 特点

- **跨平台身份认证**：通过DID实现不同平台间的身份互操作性。
- **端到端加密通信**：使用ECDHE进行短期密钥协商，保证通信的安全性。
- **高效和安全**：简化身份验证过程，确保数据的保密性和完整性。

## 使用方法

请阅读我们的[技术介绍精简版](http://pi-unlimited.com/简版)来快速了解我们技术的概要。

### 安装

在项目根目录下运行以下命令以安装所需依赖：

```bash
pip install -r requirements.txt
```

### 运行

在安装完所有依赖后，你可以通过以下命令运行SDK：

```bash
python your_sdk.py
```

## 详细介绍

更多详细内容请参阅我们的完整技术文档。

## 贡献

欢迎对本项目进行贡献。请在提交Pull Request之前阅读贡献指南。

## 许可证
    
本项目基于MIT许可证开源。详细信息请参阅LICENSE文件。

## 打包上传（先更改setup.py中版本号）

```bash
python setup.py sdist bdist_wheel 
twine upload dist/*        
```