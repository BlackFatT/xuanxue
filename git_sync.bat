@echo off
chcp 936 > nul 2>&1  # 强制切换为 GBK 编码（936 是 GBK 的代码页）

:: 配置区域
set "GITHUB_REMOTE=github"
set "GITEE_REMOTE=gitee"
set "BRANCH_NAME=master"

echo ==============================================
echo            开始同步代码到远程仓库
echo ==============================================
echo 远程仓库: %GITHUB_REMOTE% 和 %GITEE_REMOTE%
echo 目标分支: %BRANCH_NAME%
echo ==============================================

if not exist .git (
    echo 错误：当前目录不是 Git 仓库！
    pause
    exit /b 1
)

set /p "COMMIT_MSG=请输入提交说明: "
if "!COMMIT_MSG!"=="" set COMMIT_MSG="自动同步提交"

echo.
echo [1/6] 正在拉取 %GITHUB_REMOTE% 最新代码...
git pull %GITHUB_REMOTE% %BRANCH_NAME%
if %errorlevel% neq 0 (
    echo 错误：拉取 %GITHUB_REMOTE% 失败！
    pause
    exit /b 1
)

echo.
echo [2/6] 正在拉取 %GITEE_REMOTE% 最新代码...
git pull %GITEE_REMOTE% %BRANCH_NAME%
if %errorlevel% neq 0 (
    echo 错误：拉取 %GITEE_REMOTE% 失败！
    pause
    exit /b 1
)

echo.
echo [3/6] 正在添加修改到暂存区...
git add .
if %errorlevel% neq 0 (
    echo 错误：添加文件失败！
    pause
    exit /b 1
)

echo.
echo [4/6] 正在提交到本地仓库...
git commit -m %COMMIT_MSG%
if %errorlevel% neq 0 (
    echo 错误：本地提交失败！
    pause
    exit /b 1
)

echo.
echo [5/6] 正在推送到 %GITHUB_REMOTE%...
git push %GITHUB_REMOTE% %BRANCH_NAME%
if %errorlevel% neq 0 (
    echo 错误：推送到 %GITHUB_REMOTE% 失败！
    pause
    exit /b 1
)

echo.
echo [6/6] 正在推送到 %GITEE_REMOTE%...
git push %GITEE_REMOTE% %BRANCH_NAME%
if %errorlevel% neq 0 (
    echo 错误：推送到 %GITEE_REMOTE% 失败！
    pause
    exit /b 1
)

echo.
echo ==============================================
echo 成功！代码已同步到 %GITHUB_REMOTE% 和 %GITEE_REMOTE%
echo ==============================================
pause
