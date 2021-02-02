# XCodeBatchPackage
### Build For Enterprise
1. 在developer.apple.com创建App Identifiers
2. 通过Xcode的"Automatically manage signing"来自动生成相应的Provisioning Profile（输入你的BID，按一下回车Xcode会自动处理）
3. 补充package.sh里的信息(包含了rm命令，请再检查一下)
4. ./package.sh

> 主要代码来自 https://github.com/gwh111/package, 修改了其中一部分错误，重新测试运行通过.