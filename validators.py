def validate_booking_form(form, capacity):
    """清洗并校验预约表单，返回可保存的数据和错误列表。"""
    data = {
        "purpose": form.get("purpose", "").strip(),
        "attendee_count": form.get("attendee_count", "").strip(),
        "contact": form.get("contact", "").strip(),
    }
    errors = []

    if not 5 <= len(data["purpose"]) <= 200:
        errors.append("使用目的应填写5至200个字。")

    try:
        attendee_count = int(data["attendee_count"])
    except (TypeError, ValueError):
        attendee_count = 0
    if attendee_count < 1 or attendee_count > capacity:
        errors.append(f"参加人数应在1至{capacity}人之间。")

    if not 6 <= len(data["contact"]) <= 50:
        errors.append("联系方式应填写6至50个字符。")

    data["attendee_count_value"] = attendee_count
    return data, errors


def validate_approval_form(form):
    """校验审批决定；驳回必须说明原因。"""
    decision = form.get("decision", "")
    comment = form.get("comment", "").strip()
    errors = []

    if decision not in {"approve", "reject"}:
        errors.append("请选择通过或驳回。")
    if decision == "reject" and not 3 <= len(comment) <= 300:
        errors.append("驳回时请填写3至300个字的原因。")
    if decision == "approve" and len(comment) > 300:
        errors.append("审批意见不能超过300个字。")

    return decision, comment, errors
