from flask import Flask, jsonify, request
import logging

app = Flask(__name__)

# In-memory 'database' simulation
tasks = [
    {"id": 1, "title": "Complete DevOps Assignment", "done": False},
    {"id": 2, "title": "Push code to Azure Repos", "done": True}
]

# Configure logging
logging.basicConfig(level=logging.INFO)

@app.route('/')
def home():
    app.logger.info("Home endpoint called")
    return "🚀 Welcome to the Advanced Flask App on Azure!"

@app.route('/tasks', methods=['GET'])
def get_tasks():
    app.logger.info("Fetching all tasks")
    return jsonify(tasks)

@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    app.logger.info(f"Fetching task with ID: {task_id}")
    task = next((task for task in tasks if task['id'] == task_id), None)
    if task:
        return jsonify(task)
    else:
        return jsonify({"error": "Task not found"}), 404

@app.route('/tasks', methods=['POST'])
def create_task():
    app.logger.info("Creating a new task")
    data = request.get_json()
    if not data or 'title' not in data:
        return jsonify({"error": "Title is required"}), 400
    
    new_task = {
        "id": tasks[-1]['id'] + 1 if tasks else 1,
        "title": data['title'],
        "done": False
    }
    tasks.append(new_task)
    return jsonify(new_task), 201

@app.route('/tasks/<int:task_id>', methods=['PATCH'])
def update_task(task_id):
    app.logger.info(f"Updating task with ID: {task_id}")
    task = next((task for task in tasks if task['id'] == task_id), None)
    if not task:
        return jsonify({"error": "Task not found"}), 404

    data = request.get_json()
    task['title'] = data.get('title', task['title'])
    task['done'] = data.get('done', task['done'])
    return jsonify(task)

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    app.logger.info(f"Deleting task with ID: {task_id}")
    global tasks
    new_tasks = [task for task in tasks if task['id'] != task_id]
    if len(new_tasks) == len(tasks):
        return jsonify({"error": "Task not found"}), 404
    tasks = new_tasks
    return jsonify({"message": "Task deleted successfully"})

@app.errorhandler(404)
def not_found_error(error):
    app.logger.error("404 error occurred")
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    app.logger.error("500 internal server error occurred")
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)