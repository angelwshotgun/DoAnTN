import json

def find_exact_position(context, answer):
    """
    Tìm vị trí chính xác của câu trả lời trong context
    """
    index = context.find(answer)
    return index if index != -1 else None

def validate_and_fix_answer_start(data_file, output_file=None):
    """
    Kiểm tra và sửa vị trí answer_start trong dataset
    """
    with open(data_file, 'r', encoding='utf-8') as f:
        dataset = json.load(f)
    
    validation_results = []
    fixes_made = False
    
    for article in dataset['data']:
        for paragraph in article['paragraphs']:
            context = paragraph['context']
            
            for qa in paragraph['qas']:
                for answer in qa['answers']:
                    current_start = answer['answer_start']
                    answer_text = answer['text']
                    
                    # Tìm vị trí chính xác
                    correct_position = find_exact_position(context, answer_text)
                    
                    # Kiểm tra text tại vị trí hiện tại
                    current_text = context[current_start:current_start + len(answer_text)]
                    is_correct = current_start == correct_position
                    
                    if not is_correct and correct_position is not None:
                        fixes_made = True
                        answer['answer_start'] = correct_position
                    
                    validation_results.append({
                        'title': article['title'],
                        'question': qa['question'],
                        'answer_text': answer_text,
                        'old_start': current_start,
                        'new_start': correct_position,
                        'old_text': current_text,
                        'is_correct': is_correct,
                        'id': qa['id']
                    })
    
    # Lưu file đã sửa nếu có thay đổi
    if fixes_made and output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(dataset, f, ensure_ascii=False, indent=2)
    
    return validation_results

def print_validation_results(results):
    """
    In kết quả kiểm tra
    """
    print("\nKết quả kiểm tra answer_start:")
    print("-" * 80)
    
    total = len(results)
    correct = sum(1 for r in results if r['is_correct'])
    incorrect = total - correct
    
    print(f"Tổng số câu trả lời: {total}")
    print(f"Vị trí đúng: {correct}")
    print(f"Vị trí cần sửa: {incorrect}")
    
    if incorrect > 0:
        print("\nChi tiết các vị trí cần sửa:")
        for result in results:
            if not result['is_correct']:
                print("\n" + "-" * 80)
                print(f"ID: {result['id']}")
                print(f"Câu hỏi: {result['question']}")
                print(f"Câu trả lời: {result['answer_text']}")
                print(f"Vị trí cũ: {result['old_start']}")
                print(f"Text tại vị trí cũ: {result['old_text']}")
                print(f"Vị trí mới: {result['new_start']}")
                print(f"Text tại vị trí mới: {result['answer_text']}")

def main():
    """
    Hàm chính
    """
    input_file = "C:\\Users\\z\\Documents\\vu\\python\\DoAnTN\\flask_squad_app\\data\\xdfixed1.json"
    output_file = "C:\\Users\\z\\Documents\\vu\\python\\DoAnTN\\flask_squad_app\\data\\xdfixed2.json"
    
    try:
        results = validate_and_fix_answer_start(input_file, output_file)
        print_validation_results(results)
    except Exception as e:
        print(f"Lỗi: {str(e)}")

# Chạy chương trình
if __name__ == "__main__":
    main()