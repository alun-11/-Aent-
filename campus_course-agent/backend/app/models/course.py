from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from app.database import Base


class Course(Base):
    __tablename__ = "courses"
    __table_args__ = {"comment": "课程信息表"}

    name: Mapped[str] = mapped_column(
        String(50), comment="课程名称", unique=True, nullable=False
    )
    code: Mapped[str | None] = mapped_column(
        String(50), comment="课程代码", nullable=True
    )
    password: Mapped[str] = mapped_column(
        String(255), comment="密码", nullable=False
    )
    description: Mapped[str] = mapped_column(
        String(50), comment="课程描述", nullable=False
    )
    role: Mapped[str] = mapped_column(
        String(50), comment="角色：student-学生，admin-管理员", nullable=False
    )

    status: Mapped[int] = mapped_column(default=1, comment="状态：0-禁用，1-正常")
