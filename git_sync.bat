@echo off
chcp 65001 > nul 2>&1  # ���������ʾ��������

:: �������� - ��������ʵ������޸����²���
set "GITHUB_REMOTE=github"       # GitHub Զ�ֿ̲����ƣ�ͨ���� github��
set "GITEE_REMOTE=gitee"         # Gitee Զ�ֿ̲����ƣ�ͨ���� gitee��
set "BRANCH_NAME=master"         # ��֧���ƣ��������ʵ�ʷ�֧�޸ģ��� main �� master��

:: ��ʾ��Ϣ
echo ==============================================
echo            ��ʼͬ�����뵽Զ�ֿ̲�
echo ==============================================
echo Զ�ֿ̲�: %GITHUB_REMOTE% �� %GITEE_REMOTE%
echo Ŀ���֧: %BRANCH_NAME%
echo ==============================================

:: ����Ƿ��� Git �ֿ���
if not exist .git (
    echo ���󣺵�ǰĿ¼���� Git �ֿ⣡
    echo ������Ŀ��Ŀ¼�����д˽ű�
    pause
    exit /b 1
)

:: ��ȡ�ύ��Ϣ
set /p "COMMIT_MSG=�������ύ˵��: "
if "!COMMIT_MSG!"=="" set COMMIT_MSG="�Զ�ͬ���ύ"

:: ��������޸�
echo.
echo [1/4] ��������޸ĵ��ݴ���...
git add .
if %errorlevel% neq 0 (
    echo ��������ļ�ʧ�ܣ�
    pause
    exit /b 1
)

:: �ύ�����زֿ�
echo.
echo [2/4] �����ύ�����زֿ�...
git commit -m %COMMIT_MSG%
if %errorlevel% neq 0 (
    echo ���󣺱����ύʧ�ܣ�
    pause
    exit /b 1
)

:: ���͵� GitHub
echo.
echo [3/4] �������͵� %GITHUB_REMOTE%...
git push %GITHUB_REMOTE% %BRANCH_NAME%
if %errorlevel% neq 0 (
    echo �������͵� %GITHUB_REMOTE% ʧ�ܣ�
    pause
    exit /b 1
)

:: ���͵� Gitee
echo.
echo [4/4] �������͵� %GITEE_REMOTE%...
git push %GITEE_REMOTE% %BRANCH_NAME%
if %errorlevel% neq 0 (
    echo �������͵� %GITEE_REMOTE% ʧ�ܣ�
    pause
    exit /b 1
)

:: �����ʾ
echo.
echo ==============================================
echo �ɹ���������ͬ���� %GITHUB_REMOTE% �� %GITEE_REMOTE%
echo ==============================================
pause
