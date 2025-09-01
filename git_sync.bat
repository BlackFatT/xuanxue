@echo off
chcp 65001 > nul 2>&1  # 解决中文显示乱码问题

:: 配置区域 - 请根据你的实际情况修改以下参数
set "GITHUB_REMOTE=github"       # GitHub 远程仓库名称（通常是 github）
set "GITEE_REMOTE=gitee"         # Gitee 远程仓库名称（通常是 gitee）
set "BRANCH_NAME=master"         # 分支名称（根据你的实际分支修改，如 main 或 master）

:: 提示信息
echo ==============================================
echo            开始同步代码到远程仓库
echo ==============================================
echo 远程仓库: %GITHUB_REMOTE% 和 %GITEE_REMOTE%
echo 目标分支: %BRANCH_NAME%
echo ==============================================

:: 检查是否在 Git 仓库中
if not exist .git (
    echo 错误：当前目录不是 Git 仓库！
    echo 请在项目根目录下运行此脚本
    pause
    exit /b 1
)

:: 获取提交信息
set /p "COMMIT_MSG=请输入提交说明: "
if "!COMMIT_MSG!"=="" set COMMIT_MSG="自动同步提交"

:: 添加所有修改
echo.
echo [1/4] 正在添加修改到暂存区...
git add .
if %errorlevel% neq 0 (
    echo 错误：添加文件失败！
    pause
    exit /b 1
)

:: 提交到本地仓库
echo.
echo [2/4] 正在提交到本地仓库...
git commit -m %COMMIT_MSG%
if %errorlevel% neq 0 (
    echo 错误：本地提交失败！
    pause
    exit /b 1
)

:: 推送到 GitHub
echo.
echo [3/4] 正在推送到 %GITHUB_REMOTE%...
git push %GITHUB_REMOTE% %BRANCH_NAME%
if %errorlevel% neq 0 (
    echo 错误：推送到 %GITHUB_REMOTE% 失败！
    pause
    exit /b 1
)

:: 推送到 Gitee
echo.
echo [4/4] 正在推送到 %GITEE_REMOTE%...
git push %GITEE_REMOTE% %BRANCH_NAME%
if %errorlevel% neq 0 (
    echo 错误：推送到 %GITEE_REMOTE% 失败！
    pause
    exit /b 1
)

:: 完成提示
echo.
echo ==============================================
echo 成功！代码已同步到 %GITHUB_REMOTE% 和 %GITEE_REMOTE%
echo ==============================================
pause
