import json
import os
from typing import List, Dict, Any
from datetime import datetime

RAW_DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "raw-data")

# ---------------------------------------------------------------------------
# Tool #1: search_product_catalog
# TODO: Hoàn thiện hàm này — đọc file product_catalog.json, lọc theo category và max_price.
# ---------------------------------------------------------------------------

def search_product_catalog(category: str, max_price: int = 999999999999) -> List[Dict[str, Any]]:
    """
    Tra cứu sản phẩm/dịch vụ Vingroup theo danh mục và giá tối đa.
    
    Args:
        category: Loại sản phẩm ('xe_dien' hoặc 'du_lich').
        max_price: Giá tối đa (VNĐ). Mặc định không giới hạn.
    
    Returns:
        Danh sách sản phẩm phù hợp điều kiện.
    """
    catalog_file = os.path.join(RAW_DATA_DIR, "product_catalog.json")
    # TODO: Kiểm tra file tồn tại, đọc JSON, lọc sản phẩm
    # Gợi ý: Lọc theo p["category"] == category AND p["price_vnd"] <= max_price
    catalog_file = os.path.join(RAW_DATA_DIR, "product_catalog.json")
    # Kiểm tra file có tồn tại không
    if not os.path.exists(catalog_file):
        return[]
    # Đọc dữ liệu file JSON
    with open(catalog_file, "r", encoding="utf-8") as f:
        products = json.load(f)
    # Lọc sản phẩm theo category và max_price
    filtered_products = [
        p for p in products
        if p["category"] == category
        and p["price_vnd"] <= max_price
    ]
    # Trả về kết quả
    return filtered_products

# ---------------------------------------------------------------------------
# Tool #2: submit_support_ticket
# TODO: Hoàn thiện hàm này — tạo ticket mới và lưu vào support_tickets.json.
# ---------------------------------------------------------------------------

def submit_support_ticket(
    customer_name: str,
    issue_description: str,
    priority: str = "medium"
) -> Dict[str, Any]:
    """
    Ghi nhận yêu cầu hỗ trợ của khách hàng vào hệ thống ticket.
    
    Args:
        customer_name: Tên khách hàng.
        issue_description: Mô tả vấn đề cần hỗ trợ.
        priority: Mức độ ưu tiên ('low', 'medium', 'high'). Mặc định 'medium'.
    
    Returns:
        Thông tin ticket vừa tạo bao gồm ticket_id, status.
    """
    tickets_file = os.path.join(RAW_DATA_DIR, "support_tickets.json")
    # TODO: Load existing tickets, generate new ticket_id, append new ticket, save file
    # Gợi ý: ticket_id = f"TK-{today}-{seq:03d}" với today = datetime.now().strftime("%Y%m%d")
    tickets_file = os.path.join(RAW_DATA_DIR, "support_tickets.json")
    # Kiểm tra file có tồn tại không
    if not os.path.exists(tickets_file):
        return[]
    # Đọc dữ liệu file JSON
    with open(tickets_file, "r", encoding="utf-8") as f:
        tickets = json.load(f)
    # Lấy ngày hiện tại
    today = datetime.now().strftime("%Y%m%d")
    # Tìm số thứ tự ticket tiếp theo trong ngày
    existing_sequences = []
    for ticket in tickets:
        ticket_id = ticket.get("ticket_id", "")
        if ticket_id.startswith(f"TK-{today}-"):
            try:
                seq = int(ticket_id.split("-")[-1])
                existing_sequences.append(seq)
            except ValueError:
                continue
    seq = max(existing_sequences, default=0) + 1
    # Tạo ticket ID
    ticket_id = f"TK-{today}-{seq:03d}"
    # Tạo thông tin ticket mới
    new_ticket = {
        "ticket_id": ticket_id,
        "customer_name": customer_name,
        "issue_description": issue_description,
        "priority": priority,
        "status": "open",
        "created_at": datetime.now().isoformat()
    }
    # Thêm ticket vào danh sách
    tickets.append(new_ticket)
    # Lưu danh sách vào JSON
    with open(tickets_file, "w", encoding="utf-8") as f:
        json.dump(tickets, f, ensure_ascii=False, indent=4)
    return {
        "ticket_id": ticket_id,
        "customer_name": customer_name,
        "issue_description": issue_description,
        "priority": priority,
        "status": "open",
        "created_at": datetime.now().isoformat()
    }

# ---------------------------------------------------------------------------
# TOOL_DEFINITIONS — JSON Schemas mô tả cho LLM
# TODO: Định nghĩa JSON Schema cho từng tool (name, description, parameters).
# ---------------------------------------------------------------------------

TOOL_DEFINITIONS = [
    # TODO: Thêm schema cho "search_product_catalog"
    {
        "name": "search_product_catalog",
        "description": "Tra cứu sản phẩm/dịch vụ Vingroup theo danh mục và giá tối đa.",
        "parameters": {
            "type": "object",
            "properties": {
                "category": {
                    "type": "string",
                    "enum": ["xe_dien", "du_lich"],
                    "description": "Danh mục sản phẩm cần tìm."
                },
                "max_price": {
                    "type": "integer",
                    "description": "Giá tối đa của sản phẩm (VNĐ)."
                }
            },
            "required": ["category"]
        }
    },
    # TODO: Thêm schema cho "submit_support_ticket"
    {
        "name": "submit_support_ticket",
        "description": "Tạo ticket hỗ trợ khách hàng và lưu vào hệ thống.",
        "parameters": {
            "type": "object",
            "properties": {
                "customer_name": {
                    "type": "string",
                    "description": "Tên khách hàng."
                },
                "issue_description": {
                    "type": "string",
                    "description": "Mô tả vấn đề cần hỗ trợ."
                },
                "priority": {
                    "type": "string",
                    "enum": ["low", "medium", "high"],
                    "description": "Mức độ ưu tiên của ticket."
                }
            },
            "required": [
                "customer_name",
                "issue_description"
            ]
        }
    }
]

# ---------------------------------------------------------------------------
# TOOL_MAP — Ánh xạ tên tool → hàm thực thi
# ---------------------------------------------------------------------------

TOOL_MAP = {
    "search_product_catalog": search_product_catalog,
    "submit_support_ticket": submit_support_ticket
}
