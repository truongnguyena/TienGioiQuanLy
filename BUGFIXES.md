# Bug Fixes Summary

## Các lỗi đã được sửa:

### 1. Lỗi Database Schema
**Vấn đề**: Thiếu cột `world_level` và các cột khác trong bảng `world`
**Lỗi**: `psycopg2.errors.UndefinedColumn: column world.world_level does not exist`

**Giải pháp**:
- Đã tạo script migration `database_migration.sql`
- Đã tạo script Python `fix_database.py` 
- Các cột đã được thêm vào model trong `models.py`

**Cách chạy migration**:
```bash
# Chạy script SQL trực tiếp trên database
sqlite3 instance/tu_tien.db < database_migration.sql

# Hoặc chạy script Python (nếu Python hoạt động)
python fix_database.py
```

### 2. Lỗi Template Syntax
**Vấn đề**: Cú pháp Jinja2 không hợp lệ trong `guild_management.html`
**Lỗi**: `jinja2.exceptions.TemplateSyntaxError: expected token 'end of statement block', got 'if'`

**Giải pháp**:
- Đã sửa cú pháp từ `{% if guild.id == user_guild.id if user_guild else false %}` 
- Thành `{% if user_guild and guild.id == user_guild.id %}`

### 3. Lỗi None Attribute Access
**Vấn đề**: Truy cập thuộc tính trên object có thể là `None`
**Lỗi**: `jinja2.exceptions.UndefinedError: 'None' has no attribute 'strftime'`

**Giải pháp**:
- Đã thêm kiểm tra `{% if current_user.created_at %}` trong templates
- Đã sử dụng `or` operator để cung cấp giá trị mặc định trong routes.py

### 4. Lỗi Template Break Tag
**Vấn đề**: Sử dụng `{% break %}` không hợp lệ trong Jinja2
**Lỗi**: `jinja2.exceptions.TemplateSyntaxError: Encountered unknown tag 'break'`

**Giải pháp**:
- Đã loại bỏ `{% break %}` tags khỏi templates
- Sử dụng logic khác để kiểm soát vòng lặp

## Cách kiểm tra sửa lỗi:

### 1. Chạy test script:
```bash
python test_fixes.py
```

### 2. Kiểm tra database:
```bash
sqlite3 instance/tu_tien.db
.schema world
```

### 3. Kiểm tra templates:
- Mở các template files và tìm kiếm lỗi cú pháp
- Kiểm tra các thuộc tính có thể là None

## Các file đã được sửa:

1. `models.py` - Đã có đầy đủ các cột cần thiết
2. `templates/guild_management.html` - Đã sửa cú pháp Jinja2
3. `templates/profile.html` - Đã thêm kiểm tra None
4. `templates/rankings.html` - Đã loại bỏ break tags
5. `routes.py` - Đã thêm giá trị mặc định cho các thuộc tính

## Các file mới được tạo:

1. `database_migration.sql` - Script SQL để migration database
2. `fix_database.py` - Script Python để migration database
3. `test_fixes.py` - Script test để kiểm tra sửa lỗi
4. `BUGFIXES.md` - Tài liệu này

## Lưu ý:

- Nếu Python environment có vấn đề, sử dụng script SQL trực tiếp
- Backup database trước khi chạy migration
- Kiểm tra logs để đảm bảo không có lỗi mới
