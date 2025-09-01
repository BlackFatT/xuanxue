@echo off
chcp 936 > nul 2>&1  # ǿ���л�Ϊ GBK ���루936 �� GBK �Ĵ���ҳ��

:: ��������
set "GITHUB_REMOTE=github"
set "GITEE_REMOTE=gitee"
set "BRANCH_NAME=master"

echo ==============================================
echo            ��ʼͬ�����뵽Զ�ֿ̲�
echo ==============================================
echo Զ�ֿ̲�: %GITHUB_REMOTE% �� %GITEE_REMOTE%
echo Ŀ���֧: %BRANCH_NAME%
echo ==============================================

if not exist .git (
    echo ���󣺵�ǰĿ¼���� Git �ֿ⣡
    pause
    exit /b 1
)

set /p "COMMIT_MSG=�������ύ˵��: "
if "!COMMIT_MSG!"=="" set COMMIT_MSG="�Զ�ͬ���ύ"

echo.
echo [1/6] ������ȡ %GITHUB_REMOTE% ���´���...
git pull %GITHUB_REMOTE% %BRANCH_NAME%
if %errorlevel% neq 0 (
    echo ������ȡ %GITHUB_REMOTE% ʧ�ܣ�
    pause
    exit /b 1
)

echo.
echo [2/6] ������ȡ %GITEE_REMOTE% ���´���...
git pull %GITEE_REMOTE% %BRANCH_NAME%
if %errorlevel% neq 0 (
    echo ������ȡ %GITEE_REMOTE% ʧ�ܣ�
    pause
    exit /b 1
)

echo.
echo [3/6] ��������޸ĵ��ݴ���...
git add .
if %errorlevel% neq 0 (
    echo ��������ļ�ʧ�ܣ�
    pause
    exit /b 1
)

echo.
echo [4/6] �����ύ�����زֿ�...
git commit -m %COMMIT_MSG%
if %errorlevel% neq 0 (
    echo ���󣺱����ύʧ�ܣ�
    pause
    exit /b 1
)

echo.
echo [5/6] �������͵� %GITHUB_REMOTE%...
git push %GITHUB_REMOTE% %BRANCH_NAME%
if %errorlevel% neq 0 (
    echo �������͵� %GITHUB_REMOTE% ʧ�ܣ�
    pause
    exit /b 1
)

echo.
echo [6/6] �������͵� %GITEE_REMOTE%...
git push %GITEE_REMOTE% %BRANCH_NAME%
if %errorlevel% neq 0 (
    echo �������͵� %GITEE_REMOTE% ʧ�ܣ�
    pause
    exit /b 1
)

echo.
echo ==============================================
echo �ɹ���������ͬ���� %GITHUB_REMOTE% �� %GITEE_REMOTE%
echo ==============================================
pause
