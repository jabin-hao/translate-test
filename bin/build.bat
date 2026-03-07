@echo off
echo ========================================
echo   离线翻译服务 - 打包脚本
echo ========================================
echo.

echo [1/2] 使用 PyInstaller 打包...
pyinstaller translate-server.spec --noconfirm
if errorlevel 1 (
    echo 打包失败!
    pause
    exit /b 1
)

echo.
echo [2/2] 复制模型文件到输出目录...
xcopy /E /I /Y models\opus-mt-zh-en dist\translate-server\models\opus-mt-zh-en
xcopy /E /I /Y models\opus-mt-en-es dist\translate-server\models\opus-mt-en-es

echo.
echo ========================================
echo   打包完成!
echo   输出目录: dist\translate-server\
echo   运行: dist\translate-server\translate-server.exe
echo ========================================
pause
