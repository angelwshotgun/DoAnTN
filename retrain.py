# Import additional libraries for file handling
import torch
from transformers import AutoModelForQuestionAnswering, AutoTokenizer
from flask import Flask, request, jsonify, render_template
from pyngrok import ngrok, conf
from werkzeug.utils import secure_filename
import os
import PyPDF2
import io

# Nhập ngrok_token từ Google Colab User Data
from google.colab import auth, userdata
auth.authenticate_user()

# Cấu hình upload file
UPLOAD_FOLDER = '/content/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf'}

# Tạo thư mục upload nếu chưa tồn tại
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Lấy ngrok_token từ user
ngrok_token = userdata.get('ngrok_token')

# Đảm bảo rằng token đã được nhập
if not ngrok_token:
    raise ValueError("Bạn cần nhập 'ngrok_token' từ User Data trong Google Colab.")

# Cấu hình ngrok
conf.get_default().auth_token = ngrok_token

# Load model và tokenizer
model_path = "/content/phobert-qa2"
model = AutoModelForQuestionAnswering.from_pretrained(model_path)
tokenizer = AutoTokenizer.from_pretrained(model_path, use_fast=True)

# Khởi tạo Flask app
app = Flask(
    __name__,
    template_folder='/content/DoAnTN/template',
    static_folder='/content/DoAnTN/template'
)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Giới hạn kích thước file 16MB

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def read_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def read_pdf_file(file_path):
    text = ''
    with open(file_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

# Lưu context vào session
context_storage = {}

@app.route("/upload", methods=["POST"])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Đọc nội dung file
        if filename.endswith('.txt'):
            content = read_text_file(filepath)
        elif filename.endswith('.pdf'):
            content = read_pdf_file(filepath)

        # Lưu context với ID ngẫu nhiên
        session_id = os.urandom(16).hex()
        context_storage[session_id] = content

        return jsonify({
            'success': True,
            'session_id': session_id,
            'preview': content[:200] + '...' if len(content) > 200 else content
        })

    return jsonify({'error': 'File type not allowed'})

@app.route("/", methods=["GET", "POST"])
def home():
    answer = None
    messages = []

    if request.method == "POST":
        question = request.form.get("question", "")
        context = request.form.get("context", "")
        session_id = request.form.get("session_id", "")

        # Sử dụng context từ file nếu có
        if session_id and session_id in context_storage:
            context = context_storage[session_id]

        try:
            # Tokenize đầu vào
            inputs = tokenizer(
                question,
                context[:512] if context else "Tôi không có thông tin về câu hỏi này.",
                return_tensors="pt",
                max_length=258,
                truncation="only_second",
                padding="max_length"
            )

            # Dự đoán với model
            with torch.no_grad():
                outputs = model(**inputs)
                start_logits = outputs.start_logits
                end_logits = outputs.end_logits

                # Tính confidence scores
                start_probs = torch.softmax(start_logits, dim=1)
                end_probs = torch.softmax(end_logits, dim=1)
                
                start_index = torch.argmax(start_logits)
                end_index = torch.argmax(end_logits)
                
                # Tính điểm confidence tổng thể
                confidence_score = float(start_probs[0][start_index] * end_probs[0][end_index])

            # Kiểm tra độ tin cậy của câu trả lời
            if confidence_score < 0.1:  # Ngưỡng confidence 0.1
                answer = "Tôi không thể trả lời câu hỏi này một cách chính xác. Vui lòng kiểm tra lại câu hỏi hoặc cung cấp thêm thông tin."
            else:
                # Decode câu trả lời
                tokens = inputs['input_ids'][0][start_index:end_index + 1]
                raw_answer = tokenizer.decode(tokens, skip_special_tokens=True)
                
                # Xử lý và làm sạch câu trả lời
                answer = clean_answer(raw_answer)

        except Exception as e:
            print(f"Error in processing question: {str(e)}")
            answer = "Đã xảy ra lỗi khi xử lý câu hỏi. Vui lòng thử lại."

        # Thêm câu hỏi và câu trả lời vào lịch sử
        messages.append({'content': question, 'is_user': True})
        messages.append({'content': answer, 'is_user': False})

    # Render giao diện
    return render_template('index.html', answer=answer, messages=messages)

def clean_answer(text):
    """Làm sạch câu trả lời"""
    # Loại bỏ các ký tự đặc biệt không mong muốn ở cuối
    text = text.strip()
    while text.endswith('@@') or text.endswith('@'):
        text = text.rstrip('@')
    
    # Loại bỏ khoảng trắng thừa
    text = ' '.join(text.split())
    
    # Thêm dấu câu cuối nếu chưa có
    if text and not text[-1] in '.!?':
        text += '.'
        
    return text

# Hàm kiểm tra tính liên quan của câu hỏi với context
def check_question_relevance(question, context):
    """
    Kiểm tra độ liên quan giữa câu hỏi và context
    Returns: float (0-1)
    """
    # Tokenize cả câu hỏi và context
    inputs = tokenizer(
        question,
        context,
        return_tensors="pt",
        max_length=512,
        truncation=True,
        padding="max_length"
    )
    
    # Sử dụng model để tính toán điểm tương đồng
    with torch.no_grad():
        outputs = model(**inputs)
        relevance_score = torch.mean(outputs.start_logits * outputs.end_logits)
        
    return float(torch.sigmoid(relevance_score))

def list_available_files():
    """Lấy danh sách các file trong thư mục upload"""
    files = []
    for filename in os.listdir(UPLOAD_FOLDER):
        if filename.endswith(('.txt', '.pdf')):
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            file_size = os.path.getsize(file_path)
            files.append({
                'name': filename,
                'size': file_size,
                'path': file_path
            })
    return files

@app.route("/list-contexts", methods=["GET"])
def list_contexts():
    """Route để hiển thị danh sách các file context có sẵn"""
    files = list_available_files()
    return render_template('context.html', files=files)

@app.route("/select-context", methods=["POST"])
def select_context():
    """Route để chọn và load context từ file"""
    file_path = request.form.get('file_path')
    
    if not file_path or not os.path.exists(file_path):
        return jsonify({'error': 'File không tồn tại'})
        
    try:
        # Đọc nội dung file
        if file_path.endswith('.txt'):
            content = read_text_file(file_path)
        elif file_path.endswith('.pdf'):
            content = read_pdf_file(file_path)
        else:
            return jsonify({'error': 'Định dạng file không được hỗ trợ'})

        # Tạo session ID mới cho context
        session_id = os.urandom(16).hex()
        context_storage[session_id] = content

        return jsonify({
            'success': True,
            'session_id': session_id,
            'preview': content[:200] + '...' if len(content) > 200 else content,
            'filename': os.path.basename(file_path)
        })
        
    except Exception as e:
        return jsonify({'error': f'Lỗi khi đọc file: {str(e)}'})

# Kết nối ngrok
public_url = ngrok.connect(5000)
print("Ngrok URL:", public_url)

# Chạy Flask app
app.run(port=5000)