#!/bin/bash

# 智能慢病管理系统 - 一键启动脚本

echo "🚀 智能慢病管理系统启动中..."
echo ""

# 检查环境变量
check_env() {
    if [ ! -f "$1" ]; then
        echo "❌ 错误: 找不到 $1"
        echo "   请复制 $2 并重命名为 $1，然后填写配置"
        exit 1
    fi
}

# 检查后端环境变量
echo "📋 检查后端环境配置..."
check_env "backend/.env" "backend/.env.example"
echo "✅ 后端环境配置已就绪"

# 检查前端环境变量
echo "📋 检查前端环境配置..."
check_env "frontend/.env.local" "frontend/.env.example"
echo "✅ 前端环境配置已就绪"
echo ""

# 启动后端
echo "🔧 启动后端服务..."
cd backend
poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!
cd ..
echo "✅ 后端服务已启动 (PID: $BACKEND_PID) - http://localhost:8000"
echo ""

# 等待后端启动
sleep 3

# 启动前端
echo "🎨 启动前端服务..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..
echo "✅ 前端服务已启动 (PID: $FRONTEND_PID) - http://localhost:3000"
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🎉 启动完成！"
echo ""
echo "📊 访问地址："
echo "   前端应用: http://localhost:3000"
echo "   后端 API: http://localhost:8000"
echo "   API 文档: http://localhost:8000/docs"
echo ""
echo "🛑 停止服务："
echo "   按 Ctrl+C 停止所有服务"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# 等待用户中断
trap "echo ''; echo '🛑 停止所有服务...'; kill $BACKEND_PID $FRONTEND_PID; echo '✅ 已停止'; exit 0" INT

wait
