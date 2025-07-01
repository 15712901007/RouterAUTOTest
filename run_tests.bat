@echo off
rem 这一行是必须的，它告诉CMD窗口后续内容使用UTF-8代码页
chcp 65001 > nul

rem 这一行是关键，它强制所有被调用的Python进程使用UTF-8进行IO操作
set PYTHONIOENCODING=utf-8

echo.
echo ==================================================
echo           路由器自动化测试执行脚本
echo ==================================================
echo.

rem 步骤 1: 清理旧的Allure结果目录
echo [1/4] 清理旧的测试结果...
if exist .\\reports\\allure_results rmdir /s /q .\\reports\\allure_results

rem 步骤 2: 执行pytest测试
echo [2/4] 开始执行Pytest测试...
pytest .\\tests\\ --alluredir=.\\reports\\allure_results --screenshot only-on-failure --video retain-on-failure
if %errorlevel% neq 0 (
    echo.
    echo ******* 测试执行失败! *******
) else (
    echo.
    echo ******* 测试执行成功! *******
)

rem 步骤 3: 从原始数据生成标准的多文件Allure报告
echo [3/4] 生成标准Allure报告...
allure generate .\\reports\\allure_results -o .\\reports\\allure_report --clean

rem 步骤 4: 正在打开Allure报告
echo [4/4] 正在打开Allure报告...
allure open .\\reports\\allure_report

echo.
echo ==================================================
echo                 所有步骤已完成!
echo ==================================================
pause