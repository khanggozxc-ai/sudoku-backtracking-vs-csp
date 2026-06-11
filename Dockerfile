FROM python:3.11-slim

# Thiết lập thư mục làm việc bên trong container
WORKDIR /app

# Cài đặt các thư viện lõi phục vụ tính toán và vẽ đồ thị
RUN pip install --no-cache-dir pandas matplotlib

# Sao chép toàn bộ mã nguồn dự án vào container
COPY . .

# Cấp quyền thực thi cho file kịch bản Bash
RUN chmod +x run_pipeline.sh

# Thiết lập lệnh mặc định khi container khởi động
CMD ["./run_pipeline.sh"]