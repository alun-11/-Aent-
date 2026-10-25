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
    return [CourseResponse.model_validate(row) for row in rows]


def create_course(db: Session, course_data: CourseCreate) -> CourseResponse:
    """新增课程"""
    if not course_data.name.strip():
        raise BusinessException(message="课程名称不能为空")
    exist = db.query(Course).filter_by(name=course_data.name.strip()).first()
    if exist:
        raise BusinessException(message="课程名称已存在")
    course = Course(
        name=course_data.name.strip(),
        code=(course_data.code or "").strip() or None,
        password=(course_data.password or "").strip(),
        description=(course_data.description or "").strip(),
        role="student",
        status=course_data.status if course_data.status in (0, 1) else 1,
    )
    db.add(course)
    db.commit()
    db.refresh(course)
    return CourseResponse.model_validate(course)


def delete_course(db: Session, course_id: int) -> None:
    """删除课程"""
    course = db.query(Course).filter_by(id=course_id).first()
    if not course:
        raise BusinessException(message="课程不存在")
    db.delete(course)
    db.commit()


def update_course(db: Session, course_id: int, course_data: CourseUpdate) -> CourseResponse:
    """更新课程"""
    course = db.query(Course).filter_by(id=course_id).first()
    if not course:
        raise BusinessException(message="课程不存在")
    if course_data.name is not None:
        if not course_data.name.strip():
            raise BusinessException(message="课程名称不能为空")
        exist = (
            db.query(Course)
            .filter(Course.name == course_data.name.strip(), Course.id != course_id)
            .first()
        )
        if exist:
            raise BusinessException(message="课程名称已存在")
        course.name = course_data.name.strip()
    if course_data.code is not None:
        course.code = course_data.code.strip() or None
    if course_data.password is not None:
        course.password = course_data.password.strip()
    if course_data.description is not None:
        course.description = course_data.description.strip()
    if course_data.status is not None:
        course.status = course_data.status if course_data.status in (0, 1) else 1
    db.commit()
    db.refresh(course)
    return CourseResponse.model_validate(course)
