from flask import Flask, jsonify, request, abort
from flask_cors import CORS
import jwt
from datetime import datetime, timedelta

app = Flask(__name__)
# 配置 CORS（允许所有前端源访问，开发时常用）
CORS(app, resources={r"/api/*": {"origins": "*"}})
# JWT 密钥（生产环境需通过环境变量配置）
app.config['SECRET_KEY'] = 'your-secret-key-123'

# 模拟数据库数据（实际需替换为真实数据库）
# 1. 用户凭证表（用于登录验证）
db_users = [
    {"username": "admin", "password": "123456"}  # 密码建议存储哈希值（如 bcrypt）
]
# 2. 学生信息（用于 /api/info 接口）
student_info = {"name": "张三", "phone": "13812345678", "age": 20}
# 3. 用户管理列表（用于 /user 页面）
user_list = [
    {"id": 1, "name": "李四", "phone": "13900001111", "age": 25},
    {"id": 2, "name": "王五", "phone": "13922223333", "age": 28}
]

# 工具函数：验证 JWT token
def verify_token(token):
    try:
        decoded = jwt.decode(
            token, 
            app.config['SECRET_KEY'], 
            algorithms=['HS256']
        )
        return decoded['username']  # 返回登录用户名
    except jwt.ExpiredSignatureError:
        abort(401, description="Token已过期")
    except:
        abort(401, description="无效的Token")

# 登录接口（前端 /api/login）
@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json()
    # 验证用户名密码
    user = next(
        (u for u in db_users if u['username'] == data.get('username') and u['password'] == data.get('password')),
        None
    )
    if not user:
        abort(401, description="用户名或密码错误")
    
    # 生成 JWT（有效期30分钟）
    token = jwt.encode({
        "username": user['username'],
        "exp": datetime.utcnow() + timedelta(minutes=30)
    }, app.config['SECRET_KEY'], algorithm='HS256')
    
    return jsonify({"token": token})

# 学生信息接口（前端 /api/info，需登录）
@app.route("/api/info", methods=["GET"])
def get_student_info():
    # 验证 Token
    token = request.headers.get("Authorization")
    if not token:
        abort(401, description="未提供Token")
    verify_token(token.replace("Bearer ", ""))  # 验证失败会直接 abort
    
    return jsonify(student_info)

# 用户列表接口（前端 /api/users，需登录）
@app.route("/api/users", methods=["GET"])
def get_users():
    # 验证 Token
    token = request.headers.get("Authorization")
    if not token:
        abort(401, description="未提供Token")
    verify_token(token.replace("Bearer ", ""))
    
    return jsonify(user_list)

# 添加用户接口（前端 POST /api/users，需登录）
@app.route("/api/users", methods=["POST"])
def add_user():
    # 验证 Token
    token = request.headers.get("Authorization")
    if not token:
        abort(401, description="未提供Token")
    verify_token(token.replace("Bearer ", ""))
    
    # 验证请求数据
    data = request.get_json()
    if not data or "name" not in data or "phone" not in data or "age" not in data:
        abort(400, description="缺少必要字段：name/phone/age")
    
    # 添加新用户（模拟ID自增）
    new_user = {
        "id": len(user_list) + 1,
        "name": data["name"],
        "phone": data["phone"],
        "age": data["age"]
    }
    user_list.append(new_user)
    return jsonify(new_user), 201

# 更新用户接口（前端 PUT /api/users/<id>，需登录）
@app.route("/api/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    # 验证 Token
    token = request.headers.get("Authorization")
    if not token:
        abort(401, description="未提供Token")
    verify_token(token.replace("Bearer ", ""))
    
    # 查找用户
    user = next((u for u in user_list if u["id"] == user_id), None)
    if not user:
        abort(404, description="用户不存在")
    
    # 更新字段（支持部分更新）
    data = request.get_json()
    if "name" in data:
        user["name"] = data["name"]
    if "phone" in data:
        user["phone"] = data["phone"]
    if "age" in data:
        user["age"] = data["age"]
    
    return jsonify(user)

# 删除用户接口（前端 DELETE /api/users/<id>，需登录）
@app.route("/api/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    # 验证 Token
    token = request.headers.get("Authorization")
    if not token:
        abort(401, description="未提供Token")
    verify_token(token.replace("Bearer ", ""))
    
    # 查找并删除用户
    global user_list
    user = next((u for u in user_list if u["id"] == user_id), None)
    if not user:
        abort(404, description="用户不存在")
    
    user_list = [u for u in user_list if u["id"] != user_id]
    return jsonify({"message": "用户删除成功"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)  # 后端运行在5000端口