from transformers import AutoTokenizer, AutoModelForQuestionAnswering, Trainer, TrainingArguments
from datasets import Dataset

# Đường dẫn tới mô hình đã fine-tuned
fine_tuned_model_path = "./phobert-qa"

# Load lại mô hình và tokenizer đã fine-tuned
tokenizer = AutoTokenizer.from_pretrained(fine_tuned_model_path)
model = AutoModelForQuestionAnswering.from_pretrained(fine_tuned_model_path)

# Chuẩn bị dataset như trước (có thể dùng lại dữ liệu hoặc dataset mới)
# Ví dụ:
# train_dataset = Dataset.from_dict(...)  # Dataset cho lần fine-tuning mới

# Thiết lập các tham số huấn luyện tiếp tục (có thể giảm learning rate để tránh overfitting)
training_args = TrainingArguments(
    output_dir="./phobert-qa-continued",
    overwrite_output_dir=True,
    num_train_epochs=10,  # Giảm số epoch nếu chỉ muốn fine-tune thêm một chút
    learning_rate=3e-6,  # Learning rate thấp hơn
    warmup_ratio=0.1,
    weight_decay=0.1,
    per_device_train_batch_size=4,
    per_device_eval_batch_size=4,
    eval_strategy="epoch",
    save_steps=10_000,
    save_total_limit=2,
    logging_dir='./logs',
    logging_steps=100,
    report_to="none",
    fp16=True,
)

# Khởi tạo Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
    data_collator=data_collator,
)

# Bắt đầu huấn luyện tiếp tục
trainer.train()

# Lưu mô hình đã tiếp tục fine-tune
trainer.save_model("./phobert-qa-continued")
tokenizer.save_pretrained("./phobert-qa-continued")

print("Tiếp tục fine-tuning hoàn tất và mô hình đã được lưu.")
