from flask import Blueprint, jsonify, request, render_template
import json
import os

main = Blueprint('main', __name__)

DATA_PATH = os.path.join(os.getcwd(), 'data', 'squad.json')

# Đọc dữ liệu từ file squad.json
@main.route('/dataset', methods=['GET'])
def get_dataset():
    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return jsonify(data)

# Ghi dữ liệu mới vào file squad.json
@main.route('/dataset', methods=['POST'])
def write_dataset():
    new_data = request.json
    with open(DATA_PATH, 'r+', encoding='utf-8') as f:  # Thêm encoding='utf-8'
        data = json.load(f)
        data['data'].append(new_data)
        f.seek(0)
        json.dump(data, f, indent=4, ensure_ascii=False)  # ensure_ascii=False để giữ các ký tự đặc biệt
    return jsonify({'message': 'Data added successfully'}), 201

# Cập nhật dữ liệu dựa trên id
@main.route('/dataset/<id>', methods=['PUT'])
def update_dataset(id):
    updated_data = request.json
    with open(DATA_PATH, 'r+', encoding='utf-8') as f:
        data = json.load(f)
        for article in data['data']:
            # Cập nhật title nếu có
            if 'title' in updated_data:
                article['title'] = updated_data['title']
            for paragraph in article['paragraphs']:
                # Cập nhật context nếu có
                if 'context' in updated_data:
                    paragraph['context'] = updated_data['context']
                for qa in paragraph['qas']:
                    if qa['id'] == id:
                        # Cập nhật dữ liệu câu hỏi và câu trả lời
                        qa['question'] = updated_data.get('question', qa['question'])
                        qa['answers'][0]['text'] = updated_data.get('answer', qa['answers'][0]['text'])
                        qa['answers'][0]['answer_start'] = updated_data.get('answer_start', qa['answers'][0]['answer_start'])
                        break
        f.seek(0)
        json.dump(data, f, indent=4, ensure_ascii=False)
        f.truncate()
    return jsonify({'message': 'Data updated successfully'}), 200

# Lấy dữ liệu dựa trên ID
@main.route('/dataset/<id>', methods=['GET'])
def get_dataset_by_id(id):
    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)
        for article in data['data']:
            for paragraph in article['paragraphs']:
                for qa in paragraph['qas']:
                    if qa['id'] == id:
                        return jsonify({
                            'title': article['title'],
                            'paragraphs': [{
                                'context': paragraph['context'],
                                'qas': [{
                                    'question': qa['question'],
                                    'answers': qa['answers']
                                }]
                            }]
                        })
    return jsonify({'error': 'Data not found'}), 404


# Route để hiển thị trang HTML
@main.route('/')
def index():
    return render_template('index.html')
