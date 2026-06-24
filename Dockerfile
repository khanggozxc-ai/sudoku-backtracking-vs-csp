# Sử dụng hình ảnh Python chính thức bản slim để tối ưu hóa dung lượng Container
FROM python:3.11-slim

# # =======================================================
# # THIẾT LẬP CÁC BIẾN MÔI TRƯỜNG LÕI
# # =======================================================
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV MPLBACKEND=Agg

# # =======================================================
# # THƯ MỤC LÀM VIỆC BÊN TRONG CONTAINER
# # =======================================================
WORKDIR /app

# # =======================================================
# # CÀI ĐẶT TOÀN BỘ DEPENDENCIES (KHÓA PHIÊN BẢN AN TOÀN)
# # =======================================================
RUN pip install --no-cache-dir \
    pandas==2.3.1 \
    matplotlib==3.10.5 \
    numpy \
    streamlit

# # =======================================================
# # SAO CHÉP MÃ NGUỒN VÀ CẤP QUYỀN SCRIPT ĐIỀU PHỐI
# # =======================================================
COPY . .
RUN chmod +x run_pipeline.sh

# # =======================================================
# # MỞ CỔNG KẾT NỐI CHO ĐỒ HỌA WEB
# # =======================================================
EXPOSE 8501

# # =======================================================
# # LỆNH KHỞI CHẠY TỐI CAO (PIPELINE -> STREAMLIT WEB GUI)
# # =======================================================
# Đã đồng bộ chuẩn xác đường dẫn thực tế của file app.py theo sơ đồ src/streamlit_app/app.py
CMD ["bash", "-c", "./run_pipeline.sh && streamlit run streamlit_app/app.py --server.address 0.0.0.0 --server.port 8501"]