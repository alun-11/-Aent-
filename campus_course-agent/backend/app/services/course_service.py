from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.common.exceptions import BusinessException
from app.models.course import Course
from app.schemas.course import CourseCreate, CourseResponse, CourseUpdate


def list_courses(db: Session, keywords: str | None = None) -> list[CourseResponse]:
    """获取课程列表"""
    query = db.query(Course)
    if keywords and keywords.strip():
        kw = f"%{keywords.strip()}%"
        query = query.filter(
            or_(
                Course.name.like(kw),
                Course.code.like(kw),
                Course.description.like(kw),
            )
        )
    rows = query.order_by(Course.id.desc()).all()
    return [CourseResponse.model_validate(r) for r in rows]


def create_course(db: Session, data: CourseCreate) -> CourseResponse:
    """新增课程"""
    name = (data.name or "").strip()
    if not name:
        raise BusinessException(message="课程名称不能为空")
    if db.query(Course).filter_by(name=name).first():
        raise BusinessException(message="课程名称已存在")

    course = Course(
        name=name,
        code=(data.code or "").strip() or None,
        password=(data.password or "ENG101").strip() or "ENG101",
        description=(data.description or "").strip() or None,
        status=data.status if data.status in (0, 1) else 1,
    )
    db.add(course)
    db.commit()
    db.refresh(course)
    return CourseResponse.model_validate(course)


def update_course(
    db: Session, course_id: int, data: CourseUpdate
) -> CourseResponse:
    """更新课程"""
    row = db.query(Course).filter_by(id=course_id).first()
    if not row:
        raise BusinessException(message="课程不存在")

    payload = data.model_dump(exclude_unset=True, exclude_none=False)
    # 对必填约束做清洗
    for k in ("name", "code", "password", "description"):
        if k in payload and isinstance(payload[k], str):
            payload[k] = payload[k].strip() or None
    # 名称唯一性校验（排除自己）
    if payload.get("name"):
        dup = (
            db.query(Course)
            .filter(Course.name == payload["name"], Course.id != course_id)
            .first()
        )
        if dup:
            raise BusinessException(message="课程名称已存在")

    for field, value in payload.items():
        if value is not None:
            setattr(row, field, value)

    db.commit()
    db.refresh(row)
    return CourseResponse.model_validate(row)


def delete_course(db: Session, course_id: int) -> None:
    """删除课程"""
    row = db.query(Course).filter_by(id=course_id).first()
    if not row:
        raise BusinessException(message="课程不存在")
    db.delete(row)
    db.commit()
