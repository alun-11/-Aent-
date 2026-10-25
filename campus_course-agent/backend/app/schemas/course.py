from pydantic import BaseModel, ConfigDict


class CourseCreate(BaseModel):
    """课程创建模型"""

    name: str
    code: str | None = None
    password: str | None = None
    description: str | None = None
    status: int = 1


class CourseUpdate(BaseModel):
    """课程更新模型(可选)"""

    name: str | None = None
    code: str | None = None
    password: str | None = None
    description: str | None = None
    status: int | None = None


class CourseResponse(BaseModel):
    """课程返回的数据"""

    id: int
    name: str
    code: str | None = None
    password: str
    description: str | None = None
    status: int

    model_config = ConfigDict(from_attributes=True)  # 允许从 ORM 模型中读取数据
