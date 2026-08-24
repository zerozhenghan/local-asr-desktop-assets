# 听见 · 公开下载

这里仅存放“听见”本地视频转文字工具的公开安装包、首次启动运行时和固定版本模型。应用源码位于私有仓库，不在本仓库公开。

## 下载

从 [v0.1.0 预览版](https://github.com/zerozhenghan/local-asr-desktop-assets/releases/tag/v0.1.0) 下载：

- macOS Apple Silicon：`TingJian-0.1.0-macOS-arm64.dmg`
- Windows 10/11 x64：`TingJian-0.1.0-Windows-x64-Setup.exe`
- `SHA256SUMS.txt`：全部公开制品的 SHA-256 校验值

安装包本身较小。首次启动会自动下载对应系统的离线识别运行时与 `faster-whisper-small` 模型，下载后即可断网转写。

## 预览版提醒

v0.1.0 尚未使用 Apple Developer ID 或 Windows 商业证书签名，因此系统可能显示开发者身份或 SmartScreen 警告。请先核对 `SHA256SUMS.txt`，只从本仓库 Release 下载。

视频和转写内容由应用在本机处理，不会上传到本仓库或识别服务。
